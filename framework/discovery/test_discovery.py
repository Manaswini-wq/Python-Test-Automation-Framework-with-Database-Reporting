"""
Test discovery — finds test classes by scanning directories.
"""
import os
import importlib
import importlib.util
import sys

from framework.core.test_case import TestCase
from framework.core.test_suite import TestSuite


class TestDiscovery:
    def __init__(self, pattern: str = "test_*.py"):
        self.pattern = pattern

    def discover(self, search_path: str, suite_name: str = "Discovered") -> TestSuite:
        suite = TestSuite(name=suite_name)
        test_files = self._find_test_files(search_path)

        for filepath in sorted(test_files):
            classes = self._load_test_classes(filepath)
            for cls in classes:
                suite.add_class(cls)

        return suite

    def _find_test_files(self, path: str) -> list[str]:
        files = []
        for root, _, filenames in os.walk(path):
            for fn in filenames:
                if fn.startswith("test_") and fn.endswith(".py"):
                    files.append(os.path.join(root, fn))
        return files

    def _load_test_classes(self, filepath: str) -> list[type[TestCase]]:
        module_name = os.path.splitext(os.path.basename(filepath))[0]
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None or spec.loader is None:
            return []

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        try:
            spec.loader.exec_module(module)
        except Exception:
            return []

        classes = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and issubclass(attr, TestCase)
                    and attr is not TestCase):
                classes.append(attr)
        return classes
