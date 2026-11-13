// Flat cover renders for the landing's CSS books, at twice their display width.
//     node v2/render-covers.cjs
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const BOOK = path.join(__dirname, '..', '..', 'book');
(async () => {
  const b = await chromium.launch();
  for (const [src, out, q] of [
    [path.join(BOOK, 'colettes-home-bible.html'), 'cover-home-bible.jpg', 80],
    [path.join(BOOK, 'christmas', 'the-christmas-pages.html'), 'cover-christmas.jpg', 68],
  ]) {
    const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 520 / 794 });
    await p.goto('file://' + src);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(1200);
    const file = path.join(__dirname, 'assets', out);
    await p.locator('section.page').first().screenshot({ path: file, type: 'jpeg', quality: q });
    console.log(out, Math.round(fs.statSync(file).size / 1024) + ' KB');
    await p.close();
  }
  await b.close();
})();
