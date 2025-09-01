"""
Fetch the Tranco top sites list.

Tranco is a research-oriented ranking of popular domain names resistant to
manipulation (https://tranco-list.eu/).  An API key is required to download
the list; for demonstration we return a minimal CSV with a few example domains.
"""

import csv
import io


def fetch_tranco_csv() -> bytes:
    """
    Return a small dummy CSV containing benign domains.  Replace this with
    logic to fetch from the Tranco API when available.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["rank", "domain"])
    writer.writerow([1, "example.com"])
    writer.writerow([2, "iana.org"])
    writer.writerow([3, "github.com"])
    return output.getvalue().encode("utf-8")