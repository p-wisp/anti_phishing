"""
Feature extraction from HTML DOM.

This module defines simple functions for computing features from the DOM,
such as counts of forms, inputs, hidden fields, etc.  These functions mirror
what the content script collects but can be reused in offline processing.
"""

from html.parser import HTMLParser


class SimpleDOMFeatureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.form_count = 0
        self.input_count = 0
        self.hidden_count = 0
        self.in_title = False
        self.title_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "form":
            self.form_count += 1
        if tag == "input":
            self.input_count += 1
            # determine if it's hidden
            for (name, value) in attrs:
                if name == "type" and value.lower() == "hidden":
                    self.hidden_count += 1
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text.append(data)

    @property
    def title_len(self):
        return len("".join(self.title_text).strip())


def extract_dom_features(html: str) -> dict:
    """
    Given raw HTML, compute a few simple DOM features.

    :param html: raw HTML string
    :returns: dict of feature names to values
    """
    parser = SimpleDOMFeatureParser()
    parser.feed(html)
    return {
        "form_count": parser.form_count,
        "input_count": parser.input_count,
        "hidden_count": parser.hidden_count,
        "title_len": parser.title_len,
    }