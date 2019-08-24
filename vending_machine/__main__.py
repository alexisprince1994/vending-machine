"""
Top level CLI script that allows the vending_machine
module to actually be executed. Most code here
is very basic, with a lot of the heavy lifting
being done by vending_machine/core
"""

import json
import os
from decimal import Decimal

import click

from vending_machine.core.vending_machine import VendingMachine
from vending_machine.ui.printer import fancy_print
from . import STATE_FILE_LOCATION

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
    with open(STATE_FILE_LOCATION, "w") as file:
        json.dump(machine.to_json(), file)

    fancy_print(LOG_SUCCESS, "Vending machine created.")

    return None


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
    "-c", "--column", "column", type=str, help="Inspects all items in the column"
)
@click.option("-r", "--row", "row", type=int, help="Inspects all items in the row")
@click.option(
    "-p", "--position", type=str, help="View one specific item on the machine."
)
def view_items(column: str = None, row: int = None, position: str = None):
    """
    Viewing what items are in the machine. Filters are additive.
    """

    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")
        return None

    with open(STATE_FILE_LOCATION) as file:
        loaded = json.load(file)

    machine = VendingMachine.from_json(loaded)
    if position:
        machine.view_items(position[0], position[1])
    else:
        machine.view_items(column, row)

    return None


@cli.command()
@click.argument("amount", type=float)
def add_money(amount: float):
    """
    Adding money to the existing vending machine. If no machine exists, error is thrown.
    """

    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")
        return None

    with open(STATE_FILE_LOCATION) as file:
        loaded = json.load(file)

    machine = VendingMachine.from_json(loaded)
    machine.deposit(Decimal(amount))

    with open(STATE_FILE_LOCATION, "w") as file:
        json.dump(machine.to_json(), file)

    return None


@cli.command()
def view_balance():
    """
    Views the current balance you have in the machine. If no machine exists, error is thrown.
    """

    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")
        return None

    with open(STATE_FILE_LOCATION) as file:
        loaded = json.load(file)

    machine = VendingMachine.from_json(loaded)
    fancy_print(LOG_SUCCESS, f"Your current balance is {machine.balance}.")

    return None


@cli.command()
def view_purchases():
    """
    Views all purchases. If no machine exists, error is thrown.
    """
    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")
        return None

    with open(STATE_FILE_LOCATION) as file:
        loaded = json.load(file)

    machine = VendingMachine.from_json(loaded)
    machine.view_purchases()

    return None


@cli.command()
def dispense_change():
    """
    Removing the money from the existing vending machine. If no machine exists, error is thrown.
    """

    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")
        return None

    with open(STATE_FILE_LOCATION) as file:
        loaded = json.load(file)

    machine = VendingMachine.from_json(loaded)
    machine.dispense_change()

    with open(STATE_FILE_LOCATION, "w") as file:
        json.dump(machine.to_json(), file)

    return None


if __name__ == "__main__":
    cli()
