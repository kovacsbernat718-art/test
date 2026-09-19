// Render page 1 of the print edition as the EPUB cover image.
import { chromium } from 'playwright';
const out = process.argv[2] || 'epub-build/OEBPS/images/cover.jpg';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
await p.goto('file:///home/user/test/chez-colette/book/colettes-home-bible.html');
await p.waitForTimeout(4500);
await p.evaluate(() => document.fonts.ready);
await p.locator('section.page').first().screenshot({ path: out, type: 'jpeg', quality: 88 });
await b.close();
console.log('cover rendered ->', out);
