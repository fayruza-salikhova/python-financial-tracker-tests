import pytest
from pftracker import PersonalFinanceTracker
from pftracker.storage import JsonFileStorage


class TestCategories:
    def test_add_transaction(self, tmp_path):
        storage = JsonFileStorage(tmp_path / "finance.json")
        ft = PersonalFinanceTracker(storage=storage)
