#!/usr/bin/env python3
"""Make the Christmas edition of the landing page.

    node christmas/render-assets.cjs          # cover images, first
    python3 christmas/make-christmas-landing.py

Reads landing.html and writes landing-christmas.html with three additions:
the Christmas book standing in front of the Home Bible in the hero, one line
under the buy button, and a short "This December" strip under the hero.
landing.html itself is never touched, so in January the Christmas edition is
simply replaced by landing.html again. Price, checkout and every other
section are unchanged.
"""
import base64
import pathlib

HERE = pathlib.Path(__file__).parent
SRC = HERE.parent / "landing.html"
OUT = HERE.parent / "landing-christmas.html"
LIMIT = 500_000          # Gumroad's custom_html limit, in characters

CSS = """
  /* ---- Christmas edition ---- */
  .xmas-book{position:absolute;right:-7%;bottom:-7%;width:46%;transform:rotate(4deg);z-index:2;
    border-radius:2px 4px 4px 2px;box-shadow:0 26px 50px -18px rgba(0,0,0,.85),0 6px 14px rgba(0,0,0,.4)}
  .xmas-book img{display:block;width:100%;height:auto;border-radius:inherit;box-shadow:none}
  .xmas-book::before{content:"";position:absolute;inset:0 auto 0 0;width:5%;
    background:linear-gradient(90deg,rgba(0,0,0,.45),rgba(255,255,255,.1) 55%,rgba(0,0,0,.18))}
  .xmas-tag{position:absolute;left:50%;top:-1.05rem;transform:translateX(-50%) rotate(-4deg);white-space:nowrap;
    font-family:var(--sans);font-size:.66rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;
    background:#9E2A2B;color:#F7F1E6;padding:.42rem .8rem;border-radius:999px;box-shadow:0 8px 18px -8px rgba(0,0,0,.6)}
  @media(max-width:899px){ .xmas-book{right:2%;bottom:-5%;width:40%} }
  .xmas-note{margin:.9rem 0 0;font-family:var(--sans);font-size:.86rem;line-height:1.5;color:var(--cream)}
  .xmas-note b{color:var(--amber);font-weight:600}
  .xmas{background:linear-gradient(160deg,#1A4434,#12322A 60%,#0E2820);color:#F7F1E6;
    border-top:4px solid #9E2A2B;border-bottom:4px solid #9E2A2B;padding:clamp(2.4rem,6vw,3.6rem) 0}
  .xmas-grid{display:grid;gap:clamp(1.6rem,4vw,3rem);align-items:center}
  @media(min-width:860px){ .xmas-grid{grid-template-columns:auto 1fr} }
  .xmas-cover{width:min(210px,52vw);margin:0 auto;transform:rotate(-3deg);border-radius:2px 4px 4px 2px;
    box-shadow:0 22px 44px -16px rgba(0,0,0,.8)}
  .xmas-cover img{display:block;width:100%;height:auto;border-radius:inherit}
  .xmas .kick{font-family:var(--sans);font-size:.72rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:#C9A24A;margin:0 0 .6rem}
  .xmas h2{font-family:var(--serif);font-weight:400;font-size:clamp(1.7rem,4vw,2.4rem);line-height:1.12;margin:0 0 .8rem;color:#F7F1E6}
  .xmas p{color:rgba(247,241,230,.86);margin:0 0 .9rem;max-width:62ch}
  .xmas ul{list-style:none;padding:0;margin:0 0 1rem;display:grid;gap:.45rem;max-width:62ch}
  @media(min-width:640px){ .xmas ul{grid-template-columns:1fr 1fr} }
  .xmas li{position:relative;padding-left:1.25rem;color:rgba(247,241,230,.9);font-size:.95rem}
  .xmas li::before{content:"";position:absolute;left:0;top:.55em;width:.5rem;height:.5rem;border-radius:50%;background:#B0362F}
  .xmas .small{font-size:.85rem;color:rgba(247,241,230,.66)}
"""

HERO_IMG_END = """alt="Colette's Home Bible, by Colette Dubois — hardcover edition standing on a stone counter in raking window light" width="560" height="786">"""

NOTE_AFTER = """<p class="cta-note" style="margin-top:.6rem">204&nbsp;pages &middot; metric and imperial throughout</p>"""

STRIP_BEFORE = "<!-- ======== THE ARGUMENT ======== -->"


def main():
    s = SRC.read_text()
    for marker in ("</style>", HERO_IMG_END, NOTE_AFTER, STRIP_BEFORE):
        assert s.count(marker) >= 1, marker[:50]
    small = base64.b64encode((HERE / "cover-christmas-small.jpg").read_bytes()).decode()
    img = ('<img src="data:image/jpeg;base64,%s" alt="The Christmas Pages, by Colette Dubois: '
           'a Christmas companion to Colette\'s Home Bible" width="492" height="696">' % small)

    s = s.replace("</style>", CSS + "</style>", 1)
    s = s.replace(HERO_IMG_END, HERO_IMG_END + """
      <div class="xmas-book"><span class="xmas-tag">Free this Christmas</span>%s</div>""" % img, 1)
    s = s.replace(NOTE_AFTER, NOTE_AFTER + """
      <p class="xmas-note"><b>Until 31 December:</b> <em>The Christmas Pages</em>, a 25-page Christmas
        companion, comes free with every copy.</p>""", 1)
    s = s.replace(STRIP_BEFORE, """<!-- ======== THIS DECEMBER (Christmas edition only) ======== -->
<section class="xmas" id="christmas">
  <div class="wrap xmas-grid">
    <div class="xmas-cover">%s</div>
    <div>
      <p class="kick">This December &middot; free with the book</p>
      <h2>The Christmas Pages</h2>
      <p>Once a year, fifty new objects arrive in a room in a single weekend. These 25 pages apply the
        whole method to that weekend, in the same order as the book: the light first, then the height,
        then the materials and the colour.</p>
      <ul>
        <li>The number on a box of fairy lights</li>
        <li>Lighting a tree from the inside</li>
        <li>The right tree for the room</li>
        <li>Hanging it all without a drill</li>
        <li>A palette for December</li>
        <li>The r&eacute;veillon table, measured</li>
        <li>What not to buy for Christmas</li>
        <li>A printable Christmas audit</li>
      </ul>
      <p class="small">PDF and EPUB, delivered with the book. Already own Colette&rsquo;s Home Bible? It is
        waiting in your Gumroad library.</p>
    </div>
  </div>
</section>

""" % img.replace('width="492" height="696"', 'width="210" height="297" loading="lazy"') + STRIP_BEFORE, 1)

    OUT.write_text(s)
    print("wrote %s: %d characters (Gumroad limit %d)" % (OUT.name, len(s), LIMIT))
    if len(s) > LIMIT:
        raise SystemExit("too long for Gumroad's custom_html field")


if __name__ == "__main__":
    main()
