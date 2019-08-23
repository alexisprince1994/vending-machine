from decimal import Decimal


"""
A couple of utility functions that will make it a lot easier to deal with
decimals in the context of money. There are laws in the context
of where to round (up vs down, ending in 0 vs ending in 5, 
towards or away from even/odd, etc.), but for this example,
we'll just assign a constant and roll with it.
"""


def to_money(dec: Decimal) -> Decimal:
    """
    Converts an arbitrarily long (precision-wise) decimal
    to one with 2 decimal points.
    """

    cents = Decimal(".01")
    money = dec.quantize(cents)

    return money


def add(first: Decimal, second: Decimal, *args: Decimal) -> Decimal:
    """
    Adds two or more decimals and converts the precision to one with
    2 decimal points.
    """

    money = first + second

    for additional_amount in args:
        money += additional_amount

    return to_money(money)


def subtract(first: Decimal, second: Decimal, *args: Decimal) -> Decimal:
    """
    Substracts one or more values from the first argument, then
    converts precision to 2 decimal points.
    """

    money = first - second

    for additional_amount in args:
        money -= additional_amount

    return to_money(money)
