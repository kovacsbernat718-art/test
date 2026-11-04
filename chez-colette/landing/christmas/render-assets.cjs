// Render the two book covers small enough to embed in the landing page, and
// the Gumroad product images that show both books together.
//     node christmas/render-assets.cjs
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const BOOK = path.join(__dirname, '..', '..', 'book');
const OUT = __dirname;
(async () => {
  const b = await chromium.launch();
  async function cover(src, out, scale) {
    const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: scale });
    await p.goto('file://' + src);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(1200);
    await p.locator('section.page').first().screenshot({ path: out, type: 'jpeg', quality: 84 });
    await p.close();
  }
  await cover(path.join(BOOK, 'christmas', 'the-christmas-pages.html'), path.join(OUT, 'cover-christmas-small.jpg'), 0.62);
  await cover(path.join(BOOK, 'christmas', 'the-christmas-pages.html'), path.join(OUT, 'cover-christmas.jpg'), 1.4);
  await cover(path.join(BOOK, 'colettes-home-bible.html'), path.join(OUT, 'cover-home-bible.jpg'), 1.4);

  // product images: both books, standing side by side
  const uri = f => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(OUT, f)).toString('base64');
  const html = (w, h) => `<!doctype html><html><head><style>
    html,body{margin:0;width:${w}px;height:${h}px;overflow:hidden}
    body{display:flex;align-items:center;justify-content:center;gap:${Math.round(w*0.045)}px;
      background:radial-gradient(ellipse at 50% 40%,#2B2A22 0%,#16150F 70%)}
    .book{position:relative;height:${Math.round(h*0.74)}px;aspect-ratio:210/297;border-radius:2px 5px 5px 2px;
      background-size:cover;box-shadow:0 30px 60px -20px rgba(0,0,0,.85),0 8px 18px rgba(0,0,0,.45)}
    .book::before{content:"";position:absolute;inset:0 auto 0 0;width:5%;border-radius:2px 0 0 2px;
      background:linear-gradient(90deg,rgba(0,0,0,.45),rgba(255,255,255,.10) 55%,rgba(0,0,0,.18))}
    .book::after{content:"";position:absolute;inset:0;border-radius:inherit;
      background:linear-gradient(115deg,rgba(255,255,255,.10),transparent 38%)}
    .hb{background-image:url(${uri('cover-home-bible.jpg')})}
    .xm{background-image:url(${uri('cover-christmas.jpg')})}
  </style></head><body><div class="book hb"></div><div class="book xm"></div></body></html>`;
  for (const [w, h, name] of [[1280, 720, 'gumroad-cover-both-books.jpg'], [600, 600, 'gumroad-thumbnail-both-books.jpg']]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(html(w, h));
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(OUT, name), type: 'jpeg', quality: 88 });
    await p.close();
  }
  await b.close();
  for (const f of fs.readdirSync(OUT).filter(f => f.endsWith('.jpg')))
    console.log(f, Math.round(fs.statSync(path.join(OUT, f)).size / 1024) + ' KB');
})();
