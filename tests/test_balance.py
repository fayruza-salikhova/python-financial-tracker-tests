from decimal import Decimal


class TestBalance:
    def test_balance(self, tracker):
        tracker.add_transaction("2020-01-01", amount=Decimal("3000"))
        tracker.add_transaction("2022-01-04", amount=Decimal("-1500"))
        assert tracker.balance() == Decimal("1500")
