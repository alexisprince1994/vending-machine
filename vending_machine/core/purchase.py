from typing import Dict, Any
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

    def to_json(self) -> Dict[str, Any]:
        """
        Dumps the purchase object to a json serializable dictionary
        that can be converted back into a Purchase object via
        Purchase.from_json(purchase.to_json())
        :return:
        """

        return {"position": self.position, "price": str(self.price)}

    @classmethod
    def from_json(cls, dumped: Dict[str, str]):
        """
        Loads the purchase object from a json serializable dictionary
        that could have been generated from a Purchase object via
        purchase.to_json()
        """

        return cls(dumped["position"], Decimal(dumped["price"]))
