from decimal import Decimal
from datetime import date
import pytest


class TestBalance:
    @pytest.mark.parametrize(
        "amounts, expected_balance",
        [
            pytest.param(
                [Decimal("100.00"), Decimal("-20.00")],
                Decimal("80.00"),
                id="income-greater-than-expenses",
            ),
            pytest.param(
                [Decimal("20.00"), Decimal("-100.00")],
                Decimal("-80.00"),
                id="expenses-greater-than-income",
            ),
            pytest.param(
                [Decimal("100.00"), Decimal("-100.00")],
                Decimal("0.00"),
                id="income-equals-expenses",
            ),
            pytest.param(
                [Decimal("10.00"), Decimal("20.00")],
                Decimal("30.00"),
                id="only-income",
            ),
            pytest.param(
                [Decimal("-10.00"), Decimal("-20.00")],
                Decimal("-30.00"),
                id="only-expenses",
            ),
            pytest.param(
                [Decimal("0.01"), Decimal("-0.01")],
                Decimal("0.00"),
                id="minimum-currency-unit",
            ),
            pytest.param(
                [Decimal("100000000.00"), Decimal("-1.00")],
                Decimal("99999999.00"),
                id="large-income-small-expense",
            ),
            pytest.param(
                [Decimal("1000"), Decimal("-250"), Decimal("500"), Decimal("-100"), Decimal("-50")],
                Decimal("1100"),
                id="many_transactions",
            ),
            pytest.param(
                [Decimal("10.25"), Decimal("-3.15"), Decimal("2.40")],
                Decimal("9.50"),
                id="balance_with_decimal_amount",
            ),
        ],
    )
    def test_balance_calculation(self, tracker, amounts, expected_balance):
        for amount in amounts:
            tracker.add_transaction(
                when=date.today(),
                amount=amount,
            )

        assert tracker.balance() == expected_balance

    def test_balance_without_transactions(self, tracker):
        assert tracker.balance() == Decimal("0")
