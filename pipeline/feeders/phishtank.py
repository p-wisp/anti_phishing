"""
Fetch the PhishTank data dump.

PhishTank provides a downloadable dump of known phishing sites in CSV format.
See https://phishtank.org/developer_info.php for API details.
"""

import requests


PHISHTANK_DUMP = "https://data.phishtank.com/data/online-valid.csv.gz"


def fetch_phishtank_csv() -> bytes:
    """
    Download the PhishTank online-valid CSV feed (gzipped).
    Returns the raw response content.
    """
    resp = requests.get(PHISHTANK_DUMP, timeout=30)
    resp.raise_for_status()
    return resp.content