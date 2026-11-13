// Gumroad product images: a square thumbnail and a wide cover showing both books.
//     node landing/gumroad/render-thumbs.cjs
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const BOOK = path.join(__dirname, '..', '..', 'book');
const OUT = __dirname;
(async () => {
  const b = await chromium.launch();
  const covers = {};
  for (const [key, src] of [['hb', path.join(BOOK, 'colettes-home-bible.html')], ['xm', path.join(BOOK, 'christmas', 'the-christmas-pages.html')]]) {
    const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.6 });
    await p.goto('file://' + src); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1200);
    const f = path.join(OUT, 'cover-' + key + '.png');
    await p.locator('section.page').first().screenshot({ path: f });
    covers[key] = 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
    fs.unlinkSync(f);
    await p.close();
  }
  const css = `
  *{box-sizing:border-box;margin:0}
  body{width:var(--w);height:var(--h);overflow:hidden;font-family:Archivo,Helvetica,Arial,sans-serif;
    background:radial-gradient(ellipse at 50% 30%,#FFFDF8,#F1E9D8 70%,#E7DCC4)}
  .stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:var(--gap);padding-bottom:var(--pb)}
  .bk{width:var(--bw);aspect-ratio:210/297;background-size:cover;border-radius:4px 10px 10px 4px;
    box-shadow:0 40px 60px -20px rgba(30,25,15,.55),0 10px 20px -8px rgba(30,25,15,.4),inset 10px 0 14px -8px rgba(0,0,0,.45)}
  .hb{transform:rotate(-4deg)}
  .xm{transform:rotate(4deg) translateY(var(--drop));position:relative}
  .tag{position:absolute;top:-4%;left:50%;transform:translateX(-50%) rotate(-3deg);white-space:nowrap;background:#9E2A2B;color:#fff;
    font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:var(--tf);padding:.55em 1.1em;border-radius:999px;
    box-shadow:0 0 0 3px #C9A24A inset,0 8px 18px rgba(0,0,0,.3)}
  .foot{position:absolute;left:0;right:0;bottom:var(--fb);text-align:center;color:#1E2420;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:var(--ff)}
  .foot span{color:#9E2A2B}`;
  const page = (vars, foot) => `<!doctype html><html><head><meta charset="utf-8"><style>:root{${vars}}${css}</style></head><body>
    <div class="stage"><div class="bk hb" style="background-image:url(${covers.hb})"></div>
    <div class="bk xm" style="background-image:url(${covers.xm})"><div class="tag">Free until 31 December</div></div></div>
    <div class="foot">${foot}</div></body></html>`;
  const jobs = [
    ['thumbnail-both-books.png', 1200, 1200, '--w:1200px;--h:1200px;--bw:430px;--gap:46px;--pb:130px;--drop:40px;--tf:22px;--ff:30px;--fb:70px', 'Colette&rsquo;s Home Bible <span>+ free Christmas guide</span>'],
    ['cover-both-books.png', 1280, 720, '--w:1280px;--h:720px;--bw:330px;--gap:60px;--pb:60px;--drop:24px;--tf:18px;--ff:22px;--fb:28px', 'Two books &middot; one payment &middot; PDF and EPUB'],
  ];
  for (const [name, w, h, vars, foot] of jobs) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(page(vars, foot)); await p.waitForTimeout(400);
    await p.screenshot({ path: path.join(OUT, name) });
    console.log(name, Math.round(fs.statSync(path.join(OUT, name)).size / 1024) + ' KB');
    await p.close();
  }
  await b.close();
})();
