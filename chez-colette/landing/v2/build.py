#!/usr/bin/env python3
"""Build the landing page from v2/template.html.

    node v2/render-covers.cjs      # the two flat covers, first
    python3 v2/build.py

Writes two pages, both wired to Gumroad's checkout and both under its
500,000-character custom_html limit:

    landing-v2.html            December: both books, the Christmas strip
    landing-v2-january.html    after the season: the Home Bible alone

The template marks what differs with <!--XMAS-->…<!--/XMAS--> and
<!--JAN-->…<!--/JAN-->; everything else is shared. Fonts and images are
inlined as base64 so the page makes no external request. The two covers go
in once each, as CSS variables, and every book on the page draws from them.
"""
import base64
import pathlib
import re

HERE = pathlib.Path(__file__).parent
LANDING = HERE.parent
ASSETS = HERE / "assets"
FONTS = LANDING.parent / "book" / "epub-build" / "OEBPS" / "fonts"
LIMIT = 500_000

WIN = """<svg class="win" viewBox="0 0 40 40" aria-hidden="true">
      <rect class="glass" x="14" y="15" width="12" height="16"/>
      <path class="frame" d="M14 15a6 6 0 0 1 12 0v16H14z"/>
      <path class="frame" d="M20 13v18M14 22h12"/>
      <rect class="pane" x="20.9" y="22.9" width="4.2" height="7.2"/>
      <g class="shut l"><rect x="7.5" y="13.5" width="6" height="18" rx=".6"/><path class="slat" d="M8.6 16h3.8M8.6 18.5h3.8M8.6 21h3.8M8.6 23.5h3.8M8.6 26h3.8M8.6 28.5h3.8"/></g>
      <g class="shut r"><rect x="26.5" y="13.5" width="6" height="18" rx=".6"/><path class="slat" d="M27.6 16h3.8M27.6 18.5h3.8M27.6 21h3.8M27.6 23.5h3.8M27.6 26h3.8M27.6 28.5h3.8"/></g>
    </svg>"""

TICK = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M5 12.5l4.5 4.5L19 7" stroke="#EBC45C" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def data_uri(path, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode())


def fill(t):
    t = t.replace("{{win}}", WIN).replace("{{winbig}}", WIN).replace("{{tick}}", TICK)
    t = re.sub(r"\{\{font:([\w-]+)\}\}", lambda m: data_uri(FONTS / (m.group(1) + ".woff2"), "font/woff2"), t)
    t = re.sub(r"\{\{img:([\w-]+)\}\}", lambda m: data_uri(ASSETS / (m.group(1) + ".jpg"), "image/jpeg"), t)
    assert "{{" not in t, "an unfilled placeholder survived"
    return t


def edition(t, keep, drop):
    t = re.sub(r"\s*<!--%s-->.*?<!--/%s-->" % (drop, drop), "", t, flags=re.S)
    t = t.replace("<!--%s-->" % keep, "").replace("<!--/%s-->" % keep, "")
    return t


def check(name, s):
    buys = s.count('data-gumroad-action="buy"')
    prices = s.count('data-gumroad-field="price"')
    assert buys >= 4 and prices >= 4, "Gumroad wiring missing in " + name
    assert "<!--" not in re.sub(r"<!-- =+ .*? =+ -->", "", s), "an edition marker survived in " + name
    print("%-26s %7d characters, %d buy buttons, %d price fields%s"
          % (name, len(s), buys, prices, "" if len(s) <= LIMIT else "   *** OVER THE LIMIT ***"))
    assert len(s) <= LIMIT


def main():
    src = (HERE / "template.html").read_text()
    for name, keep, drop in (("landing-v2.html", "XMAS", "JAN"), ("landing-v2-january.html", "JAN", "XMAS")):
        out = fill(edition(src, keep, drop))
        (LANDING / name).write_text(out)
        check(name, out)


if __name__ == "__main__":
    main()
