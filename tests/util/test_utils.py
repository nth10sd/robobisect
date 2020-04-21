"""Test the utils.py file."""

import logging
from pathlib import Path

from robobisect.util import utils

ROBOBISECT_TEST_LOG = logging.getLogger("utils_test")
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("flake8").setLevel(logging.ERROR)


def test_mk_webkit_cache(tmpdir):
    """Test running mk_webkit_cache.

    Args:
        tmpdir (class): Fixture from pytest for creating a temporary directory
    """
    tmpdir = Path(tmpdir)
    utils.mk_webkit_cache(tmpdir)
    assert (tmpdir / "wk-cache").is_dir()
