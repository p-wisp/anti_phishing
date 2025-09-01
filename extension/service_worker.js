// Background service worker for the Anti‑Phishing Guard extension.
// It periodically synchronises declarativeNetRequest (DNR) rules from
// the gateway server. When installed or updated, it pulls the block
// list and updates the rules.  This keeps the extension up to date
// without requiring external permissions.

const API_BASE = "http://localhost:8080";

chrome.runtime.onInstalled.addListener(async () => {
  await syncBlockRules();
});

/**
 * Fetch the current block list from the API and apply it via DNR.
 */
async function syncBlockRules() {
  try {
    const res = await fetch(`${API_BASE}/v1/lists/block`);
    const list = await res.json();
    const ruleIds = list.map(r => r.id);
    await chrome.declarativeNetRequest.updateDynamicRules({
      removeRuleIds: ruleIds,
      addRules: list
    });
  } catch (e) {
    console.error("Failed to synchronise block rules", e);
  }
}