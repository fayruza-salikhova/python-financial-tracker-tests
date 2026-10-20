import pytest
from pftracker import PersonalFinanceTracker
from pftracker.storage import JsonFileStorage
from decimal import Decimal


class TestPersistence:

    @classmethod
    @pytest.fixture(scope="class")
    def reopened_tracker(cls, tmp_path_factory):
        storage_dir = tmp_path_factory.mktemp("pftracker")
        json_storage_path = storage_dir / "finance.json"

        with PersonalFinanceTracker(storage=JsonFileStorage(json_storage_path)) as tracker:
            tracker.add_category("salary")
            tracker.add_category("rent")
            tracker.add_category("groceries")
            tracker.set_budget(month="2020-05", category="groceries", amount=Decimal("1200"))
            tracker.add_transaction("2020-05-01", Decimal("-100"), category="groceries")
            tracker.add_transaction("2021-05-01", Decimal("-50"), category="groceries")
            tracker.add_transaction("2022-05-01", Decimal("-1"), category="groceries")
        with PersonalFinanceTracker(storage=JsonFileStorage(json_storage_path)) as reopened_tracker:
            yield reopened_tracker

    def test_categories_saved(self, reopened_tracker):
        assert reopened_tracker.list_categories() == sorted(["salary", "rent", "groceries"])

    def test_transactions_saved(self, reopened_tracker):
        assert len(reopened_tracker.list_transactions(category="groceries")) == 3

    def test_budget_saved(self, reopened_tracker):
        assert reopened_tracker.budget_status(month="2020-05")["groceries"]["spent"] == Decimal("100")
