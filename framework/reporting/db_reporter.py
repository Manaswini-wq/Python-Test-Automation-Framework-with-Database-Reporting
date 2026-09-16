"""
MongoDB reporter — stores test results in database for trend analysis.
"""
from pymongo import MongoClient
from datetime import datetime, timezone
from typing import Optional

from framework.core.test_result import TestResult, SuiteResult


class DBReporter:
    def __init__(self, uri: str = "mongodb://localhost:27017",
                 db_name: str = "test_results",
                 collection: str = "runs"):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection
        self._client: Optional[MongoClient] = None
        self._run_id: Optional[str] = None

    def _connect(self):
        if self._client is None:
            self._client = MongoClient(self.uri)

    def _get_collection(self):
        self._connect()
        return self._client[self.db_name][self.collection_name]

    def on_suite_start(self, suite_name: str):
        pass

    def on_test_result(self, result: TestResult):
        pass

    def on_suite_end(self, suite_result: SuiteResult):
        try:
            collection = self._get_collection()
            doc = {
                **suite_result.to_dict(),
                "run_timestamp": datetime.now(timezone.utc),
            }
            insert_result = collection.insert_one(doc)
            self._run_id = str(insert_result.inserted_id)
        except Exception as e:
            print(f"[DBReporter] Warning: Failed to store results: {e}")

    def get_history(self, suite_name: str, limit: int = 50) -> list[dict]:
        """Query past test runs for trend analysis."""
        collection = self._get_collection()
        cursor = (collection
                  .find({"suite_name": suite_name}, {"_id": 0})
                  .sort("run_timestamp", -1)
                  .limit(limit))
        return list(cursor)

    def get_flaky_tests(self, suite_name: str, runs: int = 20) -> list[dict]:
        """Find tests that sometimes pass and sometimes fail (flaky)."""
        collection = self._get_collection()
        pipeline = [
            {"$match": {"suite_name": suite_name}},
            {"$sort": {"run_timestamp": -1}},
            {"$limit": runs},
            {"$unwind": "$results"},
            {"$group": {
                "_id": "$results.test_name",
                "statuses": {"$addToSet": "$results.status"},
                "fail_count": {
                    "$sum": {"$cond": [{"$eq": ["$results.status", "FAILED"]}, 1, 0]}
                },
                "total": {"$sum": 1},
            }},
            {"$match": {"statuses": {"$all": ["PASSED", "FAILED"]}}},
            {"$sort": {"fail_count": -1}},
        ]
        return list(collection.aggregate(pipeline))

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
