// Render page 1 of a print edition as an EPUB cover image.
//     node render-cover.cjs <in.html> <out.jpg>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const src = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + src);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1500);
  await p.locator('section.page').first().screenshot({ path: out, type: 'jpeg', quality: 88 });
  await b.close();
  console.log('cover rendered ->', out);
})();
