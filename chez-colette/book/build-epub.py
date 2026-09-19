#!/usr/bin/env python3
"""Build the reflowable EPUB 3 edition from the print edition.

    python3 build-epub.py

The print edition is 204 fixed A4 pages; an EPUB has no pages at all, so the
conversion does three things that matter:

  * drops the page box, the running heads and the folios, and lets the text flow;
  * keeps every print page number as an EPUB 3 pagebreak marker, listed in the
    navigation document, so a reader can still "go to page 145" and land where
    the PDF does;
  * turns all ~200 "page NN" cross-references into live links to those markers.
"""
import base64
import html as htmllib
import pathlib
import re
import shutil
import zipfile

HERE = pathlib.Path(__file__).parent
SRC = HERE / "colettes-home-bible.html"
SRCDIR = HERE / "epub-src"
BUILD = HERE / "epub-build"
OUT = HERE / "Colettes-Home-Bible.epub"

UUID = "urn:uuid:4c1d9f3a-7b82-4e65-9d0c-1f6a5b3e8d47"
TITLE = "Colette's Home Bible"
SUBTITLE = "La Belle Maison - Make Any Room Look Expensive Without Buying Anything New"
AUTHOR = "Colette Dubois"
PUBLISHER = "Chez Colette"
LANG = "en-GB"
PUBDATE = "2026-01-01T00:00:00Z"

# page ranges -> (file stem, nav title)
CHAPTERS = [
    ((2, 2),     "titlepage", "Title page"),
    ((3, 3),     "foreword",  "A word from Colette"),
    ((4, 4),     "contents",  "What is in this book"),
    ((5, 20),    "part1",     "Part One - How to Read a Room"),
    ((21, 44),   "part2",     "Part Two - Light"),
    ((45, 84),   "part3",     "Part Three - Colour"),
    ((85, 104),  "part4",     "Part Four - Height and Proportion"),
    ((105, 124), "part5",     "Part Five - Texture and Material"),
    ((125, 144), "part6",     "Part Six - The Rented Room"),
    ((145, 164), "part7",     "Part Seven - Room by Room"),
    ((165, 180), "ref1",      "Reference - The Measurements"),
    ((181, 188), "ref2",      "Reference - The Room Audit"),
    ((189, 196), "ref3",      "Reference - What Not to Buy"),
    ((197, 204), "back",      "Thirty days, and the glossaries"),
]

ENTS = {"nbsp": " ", "mdash": "—", "ndash": "–", "middot": "·",
        "rsquo": "’", "lsquo": "‘", "ldquo": "“", "rdquo": "”",
        "eacute": "é", "egrave": "è", "agrave": "à", "ecirc": "ê",
        "acirc": "â", "ccedil": "ç", "times": "×", "divide": "÷",
        "plusmn": "±", "minus": "−", "thinsp": " ", "hellip": "…"}


def pages_of(src):
    body = src[src.index("<!-- ============ 1. COVER"):]
    return re.findall(r'<section class="page.*?</section>', body, re.S)


def text_of(fragment):
    return " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def to_xhtml_text(s):
    """Named entities to real characters; the files are UTF-8 XHTML."""
    for name, char in ENTS.items():
        s = s.replace("&%s;" % name, char)
    s = s.replace("&amp;", "\u0001AMP\u0001")
    s = s.replace("&", "&amp;").replace("\u0001AMP\u0001", "&amp;")
    return s


def close_voids(s):
    s = re.sub(r"<br\s*>", "<br/>", s)
    s = re.sub(r"<hr\b([^>]*?)/?>", r"<hr\1/>", s)
    s = re.sub(r'<svg(?![^>]*xmlns=)', '<svg xmlns="http://www.w3.org/2000/svg"', s)
    return s


def page_home(folio, index):
    """Which file a print page lives in."""
    for (lo, hi), stem, _ in CHAPTERS:
        if lo <= folio <= hi:
            return stem
    return "cover" if index == 1 else "back"


def link_page_refs(block, here, home):
    """Every 'page 145' becomes a link to that page's marker.

    The whole phrase is linked, not just the digits, so it is a reasonable tap
    target on a phone. Ranges ('pages 183 to 187', 'pages 34 and 36') get both
    ends linked.
    """
    def href_for(n):
        target = home[n]
        return "#pg%d" % n if target == here else "%s.xhtml#pg%d" % (target, n)

    def whole(m):
        word, first, joiner, second = m.group("w"), int(m.group("a")), m.group("j"), m.group("b")
        if first not in home:
            return m.group(0)
        out = '<a href="%s">%s%s</a>' % (href_for(first), word, m.group("a"))
        if second and int(second) in home:
            out += '%s<a href="%s">%s</a>' % (joiner, href_for(int(second)), second)
        elif second:
            out += joiner + second
        return out

    # the negative lookahead keeps the rewrite out of tags and attribute values
    return re.sub(r'(?P<w>[Pp]ages?\s+)(?P<a>\d{1,3})'
                  r'(?:(?P<j>\s+(?:to|and)\s+|\u2013)(?P<b>\d{1,3}))?(?![^<]*?>)',
                  whole, block)


def strip_chrome(block):
    block = re.sub(r'<div class="rh">.*?</div>\s*', "", block, flags=re.S)
    block = re.sub(r'<div class="footer">.*?</div>\s*', "", block, flags=re.S)
    return block


def render_part_opener(block, folio, home):
    label = re.search(r'<p class="part-label">(.*?)</p>', block, re.S)
    title = re.search(r'<h1 class="part-title">(.*?)</h1>', block, re.S)
    blurb = re.search(r'<p class="part-blurb">(.*?)</p>', block, re.S)
    items = re.findall(r"<li>(.*?)</li>", block, re.S)

    out = ['<header class="part-open">']
    if label:
        out.append('<p class="part-label">%s</p>' % label.group(1).strip())
    out.append('<h1>%s</h1>' % re.sub(r"<br\s*/?>", " ", title.group(1)).strip() if title else "<h1></h1>")
    if blurb:
        out.append('<p class="part-blurb">%s</p>' % blurb.group(1).strip())
    if items:
        out.append('<ul class="part-contents">')
        for it in items:
            m = re.search(r"(\d+)\s*$", text_of(it))
            if m and int(m.group(1)) in home:
                n = int(m.group(1))
                label_text = it[: it.rfind("·")] if "·" in it else it
                out.append('<li><a href="#pg%d">%s</a></li>' % (n, it.strip()))
            else:
                out.append("<li>%s</li>" % it.strip())
        out.append("</ul>")
    out.append("</header>")
    return "\n".join(out)


def render_titlepage(block):
    def grab(cls):
        m = re.search(r'<p class="%s">(.*?)</p>' % cls, block, re.S)
        return m.group(1).strip() if m else ""
    title = re.search(r'<h1 class="cover-title">(.*?)</h1>', block, re.S)
    return ('<div class="titlepage">'
            '<h1>%s</h1><p class="fr-title">%s</p>'
            '<p class="sub">%s</p><div class="rule"></div>'
            '<p class="author">%s</p></div>'
            % (re.sub(r"<br\s*/?>", " ", title.group(1)).strip() if title else TITLE,
               grab("cover-fr"), grab("cover-sub").replace("<br>", "<br/>"), grab("cover-author")))


def render_page(block, folio, index, here, home, sections):
    """One print page -> one flowing <section>, with its page marker kept."""
    is_part = 'class="page page--dark part"' in block
    is_work = "page--worksheet" in block
    is_cover_like = "cover-title" in block

    marker = ('<span class="pagebreak" epub:type="pagebreak" role="doc-pagebreak" '
              'id="pg%d" aria-label="%d"></span>' % (folio, folio)) if folio else ""

    if is_cover_like:
        inner = render_titlepage(block)
        title = TITLE
    elif is_part:
        inner = render_part_opener(block, folio, home)
        t = re.search(r'<h1 class="part-title">(.*?)</h1>', block, re.S)
        lab = re.search(r'<p class="part-label">(.*?)</p>', block, re.S)
        title = "%s: %s" % (text_of(lab.group(1)), text_of(t.group(1))) if t and lab else ""
    else:
        body = re.search(r'<div class="body">(.*?)</div>\s*$', strip_chrome(block).rstrip()[:-len("</section>")].rstrip(), re.S)
        inner = body.group(1) if body else strip_chrome(block)
        inner = re.sub(r'<p class="section-head">(.*?)</p>',
                       r'<h3 class="section-head">\1</h3>', inner, flags=re.S)
        kick = re.search(r'<p class="kicker">(.*?)</p>', inner, re.S)
        h1 = re.search(r'<h1 class="page-title([^"]*)">(.*?)</h1>', inner, re.S)
        if h1:
            tight = " tight" if "tight" in h1.group(1) else ""
            inner = inner[: h1.start()] + '<h2 class="ph%s">%s</h2>' % (tight, h1.group(2)) + inner[h1.end():]
            title = text_of(h1.group(2))
            if kick:
                k = text_of(kick.group(1))
                if k.lower() not in title.lower():
                    title = "%s: %s" % (k, title)
        else:
            title = ""

    if title:
        sections.append((folio, title))

    cls = "pg worksheet" if is_work else "pg"
    note = ""
    if is_work:
        note = ('<p class="print-note">This is a worksheet. It is meant to be written on &#8212; '
                'print page %d of the PDF edition, or copy the headings onto paper.</p>' % folio)
    return '<section class="%s" id="p%d">\n%s%s\n%s\n</section>' % (cls, folio or index, marker, note, inner.strip())


XHTML = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"
      lang="{lang}" xml:lang="{lang}">
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <link rel="stylesheet" type="text/css" href="../css/style.css"/>
</head>
<body epub:type="{semantic}">
{content}
</body>
</html>
"""


def extract_fonts(src, fontdir):
    """Pull the base64 woff2 faces out of the print edition into real files."""
    fontdir.mkdir(parents=True, exist_ok=True)
    names = {("Bodoni Moda", "normal", "400"): "bodoni-400",
             ("Bodoni Moda", "italic", "400"): "bodoni-400i",
             ("Bodoni Moda", "normal", "600"): "bodoni-600",
             ("Spectral", "normal", "400"): "spectral-400",
             ("Spectral", "italic", "400"): "spectral-400i",
             ("Spectral", "normal", "600"): "spectral-600",
             ("Archivo", "normal", "500"): "archivo-500",
             ("Archivo", "normal", "600"): "archivo-600"}
    written = []
    for m in re.finditer(r"@font-face\{font-family:'([^']+)';font-style:(\w+);"
                         r"font-weight:(\d+);[^}]*?base64,([A-Za-z0-9+/=]+)\)", src, re.S):
        key = (m.group(1), m.group(2), m.group(3))
        if key not in names:
            continue
        path = fontdir / (names[key] + ".woff2")
        path.write_bytes(base64.b64decode(m.group(4)))
        written.append(path.name)
    return sorted(written)


def build():
    src = SRC.read_text()
    pages = pages_of(src)

    folios = []
    for p in pages:
        m = re.search(r'class="folio">(\d+)<', p)
        folios.append(int(m.group(1)) if m else 0)
    # the four front-matter pages carry no printed folio, but the PDF counts
    # them, so number them 1-4 to keep "page N" in step with the PDF
    for i in range(4):
        if folios[i] == 0:
            folios[i] = i + 1

    home = {f: page_home(f, i + 1) for i, f in enumerate(folios) if f}

    if BUILD.exists():
        shutil.rmtree(BUILD)
    (BUILD / "META-INF").mkdir(parents=True)
    (BUILD / "OEBPS" / "text").mkdir(parents=True)
    (BUILD / "OEBPS" / "css").mkdir(parents=True)
    (BUILD / "OEBPS" / "images").mkdir(parents=True)

    fonts = extract_fonts(src, BUILD / "OEBPS" / "fonts")
    shutil.copy(SRCDIR / "style.css", BUILD / "OEBPS" / "css" / "style.css")
    cover = SRCDIR / "cover.jpg"
    if not cover.exists():
        raise SystemExit("epub-src/cover.jpg is missing - run render-cover.mjs first")
    shutil.copy(cover, BUILD / "OEBPS" / "images" / "cover.jpg")

    nav_rows, page_list = [], []
    files = []

    for (lo, hi), stem, navtitle in CHAPTERS:
        sections, chunks = [], []
        for i, (p, f) in enumerate(zip(pages, folios), start=1):
            if not (lo <= f <= hi):
                continue
            block = to_xhtml_text(close_voids(p))
            block = link_page_refs(block, stem, home)
            chunks.append(render_page(block, f, i, stem, home, sections))
            page_list.append((f, "%s.xhtml#pg%d" % (stem, f)))
        semantic = ("titlepage" if stem == "titlepage" else
                    "toc" if stem == "contents" else
                    "preamble" if stem == "foreword" else
                    "backmatter" if stem == "back" else "bodymatter")
        doc = XHTML.format(lang=LANG, title=htmllib.escape(navtitle),
                           semantic=semantic, content="\n\n".join(chunks))
        (BUILD / "OEBPS" / "text" / (stem + ".xhtml")).write_text(doc, encoding="utf-8")
        files.append(stem)
        nav_rows.append((stem, navtitle, sections))

    return pages, folios, fonts, nav_rows, page_list, files


NAV = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"
      lang="{lang}" xml:lang="{lang}">
<head>
  <meta charset="utf-8"/>
  <title>Contents</title>
  <link rel="stylesheet" type="text/css" href="../css/style.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc" role="doc-toc">
    <h1>Contents</h1>
{toc}
  </nav>
  <nav epub:type="landmarks" id="landmarks" hidden="hidden">
    <h2>Guide</h2>
    <ol>
      <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>
      <li><a epub:type="toc" href="nav.xhtml">Contents</a></li>
      <li><a epub:type="bodymatter" href="part1.xhtml">Start of content</a></li>
    </ol>
  </nav>
  <nav epub:type="page-list" id="page-list" hidden="hidden">
    <h2>Print pages</h2>
    <ol>
{pages}
    </ol>
  </nav>
</body>
</html>
"""

COVER = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"
      lang="{lang}" xml:lang="{lang}">
<head>
  <meta charset="utf-8"/>
  <title>Cover</title>
  <style type="text/css">
    html,body{{margin:0;padding:0;background-color:#1C1B19;height:100%;}}
    .cover-wrap{{margin:0;padding:0;text-align:center;}}
    img{{max-width:100%;max-height:100%;width:auto;height:auto;}}
  </style>
</head>
<body epub:type="cover">
  <section epub:type="cover" class="cover-wrap">
    <img src="../images/cover.jpg" alt="Colette's Home Bible - La Belle Maison"/>
  </section>
</body>
</html>
"""

OPF = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid"
         xml:lang="{lang}" prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{uuid}</dc:identifier>
    <dc:title id="maintitle">{title}</dc:title>
    <meta refines="#maintitle" property="title-type">main</meta>
    <dc:title id="subtitle">{subtitle}</dc:title>
    <meta refines="#subtitle" property="title-type">subtitle</meta>
    <dc:creator id="author">{author}</dc:creator>
    <meta refines="#author" property="role" scheme="marc:relators">aut</meta>
    <meta refines="#author" property="file-as">Dubois, Colette</meta>
    <dc:publisher>{publisher}</dc:publisher>
    <dc:language>{lang}</dc:language>
    <dc:date>{pubdate}</dc:date>
    <dc:description>{description}</dc:description>
    <dc:rights>All rights reserved. Licensed for the personal use of the individual purchaser.</dc:rights>
    <dc:subject>House &amp; Home</dc:subject>
    <dc:subject>Interior design</dc:subject>
    <dc:subject>Home improvement</dc:subject>
    <meta property="dcterms:modified">{pubdate}</meta>
    <meta property="schema:accessMode">textual</meta>
    <meta property="schema:accessMode">visual</meta>
    <meta property="schema:accessModeSufficient">textual</meta>
    <meta property="schema:accessibilityFeature">structuralNavigation</meta>
    <meta property="schema:accessibilityFeature">tableOfContents</meta>
    <meta property="schema:accessibilityFeature">printPageNumbers</meta>
    <meta property="schema:accessibilityFeature">alternativeText</meta>
    <meta property="schema:accessibilityHazard">none</meta>
    <meta property="schema:accessibilitySummary">Reflowable text with headings, lists and tables, a full table of contents, print-page markers matching the PDF edition, and alternative text on every diagram.</meta>
    <meta name="cover" content="cover-image"/>
  </metadata>
  <manifest>
{manifest}
  </manifest>
  <spine toc="ncx">
{spine}
  </spine>
</package>
"""

NCX = """<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="{lang}">
  <head>
    <meta name="dtb:uid" content="{uuid}"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>{title}</text></docTitle>
  <docAuthor><text>{author}</text></docAuthor>
  <navMap>
{navpoints}
  </navMap>
</ncx>
"""

CONTAINER = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def esc(s):
    return htmllib.escape(s, quote=False)


def write_package(fonts, nav_rows, page_list, files):
    oe = BUILD / "OEBPS"

    # ---- nav.xhtml -------------------------------------------------------
    toc = ["    <ol>"]
    for stem, navtitle, sections in nav_rows:
        toc.append('      <li><a href="%s.xhtml">%s</a>' % (stem, esc(navtitle)))
        inner = [s for s in sections if s[1] and s[1] != navtitle]
        if len(inner) > 1:
            toc.append("        <ol>")
            for folio, title in inner:
                toc.append('          <li><a href="%s.xhtml#p%d">%s</a></li>'
                           % (stem, folio, esc(title)))
            toc.append("        </ol>")
        toc.append("      </li>")
    toc.append("    </ol>")

    plist = "\n".join('      <li><a href="%s">%d</a></li>' % (href, n)
                      for n, href in page_list)
    (oe / "text" / "nav.xhtml").write_text(
        NAV.format(lang=LANG, toc="\n".join(toc), pages=plist), encoding="utf-8")
    (oe / "text" / "cover.xhtml").write_text(COVER.format(lang=LANG), encoding="utf-8")

    # ---- manifest + spine ------------------------------------------------
    items = ['    <item id="nav" href="text/nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
             '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
             '    <item id="css" href="css/style.css" media-type="text/css"/>',
             '    <item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
             '    <item id="cover" href="text/cover.xhtml" media-type="application/xhtml+xml"/>']
    for f in fonts:
        items.append('    <item id="font-%s" href="fonts/%s" media-type="font/woff2"/>'
                     % (f.replace(".woff2", ""), f))
    for stem in files:
        doc = (oe / "text" / (stem + ".xhtml")).read_text()
        props = ' properties="svg"' if "<svg" in doc else ""
        items.append('    <item id="%s" href="text/%s.xhtml" media-type="application/xhtml+xml"%s/>'
                     % (stem, stem, props))

    spine = ['    <itemref idref="cover" linear="yes"/>',
             '    <itemref idref="nav" linear="yes"/>']
    spine += ['    <itemref idref="%s" linear="yes"/>' % s for s in files]

    (oe / "content.opf").write_text(OPF.format(
        lang=LANG, uuid=UUID, title=esc(TITLE), subtitle=esc(SUBTITLE), author=esc(AUTHOR),
        publisher=esc(PUBLISHER), pubdate=PUBDATE,
        description=esc("The four corrections - light, height, texture and colour - that a French "
                        "decorator made in fourteen years of small rented flats, with every "
                        "measurement, three reference sections and fifteen worksheets."),
        manifest="\n".join(items), spine="\n".join(spine)), encoding="utf-8")

    # ---- toc.ncx (for older readers) -------------------------------------
    pts, n = [], 0
    for stem, navtitle, sections in nav_rows:
        n += 1
        pts.append('    <navPoint id="np%d" playOrder="%d">\n'
                   '      <navLabel><text>%s</text></navLabel>\n'
                   '      <content src="text/%s.xhtml"/>\n    </navPoint>'
                   % (n, n, esc(navtitle), stem))
    (oe / "toc.ncx").write_text(NCX.format(lang=LANG, uuid=UUID, title=esc(TITLE),
                                           author=esc(AUTHOR), navpoints="\n".join(pts)),
                                encoding="utf-8")
    (BUILD / "META-INF" / "container.xml").write_text(CONTAINER, encoding="utf-8")


def zip_epub():
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w") as z:
        # the mimetype must be first and stored uncompressed
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        for path in sorted(BUILD.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(BUILD).as_posix(),
                        compress_type=zipfile.ZIP_DEFLATED)
    return OUT


if __name__ == "__main__":
    pages, folios, fonts, nav_rows, page_list, files = build()
    write_package(fonts, nav_rows, page_list, files)
    print("chapters      : %d" % len(files))
    print("print pages   : %d mapped, %d markers" % (len([f for f in folios if f]), len(page_list)))
    print("fonts         : %d" % len(fonts))
    print("nav entries   : %d top, %d sub"
          % (len(nav_rows), sum(len(s) for _, _, s in nav_rows)))
    out = zip_epub()
    print("cover image   : %d KB" % round((BUILD / "OEBPS" / "images" / "cover.jpg").stat().st_size / 1024))
    print("wrote         : %s (%.2f MB)" % (out.name, out.stat().st_size / 1024 / 1024))
