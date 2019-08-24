from decimal import Decimal

import hypothesis.strategies as st
from hypothesis import given
import pytest


from vending_machine.core.exceptions import InsufficientFundsError, OutOfStockError
from vending_machine.core.item import Item
from vending_machine.utils import money


@pytest.fixture
def item():  # pylint: disable=missing-docstring

    return Item(name="Chips", price=Decimal("10.0"), remaining_stock=5)


def test_to_json(item: Item):  # pylint: disable=redefined-outer-name
    """
    Test case ensures the item object dumps to a json serializable
    dict correctly.
    """
    assert item.to_json() == {"name": "Chips", "price": "10.0", "remaining_stock": 5}


def test_from_json(item: Item):  # pylint: disable=redefined-outer-name
    """
    Ensures that the item can be dumped and loaded back to json
    and still be equal to itself
    """

    dumped = item.to_json()

    loaded = Item.from_json(dumped)

    assert item == loaded


class TestPurchase:
    """
    All tests related to the purchase method on the Item object
    """

    @given(balance=st.decimals(allow_nan=False, max_value=9, allow_infinity=False))
    def test_insufficient_funds_gets_raised(
        self, item: Item, balance: Decimal
    ):  # pylint: disable=no-self-use,invalid-name,redefined-outer-name
        """
        Test case should cover any instance where
        the price of the item is greater than the balance
        provided.
        """

        with pytest.raises(InsufficientFundsError):
            item.purchase(balance)

    # def test_insufficient_funds_gets_logged_as_error(self, item: Item, caplog):
    # 	"""
    # 	Test case should ensure insufficient funds error messages are getting logged
    # 	to the user correctly.
    # 	"""

    # 	balance = Decimal("2")
    # 	with pytest.raises(InsufficientFundsError):
    # 		item.purchase(balance)

    # 	assert len(caplog.records) == 1

    # 	logged_record = caplog.records[0]
    # 	assert logged_record.levelname == 'INFO'
    # 	assert "ERROR" in caplog.text
    # 	assert "Insufficient funds" in caplog.text

    @given(balance=st.decimals(allow_nan=False, min_value=10))
    def test_out_of_stock_gets_raised(
        self, item: Item, balance: Decimal
    ):  # pylint: disable=no-self-use,invalid-name,redefined-outer-name
        """
        Test case should cover any instance where
        the item doesn't have enough stock to be purchased (0).
        """

        item.remaining_stock = 0
        with pytest.raises(OutOfStockError):
            item.purchase(balance)

    # def test_out_of_stock_gets_logged_as_errors(self, item: Item, caplog):
    # 	"""
    # 	Test case should ensure error messages from out of stock are getting logged
    # 	to the user correctly.
    # 	"""
    # 	balance = Decimal("2")
    # 	item.remaining_stock = 0
    # 	with pytest.raises(OutOfStockError):
    # 		item.purchase(balance)

    # 	assert len(caplog.records) == 1
    # 	caplog.records[0].levelname == 'INFO'
    # 	assert "ERROR" in caplog.text
    # 	assert "Out of stock!" in caplog.text

    def test_insufficient_funds_doesnt_decrease_stock(
        self, item: Item
    ):  # pylint: disable=no-self-use,invalid-name,redefined-outer-name
        """
        Test case should ensure an error raised to insufficient
        money should not detract from the stock of the item,
        as it wasn't actually purchased and dispensed.
        """

        stock_before = item.remaining_stock

        with pytest.raises(InsufficientFundsError):
            item.purchase(Decimal("5"))

        assert stock_before == item.remaining_stock

    def test_purchases_decreases_stock(
        self, item: Item
    ):  # pylint: disable=no-self-use,invalid-name,redefined-outer-name
        """
        Test case should ensure any successful purchase
        of an item should decrement the stock.
        """

        stock_before = item.remaining_stock

        item.purchase(Decimal("500"))

        assert stock_before == item.remaining_stock + 1

    # def test_purchases_gets_logged_as_success(self, item: Item, caplog):
    # 	"""
    # 	Test case ensures successful purchases should log success
    # 	to user
    # 	"""

    # 	balance = Decimal("50")
    # 	item.purchase(balance)

    # 	assert len(caplog.records) == 1
    # 	caplog.records[0].levelname == 'INFO'
    # 	assert "SUCCESS" in caplog.text
    # 	assert "Purchased" in caplog.text
    # 	assert "Enjoy" in caplog.text

    # @given(
    #     balance=st.decimals(
    #         allow_nan=False, min_value=-100_000, max_value=100_000, allow_infinity=False
    #     )
    # )
    # def test_purchase_always_logs_as_message(
    #     self, item: Item, balance: Decimal, caplog
    # ):
    #
    #     balance = money.to_money(balance)
    #     item.remaining_stock = 5
    #
    #     try:
    #         item.purchase(balance)
    #     except InsufficientFundsError as e:
    #         # doesn't matter if it throws an error
    #         pass
    #
    #     assert len(caplog.records) == 1
    #     caplog.records[0].levelname == "INFO"
    #     # reset for hypothesis
    #     caplog.clear()

    @given(
        balance=st.decimals(
            allow_nan=False, min_value=10, max_value=100_000, allow_infinity=False
        )
    )
    def test_purchase_returns_proper_change(
        self, item: Item, balance: Decimal
    ):  # pylint: disable=no-self-use,invalid-name,redefined-outer-name
        """
        Testing to ensure that any valid purchase returns proper change
        by the formula ouput = input - price of item.

        Capping largest value at 100k because when a decimal
        gets generated by hypothesis that is larger than decimal's
        size precision, an error gets thrown.
        """

        balance = money.to_money(balance)
        expected_change = money.subtract(balance, item.price)
        # Hypothesis doesn't reset the fixture, so we're going to manually
        # reset the remaining_stock instance variable to make sure
        # we don't hit OutOfStockErrors after a couple tests
        item.remaining_stock = 5

        change = item.purchase(balance)

        assert change == expected_change
