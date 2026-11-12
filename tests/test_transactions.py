from decimal import Decimal
from datetime import date
import pytest


class TestTransactions:

    @pytest.fixture(
        params=[
            Decimal("0.01"),
            Decimal("1.23"),
            Decimal("100000000.00"),
        ],
        ids=[
            "income-cent",
            "income-small",
            "income-large",
        ],
    )
    def positive_amount(self, request):
        return request.param

    @pytest.fixture(
        params=[
            Decimal("-0.01"),
            Decimal("-1.23"),
            Decimal("-100000000.00"),
        ],
        ids=[
            "expense-cent",
            "expense-small",
            "expense-large",
        ],
    )
    def negative_amount(self, request):
        return request.param

    def test_positive_transaction(self, tracker, positive_amount):
        tracker.add_transaction(
            when=date.today(),
            amount=positive_amount,
        )

        transactions = tracker.list_transactions()

        assert transactions[0].amount == positive_amount
        assert tracker.balance() == positive_amount

    def test_negative_transaction(self, tracker, negative_amount):
        tracker.add_transaction(
            when=date.today(),
            amount=negative_amount,
        )

        transactions = tracker.list_transactions()

        assert transactions[0].amount == negative_amount
        assert tracker.balance() == negative_amount

    def test_zero_amount_raises_error(self, tracker):
        with pytest.raises(ValueError, match="Amount cannot be zero"):
            tracker.add_transaction(
                when=date.today(),
                amount=Decimal("0"),
            )
        assert tracker.list_transactions() == []

    def test_add_multiple_transactions(self, tracker):
        tracker.add_transaction("2020-01-01", amount=Decimal("100"))
        tracker.add_transaction("2020-01-02", amount=Decimal("-30"))
        tracker.add_transaction("2020-01-03", amount=Decimal("50"))

        transactions = tracker.list_transactions()

        assert len(transactions) == 3
        assert [t.amount for t in transactions] == [
            Decimal("100"),
            Decimal("-30"),
            Decimal("50"),
        ]

    def test_delete_transaction(self, tracker):
        t1 = tracker.add_transaction("2020-01-01", amount=50)
        t2 = tracker.add_transaction("2020-01-01", amount=-1000)
        tracker.delete_transaction(t1)

        assert len(tracker.list_transactions()) == 1
        assert tracker.list_transactions()[0].id == t2
        assert tracker.balance() == Decimal("-1000")

    def test_delete_last_transaction(self, tracker):
        t = tracker.add_transaction("2020-01-01", amount=Decimal("100"))

        tracker.delete_transaction(t)

        assert tracker.list_transactions() == []
        assert tracker.balance() == Decimal("0")

    def test_transactions_sorted_by_date(self, tracker):
        tracker.add_transaction("2020-01-03", amount=Decimal("30"))
        tracker.add_transaction("2020-01-01", amount=Decimal("10"))
        tracker.add_transaction("2020-01-02", amount=Decimal("20"))

        transactions = tracker.list_transactions()

        assert [t.amount for t in transactions] == [
            Decimal("10"),
            Decimal("20"),
            Decimal("30"),
        ]

    def test_transaction_description(self, tracker):
        tracker.add_transaction(
            "2020-01-01",
            amount=Decimal("-50"),
            description="Groceries",
        )

        transaction = tracker.list_transactions()[0]

        assert transaction.description == "Groceries"
