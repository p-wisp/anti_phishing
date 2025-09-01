"""
FastAPI inference service for the Anti‑Phishing Guard project.

This service exposes endpoints to score a given URL (and optional DOM features)
as potentially malicious or benign.  For demonstration purposes a simple
heuristic is used.  You can replace the scoring logic with a trained model
by loading the model from the `models/` directory.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from urllib.parse import urlparse

app = FastAPI(title="Anti‑Phishing Guard Inference API")


class ScoreIn(BaseModel):
    """Request body for scoring a URL."""
    url: str = Field(..., description="The full URL to evaluate")
    dom_features: dict | None = Field(
        default=None,
        description="Optional simple DOM features extracted in the client"
    )


class ScoreOut(BaseModel):
    """Response body containing the predicted label and probability."""
    label: str
    prob: float
    reasons: list[str]


@app.get("/health")
def health() -> dict[str, bool]:
    """Health check endpoint used by Docker and load balancers."""
    return {"ok": True}


def simple_score(features: dict) -> tuple[str, float, list[str]]:
    """
    Very naive scoring function based on URL string characteristics.  Each
    condition contributes 0.25 towards the phishing score.

    :param features: extracted features for the URL
    :returns: (label, probability, reasons)
    """
    score = 0.0
    reasons: list[str] = []
    # Penalize long URLs
    if features.get("url_len", 0) > 120:
        score += 0.25
        reasons.append(f"url_len={features['url_len']}")
    # Penalize many subdomains
    if features.get("dot_count", 0) >= 3:
        score += 0.25
        reasons.append(f"dot_count={features['dot_count']}")
    # Penalize deep paths
    if features.get("path_depth", 0) >= 4:
        score += 0.25
        reasons.append(f"path_depth={features['path_depth']}")
    # Penalize IP in hostname
    if features.get("has_ip_host"):
        score += 0.25
        reasons.append("has_ip_host=True")
    # Penalize many hidden fields in the DOM
    if features.get("dom_hidden_count", 0) >= 5:
        score += 0.1
        reasons.append(f"hidden_count={features.get('dom_hidden_count')}")
    label = "phishing" if score >= 0.5 else "benign"
    return label, min(score, 1.0), reasons


@app.post("/v1/score/url", response_model=ScoreOut)
def score_url(inp: ScoreIn) -> ScoreOut:
    """
    Score a URL using simple heuristics.  Returns a label, probability and
    list of reasons.  DOM features can optionally refine the score.
    """
    u = urlparse(inp.url)
    host = u.hostname or ""
    path = u.path or "/"
    features: dict[str, float | int | bool] = {
        "url_len": len(inp.url),
        "dot_count": host.count("."),
        "path_depth": path.count("/"),
        "has_ip_host": host.replace(".", "").isdigit(),
    }
    # merge DOM features if provided
    if inp.dom_features:
        for k, v in inp.dom_features.items():
            features[f"dom_{k}"] = v
    label, prob, reasons = simple_score(features)
    return ScoreOut(label=label, prob=prob, reasons=reasons)


@app.post("/v1/score/html", response_model=ScoreOut)
def score_html(html: str) -> ScoreOut:
    """
    (Optional) Score raw HTML.  For now this endpoint simply returns benign.
    Future implementations can parse the HTML to extract richer features.
    """
    return ScoreOut(label="benign", prob=0.0, reasons=["html_scoring_not_implemented"])