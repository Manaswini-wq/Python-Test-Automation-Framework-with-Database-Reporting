"""
Demonstrates testing with mock objects and fixtures.
"""
from framework.core.test_case import TestCase, tag
from framework.assertions.matchers import (
    assert_equal, assert_not_none, assert_isinstance, assert_in
)


class MockAPIClient:
    """Simulates an API client for testing."""
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.connected = False

    def connect(self):
        self.connected = True

    def get(self, endpoint: str) -> dict:
        if not self.connected:
            raise ConnectionError("Not connected")
        return {"status": 200, "endpoint": endpoint, "data": {"id": 1, "name": "test"}}

    def post(self, endpoint: str, data: dict) -> dict:
        if not self.connected:
            raise ConnectionError("Not connected")
        return {"status": 201, "endpoint": endpoint, "id": 42}

    def disconnect(self):
        self.connected = False


class TestAPIClient(TestCase):
    def setUp(self):
        self.client = MockAPIClient("http://localhost:8080")
        self.client.connect()

    def tearDown(self):
        self.client.disconnect()

    @tag("integration", "api")
    def test_get_request(self):
        response = self.client.get("/api/v1/users")
        assert_equal(response["status"], 200)
        assert_not_none(response["data"])

    @tag("integration", "api")
    def test_post_request(self):
        response = self.client.post("/api/v1/users", {"name": "John"})
        assert_equal(response["status"], 201)
        assert_in("id", response)

    def test_response_structure(self):
        response = self.client.get("/api/v1/items")
        assert_isinstance(response, dict)
        assert_in("data", response)
        assert_isinstance(response["data"], dict)
