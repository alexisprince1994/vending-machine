from src.ui.printer import fancy_print
from src.utils import position_from_coordinates
from typing import Dict
from decimal import Decimal


class Purchase:
    """
	Thin wrapper class around a basic dictionary to allow
	the "purchase" event to be JSON serializable,
	while being clearer than just using a dictionary
	"""

    def __init__(self, position: str, price: Decimal):
        self.position = position
        self.price = price

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.position == other.position and self.price == other.price
        return False

    def to_json(self) -> Dict[str, int]:

        return {"position": self.position, "price": str(self.price)}

    @classmethod
    def from_json(cls, dumped: Dict[str, str]):

        return cls(dumped["position"], Decimal(dumped["price"]))
