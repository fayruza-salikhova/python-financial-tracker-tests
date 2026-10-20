import pytest
import logging
from pftracker.models import UnknownCategory


class TestCategories:
    def test_add_category(self, tracker):
        tracker.add_category("Groceries")
        assert tracker.list_categories() == ["Groceries"]

    def test_add_same_category_twice(self, tracker):
        tracker.add_category("Groceries")
        tracker.add_category("Groceries")
        assert tracker.list_categories() == ["Groceries"]

    def test_add_category_strips_whitespace(self, tracker):
        tracker.add_category(" Groceries  ")
        assert tracker.list_categories() == ["Groceries"]

    def test_add_empty_category_raises_value_error(self, tracker):
        with pytest.raises(ValueError) as exc:
            tracker.add_category("")
        assert str(exc.value) == "Category name cannot be empty"

    def test_add_category_upload_logs(self, tracker, caplog):

        with caplog.at_level(logging.INFO, logger="pftracker"):
            category_name = "Groceries"
            tracker.add_category(category_name)
        assert f"Added category '{category_name}'" in caplog.messages

    def test_delete_category(self, tracker):
        tracker.add_category("Groceries")
        tracker.delete_category("Groceries")
        assert tracker.list_categories() == []

    def test_delete_unknown_category(self, tracker):
        tracker.add_category("Groceries")
        with pytest.raises(UnknownCategory) as exc:
            tracker.delete_category("Not Groceries")
        assert str(exc.value) == "Not Groceries"

    def test_delete_category_in_empty_storage(self, tracker):
        with pytest.raises(UnknownCategory) as exc:
            tracker.delete_category("Groceries")
        assert str(exc.value) == "Groceries"

    def test_delete_category_upload_logs(self, tracker, caplog):
        category_name = "Groceries"
        tracker.add_category(category_name)
        with caplog.at_level(logging.INFO, logger="pftracker"):
            tracker.delete_category("Groceries")
        assert f"Deleted category '{category_name}'" in caplog.messages

    def test_list_categories(self, tracker):
        assert tracker.list_categories() == []

    def test_list_categories_sorted_alphabetically(self, tracker):
        category_name1 = "Groceries"
        category_name2 = "Electronics"
        category_name3 = "Vehicles"
        tracker.add_category(category_name1)
        tracker.add_category(category_name2)
        tracker.add_category(category_name3)
        assert tracker.list_categories() == [
            category_name2,
            category_name1,
            category_name3,
        ]
