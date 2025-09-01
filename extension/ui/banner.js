// Simple UI helper for creating and inserting a banner.  This function
// can be imported by other scripts within the extension if desired.
export function renderBanner(title, reasons = []) {
  const bar = document.createElement("div");
  bar.className = "banner";
  bar.innerHTML = `
    <strong>${title}</strong>
    <span id="banner-reasons">${reasons.join(" · ")}</span>
    <button id="banner-dismiss">Dismiss</button>
  `;
  document.documentElement.appendChild(bar);
  document.getElementById("banner-dismiss").onclick = () => bar.remove();
}