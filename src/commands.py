""" CLI Utility Commands """

import os
from glob import glob
import subprocess

import click

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
@click.option("--verbose", default=True)
def test(verbose: bool):
    """ Runs the test suite """
    import pytest

    args = [TEST_PATH]

    if verbose:
        args.append("--verbose")

    rv = pytest.main(args)
    exit(rv)


if __name__ == "__main__":
    test()
