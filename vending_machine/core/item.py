from decimal import Decimal
from typing import Dict, Any
from .exceptions import InsufficientFundsError, OutOfStockError


# import money

LOG_ERROR = "error"
LOG_SUCCESS = "success"


class Item:

    """
	An item that exists within the vending machine.
	"""

    def __init__(self, name: str, price: Decimal, remaining_stock: int):
        self.name = name
        self.price = price
        if remaining_stock < 0:
            # Not a user facing error, and should only get thrown
            # if the dev touches the code. No need to fancy print.
            raise ValueError(
                f"Cannot have negative stock of an item. Got {remaining_stock}."
            )
        self.remaining_stock = remaining_stock

    def __repr__(self) -> str:
        return "<Item(name={}, price={}, remaining_stock={}>".format(
            self.name, self.price, self.remaining_stock
        )

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return (
                self.name == other.name
                and self.price == other.price
                and self.remaining_stock == other.remaining_stock
            )
        return False

    @classmethod
    def from_json(cls, dumped: Dict[str, Any]):
        """
		Loads the item from a dictionary. Inverse of to_json.
		"""

        return cls(
            name=dumped["name"],
            price=Decimal(dumped["price"]),
            remaining_stock=dumped["remaining_stock"],
        )

    def to_json(self) -> Dict[str, Any]:
        """
		Dumps the item to a serializable dictionary that
		is reloadable using the from_json constructor
		"""

        return {
            "name": self.name,
            "price": str(self.price),
            "remaining_stock": self.remaining_stock,
        }

    def purchase(self, balance: Decimal) -> Decimal:
        """
		Purchases an item from the vending machine. Raises InsufficientFunds
		exception if balance < price of the item.
		:return: Money left from the completed transaction
		"""

        if self.remaining_stock <= 0:
            # Don't need to put a message as that's handle by the
            # vending machine.
            raise OutOfStockError()

        if balance < self.price:
            # Don't need to put a message as that's handle by the
            # vending machine.
            raise InsufficientFundsError()

        remaining_balance = balance - self.price
        self.remaining_stock -= 1

        return remaining_balance
