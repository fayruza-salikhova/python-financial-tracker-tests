import pytest
from pftracker import PersonalFinanceTracker
from decimal import Decimal


class TestCurrency:
    @pytest.mark.parametrize("currency", ["USD", "EUR", "JPY"])
    def test_tracker_default_currency(self, monkeypatch, storage, currency):
        monkeypatch.setenv("DEFAULT_CURRENCY", currency)
        with PersonalFinanceTracker(storage=storage) as tracker:
            assert tracker.base_currency == currency

    def test_base_currency_does_not_require_conversion(self, tracker, monkeypatch):
        def fail_if_called(*args, **kwargs):
            raise AssertionError("Conversion should not be called")

        monkeypatch.setattr(
            "pftracker.main.PersonalFinanceTracker._get_convertion_rate",
            fail_if_called,
        )

        tracker.add_transaction(
            "2020-01-01",
            amount=Decimal("100"),
            currency="EUR",
        )

        assert tracker.balance() == Decimal("100")
