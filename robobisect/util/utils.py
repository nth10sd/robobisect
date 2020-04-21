"""Place utility functions here."""

import logging
from pathlib import Path

RUN_LOG = logging.getLogger("run_log")
logging.basicConfig(
    format="%(asctime)s %(name)-8s %(levelname)-8s {%(module)s} [%(funcName)s] %(message)s",
    datefmt="%m-%d %H:%M:%S", level=logging.INFO,
)
logging.getLogger("flake8").setLevel(logging.ERROR)


def mk_webkit_cache(base):
    """Create a cache dir for compiled WebKit shells if it has not already been done.
    Args:
        base (Path): Base dir for cache dir
    Returns:
        Path: Returns the full wk-cache path
    """
    if not base:
        base = Path.home()
    webkit_cache = base / "wk-cache"
    webkit_cache.mkdir(exist_ok=True)
    return webkit_cache
