# Anti-Phishing Guard Project

This repository contains a sample implementation of a phishing‑detection system suitable for a computer science graduation project.  It includes:

- A **Chrome extension** (`extension/`) built with Manifest V3 that analyzes the current webpage, extracts light‑weight DOM features, and requests risk scores from a backend API.  When a risk is detected, it overlays a warning banner on the page.
- A **gateway API** (`api/gateway/`) implemented with Node.js and Express.  It proxies score requests from the browser extension to the inference service and serves declarative Net Request (DNR) rules used by the extension.
- An **inference service** (`api/inference/`) implemented with Python and FastAPI that computes phishing scores from URL and DOM features.  The service includes a simple baseline model and can be extended with more sophisticated models (e.g. LightGBM).
- A **snapshot worker** (`pipeline/snapshot/`) using Playwright to capture HTML and screenshots of pages for offline analysis.
- A **feed ingestion loop** (`pipeline/feeders/`) that pulls data from public feeds such as URLhaus, PhishTank, and Tranco to collect malicious and benign URLs.
- Feature extraction utilities (`pipeline/features/`) for URL, host and DOM features.
- A `docker-compose.yml` file to orchestrate all containers for local development and testing.

## Quick start

To build and start all services in the background:

    docker compose build
    docker compose up -d

Verify that the inference service and gateway are healthy:

    curl http://localhost:8000/health
    curl http://localhost:8080/health

Test the score API:

    curl -X POST http://localhost:8080/v1/score/url \
      -H 'Content-Type: application/json' \
      -d '{"url":"http://example.com","dom_features":{"form_count":0,"hidden_count":0,"input_count":0,"title_len":11}}'

For browser testing, load the `extension/` directory as an unpacked extension in Chrome (navigate to `chrome://extensions`, enable developer mode, and select “Load unpacked”).  When visiting websites, the extension will request a score from the backend and display a banner for suspicious URLs.

For additional analysis and model training, see the Jupyter notebooks in `notebooks/`.

## Directory overview

The repository is organized as follows:

- `extension/` – source code for the Chrome extension.
- `api/gateway/` – Node.js gateway that proxies requests and serves DNR rules.
- `api/inference/` – Python FastAPI service that computes phishing scores.
- `pipeline/feeders/` – scripts and Dockerfile for ingesting threat/intelligence feeds.
- `pipeline/snapshot/` – worker for capturing HTML and screenshots of websites.
- `pipeline/features/` – shared feature extraction modules.
- `data/` – storage for feeds, snapshots, processed datasets and models.
- `notebooks/` – exploratory data analysis and model training notebooks.
- `docker-compose.yml` – configuration to build and run all services together.

## Disclaimer

This code is provided for educational purposes.  It is a prototype and not intended for production use.  Be sure to review the Chrome extension guidelines and API terms of use for any third‑party services you integrate.  Always handle user data responsibly and adhere to local regulations.