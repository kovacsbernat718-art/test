// Render the print edition to the PDF: A4, backgrounds on, fonts embedded.
//     node render-pdf.cjs                       the Home Bible
//     node render-pdf.cjs <in.html> <out.pdf>   any other edition, e.g. the Christmas pages
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const src = process.argv[2] ? path.resolve(process.argv[2]) : path.join(__dirname, 'colettes-home-bible.html');
  const out = process.argv[3] ? path.resolve(process.argv[3]) : path.join(__dirname, 'Colettes-Home-Bible.pdf');
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + src);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(2000);
  await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  await b.close();
  console.log('pdf ->', out);
})();
