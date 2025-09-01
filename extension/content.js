// Content script for the Anti‑Phishing Guard extension.  This script
// executes in the context of each page. It collects some simple
// DOM features and asks the backend for a score.  If the page is
// considered phishing, it displays a banner at the top of the page.

const API_BASE = "http://localhost:8080";

(async function() {
  const url = location.href;
  const forms = document.querySelectorAll("form");
  const inputs = document.querySelectorAll("input");
  const hidden = document.querySelectorAll('input[type="hidden"]');
  const payload = {
    url,
    dom_features: {
      form_count: forms.length,
      input_count: inputs.length,
      hidden_count: hidden.length,
      title_len: (document.title || "").length
    }
  };
  try {
    const res = await fetch(`${API_BASE}/v1/score/url`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload)
    });
    const out = await res.json();
    if (out.label === "phishing") {
      showBanner(`⚠️ 피싱 위험 (${Math.round(out.prob * 100)}%)`, out.reasons);
    }
  } catch (e) {
    console.debug("Failed to get score", e);
  }
})();

function showBanner(title, reasons = []) {
  const bar = document.createElement("div");
  bar.style.position = "fixed";
  bar.style.top = "0";
  bar.style.left = "0";
  bar.style.right = "0";
  bar.style.zIndex = "2147483647";
  bar.style.padding = "10px 16px";
  bar.style.background = "#ffecb3";
  bar.style.borderBottom = "1px solid #f0c36d";
  bar.style.fontFamily = "system-ui, sans-serif";
  bar.innerHTML = `
    <strong>${title}</strong>
    <span style="margin-left:8px; font-size:12px;">
      ${reasons.slice(0, 3).map(r => `<code>${r}</code>`).join(" · ")}
    </span>
    <button id="apg-dismiss" style="float:right">Dismiss</button>
  `;
  document.documentElement.appendChild(bar);
  document.getElementById("apg-dismiss").onclick = () => bar.remove();
}