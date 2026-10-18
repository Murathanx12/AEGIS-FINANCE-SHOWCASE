// Optional browser smoke check. Uses Playwright, or the existing OpenClaw copy.
const path = require('node:path');
const fs = require('node:fs');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(process.env.PLAYWRIGHT_CORE_PATH || path.join(process.env.APPDATA, 'npm/node_modules/openclaw/node_modules/playwright-core'))); }
const target = process.env.SHOWCASE_URL || 'https://aegis-finance-showcase.vercel.app';
(async () => {
  const directory = path.join(__dirname, '../validation');
  fs.mkdirSync(directory, { recursive: true });
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  try {
    for (const [name, width] of [['desktop', 1440], ['mobile', 390]]) {
      const page = await browser.newPage({ viewport: { width, height: 1000 } });
      const errors = [], failed = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('response', response => { if (response.status() >= 400 && response.url().startsWith(target)) failed.push([response.status(), response.url()]); });
      await page.goto(target, { waitUntil: 'networkidle', timeout: 45000 });
      await page.getByRole('heading', {name: 'Research with a record.'}).waitFor();
      if (await page.locator('#result-rows tr').count() !== 5) throw new Error('Missing result rows');
      for (const [button, expected] of [['Question', 'Make the claim testable.'], ['Test', 'Measure the whole experiment.'], ['Retain', 'Keep the useful lessons.'], ['Collect', 'Start with evidence.']]) {
        await page.getByRole('button', {name: button, exact: true}).click();
        await page.getByRole('heading', {name: expected, exact: true}).waitFor();
      }
      const size = await page.evaluate(() => ({viewport: innerWidth, content: document.documentElement.scrollWidth, imagesComplete: [...document.images].every(i => i.complete && i.naturalWidth > 0)}));
      if (size.content > width || !size.imagesComplete || errors.length || failed.length) throw new Error(JSON.stringify({name, size, errors, failed}));
      await page.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; window.scrollTo(0, 0); });
      await page.screenshot({path: path.join(directory, name + '.png')});
      await page.screenshot({path: path.join(directory, name + '-full.png'), fullPage: true});
      await page.goto(new URL('/methodology.html', target).href);
      await page.getByRole('heading', {name: 'Evidence & methodology.'}).waitFor();
      console.log(JSON.stringify({name, size, errors, failed}));
      await page.close();
    }
    const data = await (await fetch(new URL('/data/results.json', target))).text();
    const localData = fs.readFileSync(path.join(__dirname, '../public/data/results.json'), 'utf8');
    // Git normalizes Windows CRLF to LF; preserve all other bytes and values.
    if (data.replace(/\r\n/g, '\n') !== localData.replace(/\r\n/g, '\n')) throw new Error('Deployed snapshot differs from reviewed data');
    const privateProbe = await fetch(new URL('/brain.json', target));
    if (privateProbe.status !== 404) throw new Error('Unexpected brain export route');
    console.log(JSON.stringify({snapshot: 'exact text match, Git line endings normalized', privateExport: privateProbe.status}));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
