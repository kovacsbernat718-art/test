#!/usr/bin/env python3
"""Build the reflowable EPUB of The Christmas Pages.

    python3 build-christmas.py          # the print HTML, first
    python3 build-christmas-epub.py     # writes christmas/The-Christmas-Pages.epub

It runs build-epub.py's own machinery on the supplement, with four changes:
its own title, cover and identifier; the December colours of
christmas/epub-noel.css; the cover's note about page numbers kept; and
"page NN of the book" left unlinked, because that page is in the Home Bible,
not in this file.
"""
import importlib.util
import pathlib
import re
import shutil

HERE = pathlib.Path(__file__).parent
DIR = HERE / "christmas"

spec = importlib.util.spec_from_file_location("bookepub", HERE / "build-epub.py")
be = importlib.util.module_from_spec(spec)
spec.loader.exec_module(be)

be.SRC = DIR / "the-christmas-pages.html"
be.SRCDIR = DIR / "epub-src"
be.BUILD = DIR / "epub-build"
be.OUT = DIR / "The-Christmas-Pages.epub"
be.UUID = "urn:uuid:9e2a2b1e-4a38-4c9a-8a24-12322a7f1e6d"
be.TITLE = "The Christmas Pages"
be.SUBTITLE = "A supplement to Colette's Home Bible"
be.PUBDATE = "2026-11-01T00:00:00Z"
be.CHAPTERS = [
    ((1, 1),   "opener",  "The Christmas Pages"),
    ((2, 4),   "begin",   "Before you begin"),
    ((5, 8),   "light",   "Light, and the black window"),
    ((9, 12),  "height",  "The tree, the garland and the wreath"),
    ((13, 15), "texture", "Colour and texture"),
    ((16, 17), "table",   "The table and the window"),
    ((18, 22), "buying",  "What to buy, what not, and putting it away"),
    ((23, 24), "numbers", "The Christmas numbers, and the audit"),
]
be.COVER = be.COVER.replace("Colette's Home Bible - La Belle Maison",
                            "The Christmas Pages - a supplement to Colette's Home Bible")
be.NAV = be.NAV.replace('href="part1.xhtml"', 'href="begin.xhtml"')


def pages_of(src):
    """The supplement's pages; its cover is an ordinary part opener to the EPUB."""
    body = src[src.index("<!-- ============ THE CHRISTMAS PAGES"):]
    pages = re.findall(r'<section class="page.*?</section>', body, re.S)
    return [p.replace("page page--dark part cover-noel", "page page--dark part") for p in pages]


be.pages_of = pages_of

_link = be.link_page_refs
MASK = "\u0002"


def link_page_refs(block, here, home):
    """Leave 'page NN of the book' alone: it points into the Home Bible."""
    block = re.sub(r"([Pp])(age\s+\d+\s+of\s+the\s+book)", lambda m: m.group(1) + MASK + m.group(2), block)
    return _link(block, here, home).replace(MASK, "")


be.link_page_refs = link_page_refs

_opener = be.render_part_opener


def render_part_opener(block, folio, home):
    out = _opener(block, folio, home)
    # the opener is a file of its own here, so its contents links name their files
    out = re.sub(r'href="#pg(\d+)"', lambda m: 'href="%s.xhtml#pg%s"' % (home[int(m.group(1))], m.group(1)), out)
    note = re.search(r'<p class="noel-note">(.*?)</p>', block, re.S)
    if note:
        out = out.replace("</header>", '<p class="part-note">%s</p>\n</header>' % note.group(1).strip())
    return out


be.render_part_opener = render_part_opener


def main():
    be.SRCDIR.mkdir(exist_ok=True)
    css = (HERE / "epub-src" / "style.css").read_text() + (DIR / "epub-noel.css").read_text()
    (be.SRCDIR / "style.css").write_text(css)
    if not (be.SRCDIR / "cover.jpg").exists():
        raise SystemExit("christmas/epub-src/cover.jpg is missing - run render-cover.cjs on the supplement first")
    pages, folios, fonts, nav_rows, page_list, files = be.build()
    be.write_package(fonts, nav_rows, page_list, files)
    opf = be.BUILD / "OEBPS" / "content.opf"
    text = opf.read_text()
    text = re.sub(r"(<dc:description>).*?(</dc:description>)",
                  r"\1The Christmas supplement to Colette's Home Bible: Christmas lights and colour "
                  r"temperature, the tree, garlands and wreaths, hanging without a drill, the "
                  r"r&#233;veillon table, what not to buy, the Christmas numbers and an audit.\2",
                  text, flags=re.S)
    opf.write_text(text)
    out = be.zip_epub()
    print("chapters %d, page markers %d, wrote %s (%.2f MB)"
          % (len(files), len(page_list), out.name, out.stat().st_size / 1024 / 1024))


if __name__ == "__main__":
    main()
