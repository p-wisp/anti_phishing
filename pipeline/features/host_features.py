"""
Feature extraction from domain and hosting information.

Real implementations should query RDAP (WHOIS replacement), TLS certificate
metadata or DNS to compute features such as domain age, registrar reputation,
and certificate validity.  This module provides placeholders for demonstration.
"""

from urllib.parse import urlparse


def extract_host_features(url: str) -> dict:
    """
    Extract simple host-level features from a URL.

    :param url: full URL
    :returns: dict of feature names to numeric or boolean values
    """
    parsed = urlparse(url)
    host = parsed.hostname or ""
    features = {
        "host_len": len(host),
        "subdomain_count": host.count("."),
        "has_port": parsed.port is not None,
    }
    return features