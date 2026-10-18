// Fresh Chromium checks for the restored public site; no finance or browser-profile access.
const path = require('node:path');
const fs = require('node:fs');
const { chromium } = require(process.env.PLAYWRIGHT_CORE_PATH || path.join(process.env.APPDATA, 'npm/node_modules/openclaw/node_modules/playwright-core'));
const target = (process.env.SHOWCASE_URL || 'https://aegis-finance-showcase.vercel.app').replace(/\/$/, '');
const assets = ['aegis-orbit.svg', 'aegis-pipeline.svg', 'aegis-gauntlet.svg', 'historical-highlights.svg'];
const stages = [['Sensors','World sensors'],['Evidence','Evidence'],['Theory','World state and theory'],['Forecast','Forecasts'],['Decision','Decision'],['Paper action','Paper action'],['Outcome','Outcome'],['Attribution','Attribution'],['Learning','Learning']];
const normalized = text => text.replace(/\r\n/g, '\n');
function assert(ok, message) { if (!ok) throw new Error(message); }
async function inspectReferences(page) {
  return page.evaluate(() => {
    const ids = [...document.querySelectorAll('[id]')].map(node => node.id);
    const missingAria = [...document.querySelectorAll('[aria-labelledby]')].flatMap(node => node.getAttribute('aria-labelledby').split(/\s+/).filter(id => !document.getElementById(id)));
    const missingUrls = [...document.querySelectorAll('svg *')].flatMap(node => [...node.attributes].flatMap(attribute => [...attribute.value.matchAll(/url\(#([^)]+)\)/g)].filter(match => !document.getElementById(match[1])).map(match => match[1])));
    return { duplicateIds: ids.filter((id,index) => ids.indexOf(id) !== index), missingAria, missingUrls, inlineGraphics: document.querySelectorAll('svg[data-motion]').length };
  });
}
(async () => {
  const directory = path.join(__dirname, '../validation');
  fs.mkdirSync(directory, { recursive: true });
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  try {
    for (const [name,width] of [['desktop',1440],['mobile',390]]) {
      const page = await browser.newPage({ viewport: { width, height: 1000 } });
      const errors = [], failed = [], cspErrors = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('response', response => { if (response.status() >= 400 && response.url().startsWith(target)) failed.push([response.status(),response.url()]); });
      page.on('console', event => { if (event.type() === 'error' && /Content Security Policy|Refused to apply|Refused to execute/i.test(event.text())) cspErrors.push(event.text()); });
      await page.goto(target, { waitUntil:'networkidle', timeout:45000 });
      await page.waitForFunction(() => document.querySelectorAll('svg[data-motion]').length === 5);
      assert(await page.locator('#result-rows tr').count() === 3, 'Historical table must account for all three selected examples');
      const highlights = await page.locator('#highlights').innerText();
      assert(highlights.includes('+10.599%') && highlights.includes('307') && highlights.includes('09 October 2026'), 'Historical value/date/selection boundary missing');
      for (const [button,expected] of stages) {
        await page.getByRole('button',{name:button,exact:true}).click();
        assert(await page.locator('#stage-title').innerText() === expected, `${button} did not select its stage`);
        assert((await page.locator('#stage-body').innerText()).length > 30 && (await page.locator('#stage-code').innerText()).length > 5, `${button} details are incomplete`);
      }
      const references = await inspectReferences(page);
      assert(!references.duplicateIds.length && !references.missingAria.length && !references.missingUrls.length, JSON.stringify(references));
      await page.waitForTimeout(1600); // let the one-shot bars reach their recorded widths
      await page.getByRole('button',{name:'Pause motion',exact:true}).click();
      const before = await page.locator('svg[data-motion]').evaluateAll(nodes => nodes.map(node => node.getCurrentTime()));
      await page.waitForTimeout(180);
      const after = await page.locator('svg[data-motion]').evaluateAll(nodes => nodes.map(node => node.getCurrentTime()));
      assert(before.every((time,index) => Math.abs(time-after[index]) < .04), 'Pause did not freeze all SVG SMIL timelines');
      assert(await page.locator('#motion-toggle').getAttribute('aria-pressed') === 'true', 'Pause state not accessible');
      const size = await page.evaluate(() => ({viewport:innerWidth,content:document.documentElement.scrollWidth,imagesComplete:[...document.images].every(image=>image.complete&&image.naturalWidth>0)}));
      assert(size.content <= width && size.imagesComplete && !errors.length && !failed.length && !cspErrors.length, JSON.stringify({name,size,errors,failed,cspErrors}));
      await page.evaluate(() => { document.documentElement.style.scrollBehavior='auto';scrollTo(0,0); });
      await page.waitForFunction(() => Math.abs(scrollY) < 2);
      await page.screenshot({path:path.join(directory,name+'.png')});
      await page.screenshot({path:path.join(directory,name+'-full.png'),fullPage:true});
      await page.getByRole('button',{name:'Resume motion',exact:true}).click();
      await page.goto(new URL('/methodology.html',target).href);
      assert((await page.locator('h1').innerText()).includes('Historical highlights.'), 'Methodology page missing');
      assert((await page.locator('main').innerText()).includes('overlapping holdings cluster'), 'Dependent selected examples not explained');
      console.log(JSON.stringify({name,size,references,stageControls:9,pause:true,errors,cspErrors}));
      await page.close();
    }
    const reduced = await browser.newPage({ viewport:{width:1280,height:1000},reducedMotion:'reduce' });
    await reduced.goto(target);await reduced.waitForFunction(()=>document.querySelectorAll('svg[data-motion]').length===5);
    assert(await reduced.getByRole('button',{name:'Resume motion',exact:true}).isVisible(), 'Reduced motion should start paused');
    const frame = await reduced.evaluate(()=>({visibleComets:[...document.querySelectorAll('animateMotion')].filter(node=>getComputedStyle(node.parentElement).display!=='none').length,incompleteBars:[...document.querySelectorAll('.result-bar')].filter(node=>getComputedStyle(node).transform!=='none').length}));
    assert(!frame.visibleComets && !frame.incompleteBars, 'Reduced-motion frame is not complete: '+JSON.stringify(frame));
    for(const asset of assets){
      await reduced.goto(new URL('/assets/'+asset,target).href);
      const standalone = await reduced.evaluate(()=>({visibleComets:[...document.querySelectorAll('animateMotion')].filter(node=>getComputedStyle(node.parentElement).display!=='none').length,incompleteBars:[...document.querySelectorAll('.result-bar')].filter(node=>getComputedStyle(node).transform!=='none').length}));
      assert(!standalone.visibleComets&&!standalone.incompleteBars, 'Standalone reduced SVG failed: '+asset);
    }
    await reduced.close();
    console.log(JSON.stringify({reducedMotion:'complete HTML and four standalone SVG frames',frame}));
    const response = await fetch(new URL('/data/results.json',target));assert(response.ok,'Snapshot unavailable');const text = await response.text();
    const local = fs.readFileSync(path.join(__dirname,'../public/data/results.json'),'utf8');
    assert(normalized(text)===normalized(local),'Deployed snapshot differs from reviewed data');
    const data=JSON.parse(text);assert(data.last_market_mark==='2026-10-09'&&data.benchmark_comparable_accounts===307&&data.rows.length===3&&data.rows[0].return_pct===10.599&&data.is_live_feed===false,'Historical packet scope differs');
    for(const asset of assets){const downloaded=await fetch(new URL('/assets/'+asset,target));assert(downloaded.ok&&normalized(await downloaded.text())===normalized(fs.readFileSync(path.join(__dirname,'../public/assets',asset),'utf8')),'SVG differs from reviewed asset: '+asset);}
    for(const route of ['/brain.json','/.env.local','/scripts/brand_renderer.py','/backend/data/optimus/paper_accounts/roi_2026-10-10T235231Z.json']){const probe=await fetch(new URL(route,target));assert(probe.status===404,`Private/source probe ${route} returned ${probe.status}`);}
    console.log(JSON.stringify({snapshot:'exact text match, Git line endings normalized',reviewedSvgAssets:4,privateSourceProbes:'four 404s'}));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exit(1)});
