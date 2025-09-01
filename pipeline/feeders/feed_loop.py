"""
Simple feed ingestion loop for Anti‑Phishing Guard.

This script periodically fetches data from several public feeds to collect
phishing and benign URLs.  It writes the raw CSV data into the configured
output directory.  Real implementations should include deduplication,
timestamp handling and error recovery.
"""

import time
import os
from datetime import datetime
from typing import Callable

from urlhaus import fetch_urlhaus_csv
from phishtank import fetch_phishtank_csv
from tranco import fetch_tranco_csv

OUT_DIR = os.environ.get("OUT_DIR", "/data")
os.makedirs(OUT_DIR, exist_ok=True)


def save_feed(name: str, content: bytes) -> None:
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    file_path = os.path.join(OUT_DIR, f"{name}-{ts}.csv")
    with open(file_path, "wb") as f:
        f.write(content)
    print(f"Saved {name} feed to {file_path}")


def poll(feeds: dict[str, Callable[[], bytes]], interval: int) -> None:
    while True:
        for name, fetch_fn in feeds.items():
            try:
                content = fetch_fn()
                save_feed(name, content)
            except Exception as e:
                print(f"Error fetching {name}: {e}")
        time.sleep(interval)


if __name__ == "__main__":
    FEEDS = {
        "urlhaus": fetch_urlhaus_csv,
        "phishtank": fetch_phishtank_csv,
        "tranco": fetch_tranco_csv,
    }
    # Poll every hour
    poll(FEEDS, interval=3600)