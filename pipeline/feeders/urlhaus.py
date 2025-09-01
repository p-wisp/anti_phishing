"""
Fetch the URLhaus CSV feed of recent malware URLs.

Documentation: https://urlhaus.abuse.ch/downloads/
"""

import requests


URLHAUS_RECENT_CSV = "https://urlhaus.abuse.ch/downloads/csv_recent/"


def fetch_urlhaus_csv() -> bytes:
    """
    Download the recent URLhaus CSV feed.
    Returns the raw response content (gzip compressed).
    """
    resp = requests.get(URLHAUS_RECENT_CSV, timeout=30)
    resp.raise_for_status()
    return resp.content