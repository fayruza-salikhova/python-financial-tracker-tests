from decimal import Decimal
import pytest


class TestConversion:
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

    def test_multiple_positive_transactions_in_diff_currencies(self, tracker):
        tracker.add_transaction(
            "2020-01-01",
            amount=Decimal("100"),
            currency="USD",
        )
        tracker.add_transaction(
            "2020-01-02",
            amount=Decimal("200"),
            currency="JPY",
        )

        assert tracker.balance() == Decimal("270")

    def test_negative_transaction_in_diff_currency(self, tracker):
        tracker.add_transaction(
            "2020-01-01",
            amount=Decimal("-100"),
            currency="USD",
        )

        assert tracker.balance() == Decimal("-90")

    def test_balance_with_multiple_currencies(self, tracker):
        tracker.add_transaction(
            "2020-01-01",
            amount=Decimal("100"),
            currency="USD",
        )
        tracker.add_transaction(
            "2020-01-02",
            amount=Decimal("-50"),
            currency="JPY",
        )
        tracker.add_transaction(
            "2020-01-03",
            amount=Decimal("20"),
            currency="EUR",
        )

        assert tracker.balance() == Decimal("65")

    def test_conversion_rounding(self, tracker):
        tracker.add_transaction(
            "2020-01-01",
            amount=Decimal("10.01"),
            currency="USD",
        )

        assert tracker.balance() == Decimal("9.01")

    def test_currency_lowercase(self, tracker):
        tracker.add_transaction(
            "2020-01-01",
            amount=Decimal("100"),
            currency="usd",
        )

        assert tracker.balance() == Decimal("90")
