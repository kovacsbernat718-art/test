#!/usr/bin/env python3
"""Validate the built EPUB: package integrity, XML, links, accessibility.

    python3 check-epub.py
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

EPUB = pathlib.Path(__file__).parent / "Colettes-Home-Bible.epub"
NS = {"opf": "http://www.idpf.org/2007/opf",
      "c": "urn:oasis:names:tc:opendocument:xmlns:container",
      "x": "http://www.w3.org/1999/xhtml",
      "epub": "http://www.idpf.org/2007/ops",
      "ncx": "http://www.daisy.org/z3986/2005/ncx/"}

problems, notes = [], []


def fail(msg):
    problems.append(msg)


def main():
    z = zipfile.ZipFile(EPUB)
    names = z.namelist()

    # --- 1. container integrity ------------------------------------------
    if names[0] != "mimetype":
        fail("mimetype is not the first entry (it is %r)" % names[0])
    info = z.getinfo("mimetype")
    if info.compress_type != zipfile.ZIP_STORED:
        fail("mimetype is compressed; it must be stored")
    if z.read("mimetype") != b"application/epub+zip":
        fail("mimetype content is wrong")
    if "META-INF/container.xml" not in names:
        fail("META-INF/container.xml missing")

    root = ET.fromstring(z.read("META-INF/container.xml"))
    opf_path = root.find(".//c:rootfile", NS).get("full-path")
    notes.append("rootfile: %s" % opf_path)

    # --- 2. every XML file parses ----------------------------------------
    xmls = [n for n in names if n.endswith((".xhtml", ".opf", ".ncx", ".xml"))]
    for n in xmls:
        try:
            ET.fromstring(z.read(n))
        except ET.ParseError as e:
            fail("XML not well-formed: %s - %s" % (n, e))
    notes.append("XML files parsed: %d" % len(xmls))

    # undefined named entities are a parse error in XHTML; catch them early
    for n in xmls:
        body = z.read(n).decode("utf-8")
        bad = set(re.findall(r"&([a-zA-Z]{2,10});", body)) - {"amp", "lt", "gt", "quot", "apos"}
        if bad:
            fail("%s uses named entities XHTML does not define: %s" % (n, sorted(bad)))

    # --- 3. manifest <-> files -------------------------------------------
    opf = ET.fromstring(z.read(opf_path))
    base = opf_path.rsplit("/", 1)[0]
    manifest = {}
    for item in opf.findall(".//opf:manifest/opf:item", NS):
        href = item.get("href")
        full = "%s/%s" % (base, href)
        manifest[item.get("id")] = (full, item.get("media-type"), item.get("properties") or "")
        if full not in names:
            fail("manifest lists a file that is not in the zip: %s" % full)

    packaged = {f for _, (f, _, _) in manifest.items()}
    for n in names:
        if n in ("mimetype", "META-INF/container.xml", opf_path):
            continue
        if n not in packaged:
            fail("file in the zip but not in the manifest: %s" % n)
    notes.append("manifest items: %d" % len(manifest))

    # exactly one nav doc, one cover-image
    navs = [i for i, (_, _, p) in manifest.items() if "nav" in p.split()]
    covers = [i for i, (_, _, p) in manifest.items() if "cover-image" in p.split()]
    if len(navs) != 1:
        fail("expected exactly one nav document, found %d" % len(navs))
    if len(covers) != 1:
        fail("expected exactly one cover-image, found %d" % len(covers))

    # --- 4. spine ---------------------------------------------------------
    spine = [it.get("idref") for it in opf.findall(".//opf:spine/opf:itemref", NS)]
    for idref in spine:
        if idref not in manifest:
            fail("spine references an unknown id: %s" % idref)
    notes.append("spine items: %d" % len(spine))
    if opf.find(".//opf:spine", NS).get("toc") not in manifest:
        fail("spine/@toc does not point at the ncx")

    # --- 5. ids and internal links ---------------------------------------
    ids, links, imgs, svgs = {}, [], 0, 0
    docs = [f for f, m, _ in manifest.values() if m == "application/xhtml+xml"]
    for d in docs:
        tree = ET.fromstring(z.read(d))
        ids[d] = {e.get("id") for e in tree.iter() if e.get("id")}
        for a in tree.iter("{http://www.w3.org/1999/xhtml}a"):
            href = a.get("href")
            if href and not href.startswith(("http:", "https:", "mailto:")):
                links.append((d, href))
        for img in tree.iter("{http://www.w3.org/1999/xhtml}img"):
            imgs += 1
            if not img.get("alt"):
                fail("%s has an <img> with no alt text" % d)
        for s in tree.iter("{http://www.w3.org/2000/svg}svg"):
            svgs += 1
            if not (s.get("{http://www.w3.org/XML/1998/namespace}lang") or
                    s.get("role") or s.get("aria-label") or
                    s.find("{http://www.w3.org/2000/svg}title") is not None):
                fail("%s has an <svg> with no accessible name" % d)

    broken = 0
    for src, href in links:
        path, _, frag = href.partition("#")
        target = src if not path else "%s/%s" % (src.rsplit("/", 1)[0], path)
        target = re.sub(r"/[^/]+/\.\./", "/", target)
        if target not in ids:
            fail("link to a document that is not in the book: %s -> %s" % (src, href))
            broken += 1
        elif frag and frag not in ids[target]:
            fail("link to a missing anchor: %s -> %s" % (src, href))
            broken += 1
    notes.append("internal links: %d, broken: %d" % (len(links), broken))
    notes.append("images: %d, svg diagrams: %d" % (imgs, svgs))

    # --- 6. page markers --------------------------------------------------
    nav_doc = manifest[navs[0]][0]
    nav = ET.fromstring(z.read(nav_doc))
    pagelist = [n for n in nav.iter("{http://www.w3.org/1999/xhtml}nav")
                if n.get("{http://www.idpf.org/2007/ops}type") == "page-list"]
    toc = [n for n in nav.iter("{http://www.w3.org/1999/xhtml}nav")
           if n.get("{http://www.idpf.org/2007/ops}type") == "toc"]
    if not toc:
        fail("nav document has no toc")
    markers = sum(len(re.findall(r'epub:type="pagebreak"', z.read(d).decode("utf-8")))
                  for d in docs)
    entries = len(pagelist[0].findall(".//{http://www.w3.org/1999/xhtml}a")) if pagelist else 0
    notes.append("page markers: %d in text, %d in the page-list" % (markers, entries))
    if pagelist and markers != entries:
        fail("page markers and page-list entries disagree (%d vs %d)" % (markers, entries))

    # --- 7. print-only chrome should be gone ------------------------------
    for d in docs:
        body = z.read(d).decode("utf-8")
        for cls in ('class="rh"', 'class="footer"', 'class="folio"'):
            if cls in body:
                fail("%s still contains print chrome: %s" % (d, cls))

    # --- report -----------------------------------------------------------
    print("EPUB: %s (%.2f MB, %d files)" % (EPUB.name, EPUB.stat().st_size / 1024 / 1024, len(names)))
    for n in notes:
        print("  - %s" % n)
    if problems:
        print("\n%d PROBLEM(S):" % len(problems))
        for p in problems:
            print("  ! %s" % p)
        return 1
    print("\nno problems found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
