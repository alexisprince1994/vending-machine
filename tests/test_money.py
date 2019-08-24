from decimal import Decimal

import pytest

from vending_machine.utils import to_money, add


@pytest.mark.parametrize(
    "input_val,output",
    [("0.5200000005", "0.52"), ("5.50", "5.50"), ("10.7501283", "10.75"), ("10", "10")],
)
def test_to_money_rounds_to_2_decimal_places(
    input_val, output
):  # pylint: disable=invalid-name
    """
    Testing to make sure that regardless of how many decimal places
    are in the input, the output always has 2.
    """

    dec = Decimal(input_val)

    assert to_money(dec) == Decimal(output)


def test_add_2_args():
    """
    Adding 2 decimals and ensuring the result rounds correctly
    """

    dec1 = Decimal("5.5")
    dec2 = Decimal("5.5")

    assert add(dec1, dec2) == Decimal("11")


def test_add_3_args():
    """
    Test case should ensure that an arbitrary number of positional
    arguments are accepted
    """

    dec1 = Decimal("5.50")
    dec2 = Decimal("5.5")
    dec3 = Decimal("5.5000")

    assert add(dec1, dec2, dec3) == Decimal("16.5")
