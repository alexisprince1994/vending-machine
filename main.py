import click
from src.ui.printer import fancy_print
import json
from src.logger import GLOBAL_LOGGER as logger
from src.core.vending_machine import VendingMachine
import os
from decimal import Decimal

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
STATE_FILE_LOCATION = os.path.join(PROJECT_ROOT, "state.json")

LOG_ERROR = "error"
LOG_SUCCESS = "success"
LOG_HELP = "info"


@click.group()
def cli():
    """A simple command line tool"""


@cli.command()
def start():
    """
    Initiates the state of the vending machine. If there's an existing
    vending machine, and start is called again, the existing state is
    not touched.
    """

    if os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(
            LOG_HELP, "An existing vending machine exists. Proceeding with that."
        )
        return None

    machine = VendingMachine()
    with open(STATE_FILE_LOCATION, "w") as f:
        json.dump(machine.to_json(), f)

    fancy_print(LOG_SUCCESS, "Vending machine created.")


@cli.command()
def destroy():
    """
    Destroys the state of the vending machine without rebuilding a new one.
    If no existing machine exists, nothing happens.
    """
    if os.path.isfile(STATE_FILE_LOCATION):
        os.remove(STATE_FILE_LOCATION)
        fancy_print(LOG_SUCCESS, "Vending machine destroyed.")
    else:
        fancy_print(LOG_HELP, "No vending machine found. Doing nothing.")


@cli.command()
def rebuild():
    """
    Destroys the vending machine (if exists) and rebuilds from scratch.
    """

    pass


@cli.command()
@click.option(
    "-c", "--column", "column", type=int, help="Inspects all items in the column"
)
@click.option("-r", "--row", "row", type=int, help="Inspects all items in the row")
def view_items(column: int = None, row: int = None):
    """
    Viewing what items are in the machine. Filters are additive.
    """

    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")
        return None

    with open(STATE_FILE_LOCATION) as f:
        loaded = json.load(f)

    machine = VendingMachine.from_json(loaded)
    machine.view_items(column, row)


@cli.command()
@click.argument('amount', type=float)
def add_money(amount: float):
    """
    Adding money to the existing vending machine. If no machine exists, error is thrown.
    """

    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")
        return None

    with open(STATE_FILE_LOCATION) as f:
        loaded = json.load(f)

    machine = VendingMachine.from_json(loaded)
    machine.deposit(Decimal(amount))

    with open(STATE_FILE_LOCATION, 'w') as f:
        json.dump(machine.to_json(), f)

@cli.command()
def view_balance():
    """
    Views the current balance you have in the machine. If no machine exists, error is thrown.
    """

    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")
        return None

    with open(STATE_FILE_LOCATION) as f:
        loaded = json.load(f)

    machine = VendingMachine.from_json(loaded)
    fancy_print(LOG_SUCCESS, f"Your current balance is {machine.balance}.")
    

@cli.command()
def dispense_change():
    """
    Removing the money from the existing vending machine. If no machine exists, error is thrown.
    """

    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")
        return None

    with open(STATE_FILE_LOCATION) as f:
        loaded = json.load(f)

    machine = VendingMachine.from_json(loaded)
    machine.dispense_change()

    with open(STATE_FILE_LOCATION, 'w') as f:
        json.dump(machine.to_json(), f)

if __name__ == "__main__":
    cli()
