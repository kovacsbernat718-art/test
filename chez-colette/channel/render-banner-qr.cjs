// YouTube channel banner (2048x1152) with the book and a QR code to the landing page.
// Everything that matters sits inside YouTube's 1235x338 safe area, so it shows on
// phones, desktops and TVs alike.
//     NODE_PATH=<dir with qrcode, jsqr, pngjs> node channel/render-banner-qr.cjs
const { chromium } = require('playwright');
const QRCode = require('qrcode');
const jsQR = require('jsqr');
const { PNG } = require('pngjs');
const path = require('path');
const fs = require('fs');
const URL = 'https://www.colette-dubois.com';
const BOOK = path.join(__dirname, '..', 'book', 'colettes-home-bible.html');
const FONTS = path.join(__dirname, '..', 'book', 'epub-build', 'OEBPS', 'fonts');
const ARCHIVO800 = path.join(__dirname, '..', 'landing', 'v2', 'assets', 'archivo-800.woff2');
const font = f => 'data:font/woff2;base64,' + fs.readFileSync(f).toString('base64');
(async () => {
  const b = await chromium.launch();
  let p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.2 });
  await p.goto('file://' + BOOK); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1200);
  const cover = 'data:image/png;base64,' + (await p.locator('section.page').first().screenshot()).toString('base64');
  await p.close();
  const qr = await QRCode.toString(URL, { type: 'svg', errorCorrectionLevel: 'M', margin: 0, color: { dark: '#1E2420', light: '#FFFFFF' } });
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face{font-family:Bodoni;font-weight:400;src:url(${font(path.join(FONTS, 'bodoni-400.woff2'))})}
  @font-face{font-family:Bodoni;font-weight:400;font-style:italic;src:url(${font(path.join(FONTS, 'bodoni-400i.woff2'))})}
  @font-face{font-family:Archivo;font-weight:600;src:url(${font(path.join(FONTS, 'archivo-600.woff2'))})}
  @font-face{font-family:Archivo;font-weight:800;src:url(${font(ARCHIVO800)})}
  *{box-sizing:border-box;margin:0}
  body{width:2048px;height:1152px;overflow:hidden;position:relative;
    background:radial-gradient(ellipse at 30% 45%,#FFFDF8 0,#F5EEDF 45%,#E9DEC7 100%);
    font-family:Archivo,Helvetica,sans-serif;color:#1E2420}
  body::before{content:"";position:absolute;inset:0;
    background:repeating-linear-gradient(0deg,rgba(30,36,32,.035) 0 1px,transparent 1px 32px),
               repeating-linear-gradient(90deg,rgba(30,36,32,.035) 0 1px,transparent 1px 32px)}
  .rays{position:absolute;inset:0;background:repeating-linear-gradient(115deg,rgba(201,150,43,.05) 0 60px,transparent 60px 150px)}
  .safe{position:absolute;left:406px;top:407px;width:1235px;height:338px;display:flex;align-items:center;gap:40px;padding:0 6px 0 24px}
  .txt{flex:1;min-width:0}
  .kick{font-weight:800;font-size:17px;letter-spacing:.32em;text-transform:uppercase;color:#245841;margin-bottom:14px}
  h1{font-family:Bodoni;font-weight:400;font-size:60px;line-height:1.04;letter-spacing:-.01em}
  h1 em{color:#A8701B}
  .sub{margin-top:20px;font-weight:600;font-size:22px;color:#4A524C;letter-spacing:.01em}
  .book{flex:none;width:214px;aspect-ratio:210/297;background:url(${cover}) center/cover;border-radius:3px 7px 7px 3px;transform:rotate(-3deg);
    box-shadow:0 30px 44px -16px rgba(30,25,15,.6),0 8px 16px -6px rgba(30,25,15,.4),inset 8px 0 10px -6px rgba(0,0,0,.5)}
  .card{flex:none;width:262px;height:326px;background:#fff;border-radius:16px;padding:20px 22px 16px;text-align:center;
    box-shadow:0 0 0 3px #C9962B,0 24px 40px -18px rgba(30,25,15,.55)}
  .card .scan{font-weight:800;font-size:15px;letter-spacing:.2em;text-transform:uppercase;color:#1E2420}
  .card .qr{width:206px;height:206px;margin:12px auto 10px}
  .card .qr svg{width:100%;height:100%;display:block}
  .card .url{font-weight:800;font-size:17px;color:#245841;letter-spacing:.01em}
  </style></head><body><div class="rays"></div>
  <div class="safe">
    <div class="txt"><p class="kick">Chez Colette &middot; French interiors</p>
      <h1>We do not decorate a room. <em>We correct it.</em></h1>
      <p class="sub">Every rule and measurement in one book: Colette&rsquo;s Home Bible</p></div>
    <div class="book"></div>
    <div class="card"><p class="scan">Scan for the book</p><div class="qr">${qr}</div><p class="url">colette-dubois.com</p></div>
  </div></body></html>`;
  p = await b.newPage({ viewport: { width: 2048, height: 1152 } });
  await p.setContent(html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  const out = path.join(__dirname, 'channel-banner-qr-2048x1152.png');
  await p.screenshot({ path: out });
  // the same banner with the safe area outlined, for checking only
  await p.addStyleTag({ content: '.safe{outline:4px dashed #E0245E;outline-offset:0}' });
  await p.screenshot({ path: path.join(__dirname, 'channel-banner-qr-SAFE-AREA-GUIDE.png') });
  await b.close();
  const png = PNG.sync.read(fs.readFileSync(out));
  const code = jsQR(new Uint8ClampedArray(png.data), png.width, png.height);
  console.log('decoded:', code ? code.data : 'NOT READABLE', '| size', Math.round(fs.statSync(out).size / 1024), 'KB');
  if (!code || code.data !== URL) process.exit(1);
})();
