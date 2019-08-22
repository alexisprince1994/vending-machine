import click
from ui.printer import fancy_print
import json
from .logger import GLOBAL_LOGGER as logger
from core.vending_machine import VendingMachine
import os

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
STATE_FILE_LOCATION = os.path.join(PROJECT_ROOT, "state.json")

LOG_ERROR = "error"
LOG_SUCCESS = "success"
LOG_HELP = "help"


@click.command
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


@click.command
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


@click.command
def rebuild():
    """
	Destroys the state of the vending machine (if exists) and rebuilds from scratch.
	"""

    destroy()
    start()


@click.command
def add_money():
    """
	Adding money to the existing vending machine. An error message is shown.
	"""

    if not os.path.isfile(STATE_FILE_LOCATION):
        fancy_print(LOG_ERROR, "Please initialize the vending machine first.")

    with open(STATE_FILE_LOCATION) as f:
        loaded = json.load(f)

    machine = VendingMachine.from_json(loaded)
    amount = click.prompt("How much money would you like to add?", default=0.0)
