"""Test the utils.py file."""

import logging

from robobisect.util import utils

ROBOBISECT_TEST_LOG = logging.getLogger("utils_test")
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("flake8").setLevel(logging.ERROR)


def test_test_util_function():
    """Test running test_util_function."""
    utils.test_util_function()
