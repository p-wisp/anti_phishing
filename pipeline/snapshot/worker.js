import { chromium } from "playwright";
import fs from "fs/promises";

/**
 * Capture a snapshot of a URL and save the HTML and a full-page PNG screenshot.
 * The output directory is controlled by the OUTPUT_DIR environment variable.
 */

async function capture(url) {
  const outDir = process.env.OUTPUT_DIR || "/srv/out";
  await fs.mkdir(outDir, { recursive: true });
  const ts = Date.now();
  const baseName = `${outDir}/${ts}`;

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });

  // Save HTML
  const html = await page.content();
  await fs.writeFile(`${baseName}.html`, html, "utf-8");
  // Save screenshot
  await page.screenshot({ path: `${baseName}.png`, fullPage: true });

  await browser.close();
  console.log(JSON.stringify({ url, html: `${baseName}.html`, image: `${baseName}.png` }));
}

// Accept URL from CLI arguments
const url = process.argv[2] || "https://example.com";
capture(url).catch(err => {
  console.error(err);
  process.exit(1);
});