from decimal import Decimal
from vending_machine.core.exceptions import InsufficientFundsError, OutOfStockError
from vending_machine.core.item import Item
from vending_machine.core.vending_machine import VendingMachine
from vending_machine.utils import money

from hypothesis import given
import hypothesis.strategies as st

import decimal
import pytest


@pytest.fixture
def item():

    return Item(name="Chips", price=Decimal("10.0"), remaining_stock=5)


@pytest.fixture
def machine():

    return VendingMachine()


@pytest.fixture
def loaded_machine(machine):

    machine.deposit(Decimal(10))
    return machine


class BaseLogTestingMixin:
    @staticmethod
    def logs_one_message(caplog, levelname: str = "INFO"):
        """
        Utility method to ensure that exactly one message is logged
        at the provided level.
        """

        assert len(caplog.records) == 1
        logged_record = caplog.records[0]
        assert logged_record.levelname == levelname

class TestViewPurchases(BaseLogTestingMixin):

    def test_view_purchases_log(self, loaded_machine: VendingMachine, caplog):
        """
        Test case ensures that the correct number of messages get logged.
        """

        loaded_machine.purchase_item("A1")
        loaded_machine.purchase_item("A1")

        # Clearing messages emitted by purchasing the item
        caplog.clear()

        loaded_machine.view_purchases()
        assert len(caplog.records) == 3
        assert "You bought" in caplog.text

    def test_view_purchases_logs_header_message(self, machine: VendingMachine, caplog):
        """
        Test case should ensure that a header message gets emitted, regardless
        of whether there were purchases or not.
        """

        machine.view_purchases()
        self.logs_one_message(caplog)
        assert "You've spent 0 on 0 items." in caplog.text
        assert "You bought" not in caplog.text


class TestPurchaseItem(BaseLogTestingMixin):
    def test_out_of_stock_gets_logged_as_error(
        self, loaded_machine: VendingMachine, caplog
    ):
        """
        Test case should ensure error messages from out of stock are getting logged
        to the user correctly.
        """

        loaded_machine.items["A1"].remaining_stock = 0

        loaded_machine.purchase_item("A1")

        self.logs_one_message(caplog)
        assert "ERROR" in caplog.text
        assert "Out of stock!" in caplog.text

    def test_out_of_stock_doesnt_add_purchase(self, loaded_machine: VendingMachine):
        """
        Test case to ensure that if there isn't any stock left of an item, a purchase
        doesn't get added to the purchase log.
        """

        loaded_machine.items["A1"].remaining_stock = 0

        loaded_machine.purchase_item("A1")

        assert len(loaded_machine.purchases) == 0

    def test_incorrect_position_gets_logged_as_error(
        self, loaded_machine: VendingMachine, caplog
    ):
        """
        Test case should ensure that entering a position on the machine that doesn't
        exist should log an error back to the console.
        For example, A1 should exist, while ABC123 shouldn't
        """

        loaded_machine.purchase_item("ABC123")
        self.logs_one_message(caplog)
        assert "ERROR" in caplog.text
        assert "no item located" in caplog.text
        assert "Please try again!" in caplog.text

    def test_incorrect_position_doesnt_add_purchase(
        self, loaded_machine: VendingMachine
    ):
        """
        Test case to ensure that if the position is invalid, a purchase
        doesn't get added to the purchase log.
        """

        loaded_machine.purchase_item("ABC123")
        assert len(loaded_machine.purchases) == 0

    def test_insufficient_funds_gets_logged_as_error(
        self, machine: VendingMachine, caplog
    ):
        """
        Test case should ensure that if the user hasn't loaded enough money
        into the machine that the attempt to purchase an item will
        fail.
        """

        machine.purchase_item("A1")
        self.logs_one_message(caplog)
        assert "ERROR" in caplog.text
        assert "Insufficient funds" in caplog.text

    def test_insufficient_funds_doesnt_add_purchase(self, machine: VendingMachine):
        """
        Test case should ensure that if the user didn't have funds to complete
        the purchase, a purchase isn't added to the log
        """

        machine.purchase_item("A1")
        assert len(machine.purchases) == 0

    def test_successful_purchase_gets_logged_as_success(
        self, loaded_machine: VendingMachine, caplog
    ):
        """
        Test case should ensure that if everything goes well, the user sees a success message
        """

        loaded_machine.purchase_item("A1")
        self.logs_one_message(caplog)
        assert "SUCCESS" in caplog.text
        assert "Purchased" in caplog.text
        assert "Enjoy!" in caplog.text

    def test_purchased_stock_decrements(self, loaded_machine: VendingMachine):
        """
        Mostly already captured by tests on the item, but ensuring
        that the item purchased decrements its stock
        """
        previous_stock = loaded_machine.items["A1"].remaining_stock
        loaded_machine.purchase_item("A1")
        current_stock = loaded_machine.items["A1"].remaining_stock

        assert current_stock == (previous_stock - 1)

    def test_purchased_decreases_balance(self, loaded_machine: VendingMachine):
        """
        Test case ensures that the balance on the machine gets correctly
        updated according to the price of the item purchased
        """

        current_balance = loaded_machine.balance
        price_of_item = loaded_machine.items["A1"].price
        expected_balance = current_balance - price_of_item

        loaded_machine.purchase_item("A1")

        assert loaded_machine.balance == expected_balance

    def test_successful_purchase_gets_added_to_purchase_log(
        self, loaded_machine: VendingMachine
    ):
        """
        Ensures the purchase gets appended to the log
        """
        position = "A1"
        price = loaded_machine.items[position].price
        loaded_machine.purchase_item(position)
        assert len(loaded_machine.purchases) == 1
        purchase = loaded_machine.purchases[0]

        assert purchase.position == position
        assert purchase.price == price


class TestDeposit(BaseLogTestingMixin):
    @given(
        deposit=st.decimals(
            allow_nan=False, min_value=-100_000, max_value=100_000, allow_infinity=False
        )
    )
    def test_deposit_always_logs_a_message(self, deposit: Decimal, caplog):

        deposit = money.to_money(deposit)
        machine = VendingMachine()

        machine.deposit(deposit)
        self.logs_one_message(caplog)
        # Resetting the log capturing utility because hypothesis won't reset it
        caplog.clear()

    @given(deposit=st.decimals(allow_nan=False, min_value=0.01, allow_infinity=False))
    def test_deposit_money_accepts_positive_amounts(self, deposit: Decimal):
        """
        Test case ensures that any positive amount rounded to the
        nearest cent can be accepted by the vending machine.
        """

        deposit = money.to_money(deposit)

        machine = VendingMachine()

        machine.deposit(deposit)
        machine.deposit(deposit)

        assert machine.balance == money.add(deposit, deposit)

    def test_deposit_0_or_less_logs_error_to_user(self, caplog):

        deposit = money.to_money(Decimal("-5"))

        machine = VendingMachine()
        machine.deposit(deposit)

        self.logs_one_message(caplog)
        assert "ERROR" in caplog.text
        assert "negative or 0" in caplog.text

    def test_deposit_money_logs_success_to_user(self, caplog):

        deposit = money.to_money(Decimal("30"))

        machine = VendingMachine()
        machine.deposit(deposit)

        self.logs_one_message(caplog)

        assert "SUCCESS" in caplog.text
        assert "Successfully deposited" in caplog.text


class TestDispenseChange(BaseLogTestingMixin):
    def test_funded_logs_success_with_funded_amount(
        self, loaded_machine: VendingMachine, caplog
    ):
        """
        Tests to make sure that the success message has the balance in it
        """
        balance = loaded_machine.balance
        loaded_machine.dispense_change()
        self.logs_one_message(caplog)
        assert str(balance) in caplog.text
        assert "SUCCESS" in caplog.text
        assert "Dispensed" in caplog.text

    def test_unfunded_logs_success(self, machine: VendingMachine, caplog):
        """
        Tests to make sure that the success message still displays, even
        with 0 balance
        """

        machine.dispense_change()
        self.logs_one_message(caplog)
        assert "SUCCESS" in caplog.text
        assert "Dispensed" in caplog.text

    @given(deposit=st.decimals(allow_nan=False, min_value=0.01, allow_infinity=False))
    def test_resets_balance(self, machine: VendingMachine, deposit: Decimal):
        """
        Test case to ensure that no leftover balance
        is retained after someone requests their change,
        regardless of size of previous deposits
        """

        machine.deposit(deposit)
        machine.deposit(deposit)

        change = machine.dispense_change()
        assert change == money.add(deposit, deposit)
        assert machine.balance == Decimal(0)

class TestViewItems(BaseLogTestingMixin):

    def test_invalid_position_logs_error(self, machine: VendingMachine, caplog):
        """
        Makes sure that if the user types in an invalid position, an error
        message shows
        """

        machine.view_items(column=22, row=100)
        self.logs_one_message(caplog)
        assert "ERROR" in caplog.text
        assert "isn't a slot" in caplog.text

    def test_specific_valid_position_logs_one_success(self, machine: VendingMachine, caplog):
        """
        Ensures that only one message gets logged
        """
        machine.view_items(1, 1)
        self.logs_one_message(caplog)

    def test_view_all_items(self, machine: VendingMachine, caplog):
        """
        Test ensures that the number of items returned to the user
        is len(items) - 1 (one initial success message)
        """

        machine.view_items()
        assert len(caplog.records) == len(machine.items)


def test_to_and_from_json_inverse(loaded_machine):
    """
    Test case to ensure the machine is json serializable
    and will load to its previous state if reloaded
    immediately.
    """

    dumped = loaded_machine.to_json()

    loaded = VendingMachine.from_json(dumped)
    assert loaded == loaded_machine


@given(stock=st.integers(min_value=0))
def test_fill_machine_assigns_correct_stock(stock: int):
    """
    Test case should ensure the param given to constructor
    successfully passes through to all generated vending
    machine items.
    """

    machine = VendingMachine(stock=stock)

    for item in machine.items.values():
        assert item.remaining_stock == stock


def test_fill_machine_stops_filling_after_number_out_of_items():
    """
    Test case ensures that if too many items are specified,
    the program will just utlize all of them instead of crashing
    and burning.
    """

    num_items = len(VendingMachine.vending_machine_items)

    machine = VendingMachine(stock=num_items + 1)

    assert len(machine.items.keys()) == num_items


