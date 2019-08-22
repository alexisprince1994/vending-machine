class InsufficientFundsError(Exception):
    """
	This exception should get thrown when someone tries to purchase an item
	when they don't have the appropriate balance.
	"""

    pass


class OutOfStockError(Exception):
    """
	This exception should get thrown when someone tries to purchase an item
	and the vending machine has run out of stock.
	"""

    pass


class InvalidLocationError(Exception):
    """
	This exception should get thrown when someone enters an invalid combination
	of row and column coordinates for the vending machine.
	Ex: If the machine has A1 through C5, and they put F13, this exception
	would get raised.
	"""

    pass
