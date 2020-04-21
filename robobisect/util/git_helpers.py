"""Place helper functions related to Git here."""

from robobisect.util.utils import RUN_LOG


def broken_range(start_bad, start_good):
    """Create a cache dir for compiled WebKit shells if it has not already been done.
    Args:
        start_bad (str): First revision that shows the symptom
        start_good (str): First revision that no longer shows the symptom
    Returns:
        str: Returns the string representing the |git bisect skip| range
    """
    RUN_LOG.debug("start_bad is: %s", start_bad)
    RUN_LOG.debug("start_good is: %s", start_good)
    return f"{start_bad} {start_bad}..{start_good}^"
