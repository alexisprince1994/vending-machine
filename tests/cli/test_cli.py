from click.testing import CliRunner
import pytest
import os
from vending_machine import STATE_FILE_LOCATION
from vending_machine.__main__ import (
    start,
    destroy,
    view_items,
    view_balance,
    view_purchases,
    add_money,
    dispense_change,
)


class BaseHasExitCode0:

    pass


@pytest.fixture
def reset_state():

    if os.path.isfile(STATE_FILE_LOCATION):
        os.remove(STATE_FILE_LOCATION)

    yield None

    if os.path.isfile(STATE_FILE_LOCATION):
        os.remove(STATE_FILE_LOCATION)


@pytest.fixture
def runner():

    return CliRunner()


def test_start_creates_statefile(runner, reset_state, caplog):
    """
    Test case ensuring the start command will create a new json state
    file if one doesn't exist yet.
    """
    assert not os.path.isfile(STATE_FILE_LOCATION)
    result = runner.invoke(start)
    assert result.exit_code == 0
    assert "SUCCESS" in caplog.text
    assert os.path.isfile(STATE_FILE_LOCATION)


def test_start_does_nothing_if_existing(runner, reset_state, caplog):
    """
    Test case ensuring that start has "create if not exists" style
    behavior.
    """

    assert not os.path.isfile(STATE_FILE_LOCATION)
    result = runner.invoke(start)
    assert result.exit_code == 0
    assert "SUCCESS" in caplog.text
    assert os.path.isfile(STATE_FILE_LOCATION)

    result = runner.invoke(start)
    assert result.exit_code == 0
    assert "INFO" in caplog.text
    assert os.path.isfile(STATE_FILE_LOCATION)


def test_destroy_destroys_statefile(runner, reset_state, caplog):
    """
    Test case ensuring that the destroy command will destroy an
    existing state file (if it exists).
    """

    result = runner.invoke(start)
    assert os.path.isfile(STATE_FILE_LOCATION)
    result = runner.invoke(destroy)
    assert result.exit_code == 0
    assert "SUCCESS" in caplog.text

    assert not os.path.isfile(STATE_FILE_LOCATION)


def test_destroy_does_nothing_if_no_statefile(runner, reset_state, caplog):
    """
    Tests to make sure that the destroy command
    can run without the program erroring out, even if
    there isn't an existing state file
    """
    assert not os.path.isfile(STATE_FILE_LOCATION)
    result = runner.invoke(destroy)
    assert result.exit_code == 0
    assert not os.path.isfile(STATE_FILE_LOCATION)
    assert "INFO" in caplog.text
    assert "doing nothing" in caplog.text.lower()


def test_view_items_prints_messages_from_row_and_column(runner, reset_state, caplog):
    """
    Tests to make sure the view items command prints out the
    correct number of messages to the console if given
    a specific position
    """

    result = runner.invoke(start)
    assert result.exit_code == 0
    caplog.clear()
    result = runner.invoke(view_items, ["-c", "A", "-r", 1])
    assert len(caplog.records) == 1
    assert result.exit_code == 0


def test_view_items_prints_messages_from_position(runner, reset_state, caplog):
    """
    Tests to make sure the view items command prints out the
    correct number of messages to the console if given
    a specific position
    """

    result = runner.invoke(start)
    assert result.exit_code == 0
    caplog.clear()
    result = runner.invoke(view_items, ["-p", "A1"])
    assert len(caplog.records) == 1
    assert result.exit_code == 0


def test_deposit_money(runner, reset_state, caplog):
    """
    Test case ensures you're able to deposit money via CLI
    """

    result = runner.invoke(start)
    assert result.exit_code == 0
    caplog.clear()

    result = runner.invoke(add_money, ["10"])

    assert len(caplog.records) == 1
    assert result.exit_code == 0
    assert "10" in caplog.text


def test_view_balance(runner, reset_state, caplog):
    """
    Test case ensures that the sum of money deposited
    is viewable.
    """
    result = runner.invoke(start)
    caplog.clear()
    result = runner.invoke(add_money, ["10"])
    caplog.clear()

    result = runner.invoke(view_balance)
    assert result.exit_code == 0
    assert len(caplog.records) == 1
    assert "10" in caplog.text


def test_dispense_change(runner, reset_state, caplog):
    """
    Test case ensures that you're able to get change
    from the machine and it resets the balance to 0
    """

    result = runner.invoke(start)
    caplog.clear()
    result = runner.invoke(add_money, ["10"])
    caplog.clear()
    result = runner.invoke(view_balance)
    assert "10" in caplog.text
    caplog.clear()

    result = runner.invoke(dispense_change)
    assert result.exit_code == 0
    assert len(caplog.records) == 1
    assert "10.00" in caplog.text
    caplog.clear()

    result = runner.invoke(dispense_change)
    assert result.exit_code == 0
    assert len(caplog.records) == 1
    assert "0.00" in caplog.text
