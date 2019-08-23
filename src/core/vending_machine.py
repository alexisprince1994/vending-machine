from decimal import Decimal
import string
from typing import Tuple, Dict, Optional, List, Any
from .item import Item
from .purchase import Purchase
from src import money
from src.utils import position_from_coordinates
from .exceptions import InvalidLocationError, InsufficientFundsError, OutOfStockError
from src.ui.printer import fancy_print, formatted_print
import decimal

LOG_ERROR = "error"
LOG_SUCCESS = "success"


class VendingMachine:

    """
    Top level class that handles routing functionality of
    vending machine requests.
    """

    vending_machine_items = [
        {"name": "Gatorade (Blue)", "price": Decimal("1.75")},
        {"name": "Gatorade (Yellow)", "price": Decimal("1.75")},
        {"name": "Gatorade (Red)", "price": Decimal("1.75")},
        {"name": "Gatorade (Orange)", "price": Decimal("1.75")},
        {"name": "Coca Cola", "price": Decimal("1.25")},
        {"name": "Fruit Snacks", "price": Decimal("0.75")},
        {"name": "Oreos", "price": Decimal("0.50")},
        {"name": "Lays", "price": Decimal("1.00")},
        {"name": "Ruffles", "price": Decimal("1.00")},
        {"name": "Cheetos", "price": Decimal("1.00")},
        {"name": "Reeses Cups", "price": Decimal("0.75")},
        {"name": "KitKat", "price": Decimal("0.75")},
        {"name": "M&Ms", "price": Decimal("0.75")},
        {"name": "Orbit", "price": Decimal("0.25")},
        {"name": "Trident", "price": Decimal("0.25")},
    ]

    def __init__(
        self,
        items: Optional[Dict] = None,
        stock: int = 3,
        balance: Optional[Decimal] = None,
        purchases: List[Purchase] = None,
    ):
        """
        Constructor for a Vending Machine.
        """
        if items is None:
            # Fixing the size of the machine, mostly because
            # I can't think of that many different snacks to put
            # into it. Don't worry, I'll make sure the code works
            # regardless of size (assuming a reasonable size (<= 20, 20))
            items = self.create_initial_machine(
                self.vending_machine_items, rows=5, columns=3, stock=stock
            )

        self.items = items
        self._balance = balance if balance else Decimal(0)
        self.purchases = purchases if purchases else []

    @staticmethod
    def create_initial_machine(
        vending_machine_items: Dict[str, Any], rows: int, columns: int, stock: int = 3
    ) -> None:
        """
        Initializing the machine's state full of vending
        machine items. Hiding this in another method to
        eventually make this stateful if required.
        """

        items = {}

        letters = string.ascii_uppercase

        item_number = 0
        for column in range(columns):
            letter = letters[column]
            for row in range(rows):
                location = "{}{}".format(letter, row + 1)

                try:
                    item_dict = vending_machine_items[item_number]
                except IndexError as e:
                    print(
                        f"Not enough predetermined vending machine items. Qutting at {item_number}"
                    )
                    return
                item_dict["remaining_stock"] = stock
                items[location] = Item(**item_dict)
                item_number += 1

        return items

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.items == other.items
                and self.balance == other.balance
                and self.purchases == other.purchases
            )
        return False

    @property
    def balance(self):
        """
        Property responsible for displaying money nicely
        instead of just a Decimal object that could
        have up to 28 points of precision
        """
        return money.to_money(self._balance)

    def to_json(self) -> Dict[str, Any]:
        """
        Dumps the core vending machine object to a json
        serializable object to be able to save to disk
        to persist state across CLI commands.
        """

        return {
            "balance": str(money.to_money(self._balance)),
            "items": {
                location: item.to_json() for location, item in self.items.items()
            },
            "purchases": [purchase.to_json() for purchase in self.purchases],
        }

    @classmethod
    def from_json(cls, dumped: Dict[str, Any]):
        """
        Loads the core vending machine object from a json
        serializable object to be able to save to disk
        to persist state across CLI commands.
        """
        balance = dumped["balance"]
        purchases = [Purchase.from_json(purchase) for purchase in dumped["purchases"]]
        items = {
            location: Item.from_json(item) for location, item in dumped["items"].items()
        }

        return cls(balance=Decimal(balance), items=items, purchases=purchases)

    def view_purchases(self) -> None:
        """
        Lists out the purchases a user has made on this machine.
        There should be one message per purchase, as well as one stating
        how many purchases and how much money they spent.
        """

        total_amount_spent = sum((purchase.price for purchase in self.purchases))
        total_items_bought = len(self.purchases)

        header_message = "You've spent {} on {} items.".format(
                total_amount_spent, total_items_bought)
        if total_items_bought > 0:
            header_message += " You bought..."

        formatted_print(header_message)
        for indx, purchase in enumerate(self.purchases):
            message = "{}: {} costs {}".format(indx, self.items[purchase.position], purchase.price)
            formatted_print(message)



    def view_items(self, column: int = None, row: int = None) -> None:
        """
        Top level function responsible for listing out the items
        in the vending machine.
        If column or row are supplied, the items will be filtered
        for the subset specified.
        """

        if column is not None:
            try:
                letter, _ = position_from_coordinates(column, 1)
            except IndexError:
                fancy_print(LOG_ERROR, f"{letter}{row} isn't a slot on this machine.")
                return None

        if column is not None and row is not None:
            letter, row = position_from_coordinates(column, row)
            if f"{letter}{row}" not in self.items:
                fancy_print(LOG_ERROR, f"{letter}{row} isn't a slot on this machine.")
                return None

        # Not planning on modifying underlying items, but better
        # to be safe than sorry
        items = self.items.copy()

        if row is not None:
            items = {
                position: item for position, item in items.items() if str(row) in position
            }

        if column is not None:

            items = {
                position: item for position, item in items.items() if letter in position
            }

        messages = [
            "{}: {} costs {}, and there are {} units in stock.".format(position, item.name, item.price, item.remaining_stock)
            for position, item in sorted(items.items())
        ]

        
        for message in messages:
            formatted_print(message)

    def purchase_item(self, position: str) -> None:
        """
        Top level function that handles purchasing an item
        for the user and printing the result back to the console.
        """

        try:
            item = self.items[position]
            self._balance = item.purchase(self.balance)
            self.purchases.append(Purchase(position, item.price))

        except KeyError:
            fancy_print(
                LOG_ERROR, f"There is no item located at {position}. Please try again!"
            )

        except OutOfStockError:
            fancy_print(LOG_ERROR, f"Out of stock! There are no more {item.name} left!")

        except InsufficientFundsError:
            fancy_print(
                LOG_ERROR,
                f"Insufficient funds. {item.name} costs {item.price}, but got {self.balance}.",
            )
        else:
            fancy_print(
                LOG_SUCCESS,
                f"Purchased {item.name} for {item.price}. Your remaining balance is {self.balance}. Enjoy!",
            )

    def deposit(self, deposit_amount: Decimal) -> Decimal:
        """
        Inserting money into the vending machine.
        :return: Current Balance
        """

        if deposit_amount <= 0:
            fancy_print(LOG_ERROR, "Can't add negative or 0 cents to the machine.")
            return None

        self._balance = self._balance + deposit_amount
        fancy_print(
            LOG_SUCCESS,
            f"Successfully deposited {deposit_amount}. Your balance is now {self.balance}.",
        )

    def dispense_change(self) -> Decimal:
        """
        Returns the remaining amount to the user
        """

        change = money.to_money(self._balance)

        self._balance = Decimal(0)
        fancy_print(LOG_SUCCESS, f"Dispensed {change}. Have a good day!")

        return change
