"""
Extract simple lexical features from a URL.

These features are purely string based and can be computed very quickly.
"""

from urllib.parse import urlparse
import re

IP_LIKE = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")


def extract_url_features(url: str) -> dict:
    """
    Extract basic features from a URL such as length, number of dots, path depth,
    whether the host appears to be an IP address, etc.

    :param url: full URL
    :returns: dict of feature names to values
    """
    parsed = urlparse(url)
    host = parsed.hostname or ""
    path = parsed.path or "/"
    return {
        "url_len": len(url),
        "host_len": len(host),
        "dot_count": host.count("."),
        "path_depth": path.count("/"),
        "has_ip_host": bool(IP_LIKE.match(host)),
        "has_at": "@" in url,
        "has_port": parsed.port is not None,
    }