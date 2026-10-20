from decimal import Decimal
import pytest


class TestConvertion:
    @pytest.fixture(autouse=True)
    def mock_currencies_conversion(self, monkeypatch):
        monkeypatch.setattr(
            "pftracker.main.PersonalFinanceTracker._get_convertion_rate",
            lambda *args, **kwargs: Decimal("0.9"),
        )

    def test_transaction_in_diff_currency(self, tracker):
        tracker.add_transaction("1999-01-04", amount=Decimal("100"), currency="USD")
        assert tracker.balance() == Decimal("90"), tracker.balance()

    def test_budget_with_transactions_diff_currency(self, tracker):
        tracker.add_category("Rent")

        tracker.set_budget(month="2020-01", category="Rent", amount=Decimal("5000"), currency="EUR")

        tracker.add_transaction("2020-01-05", Decimal("-1000"), category="Rent", currency="JPY")
        tracker.add_transaction("2020-01-05", Decimal("-100"), category="Rent", currency="USD")
        tracker.add_transaction("2020-01-05", Decimal("-10"), category="Rent", currency="EUR")

        assert tracker.budget_status("2020-01")["Rent"]["spent"] == Decimal("900") + Decimal("90") + Decimal("10")
