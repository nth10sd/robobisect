"""Test the start.py file."""

import logging

import pytest

from robobisect import start

ROBOBISECT_TEST_LOG = logging.getLogger("start_test")
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("flake8").setLevel(logging.ERROR)


@pytest.mark.slow
def test_main():
    """Test running the main function."""
    start.main()
