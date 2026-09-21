#!/usr/bin/env python3
"""Shrink landing.html under Gumroad's 500,000-character custom_html limit.

Two savings, in this order:
  1. every carousel page was embedded twice - once in the button's data-full
     attribute and once in the <img> inside it. The lightbox now reads the
     image it already has, so the second copy goes.
  2. what is left is re-encoded at the size it is actually displayed.
"""
import base64, io, re, sys, pathlib
from PIL import Image

LIMIT = 500_000
SRC = pathlib.Path('landing.html')
DST = pathlib.Path('landing-small.html')
s = SRC.read_text(errors='replace')
start = len(s)

# --- 1. drop the duplicate copies -------------------------------------------
s = re.sub(r'\s+data-full="data:image/[a-z]+;base64,[A-Za-z0-9+/=]+"', '', s)
s = s.replace("lbimg.src=b.getAttribute('data-full');",
              "var im=b.querySelector('img'); lbimg.src=im?im.src:'';")
assert 'data-full' not in s, "a data-full attribute survived"
assert "b.querySelector('img')" in s, "lightbox rewiring failed"
print("after de-duplication: %d chars (saved %d)" % (len(s), start-len(s)))

# --- 2. re-encode at sensible sizes -----------------------------------------
def recode(b64, max_w, quality):
    im = Image.open(io.BytesIO(base64.b64decode(b64)))
    if im.mode != 'RGB':
        im = im.convert('RGB')
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode(), im.size

s_html = s

def pass_at(html, max_w, quality):
    out = html
    for m in re.finditer(r'data:image/[a-z]+;base64,([A-Za-z0-9+/=]+)', html):
        new, _ = recode(m.group(1), max_w, quality)
        out = out.replace(m.group(0), 'data:image/jpeg;base64,' + new)
    return out

# The carousel pages open in a lightbox and sit at about 234px in the rail, so
# they can take more compression than the cover, which is the first thing anyone
# sees. Size each by what it is for rather than treating them alike.
def pass_split(html, cover_w, cover_q, page_w, page_q):
    out = html
    for m in re.finditer(r'data:image/[a-z]+;base64,([A-Za-z0-9+/=]+)', html):
        im = Image.open(io.BytesIO(base64.b64decode(m.group(1))))
        is_page = im.height > im.width * 1.3 and im.width >= 800
        new, _ = recode(m.group(1), *( (page_w, page_q) if is_page else (cover_w, cover_q) ))
        out = out.replace(m.group(0), 'data:image/jpeg;base64,' + new)
    return out

for cw, cq, pw, pq in ((760, 80, 560, 68), (720, 78, 520, 66),
                       (680, 76, 500, 64), (640, 74, 460, 62)):
    trial = pass_split(s_html, cw, cq, pw, pq)
    print("   cover %3dpx q%d, pages %3dpx q%d -> %7d chars%s"
          % (cw, cq, pw, pq, len(trial), "   <- 5%+ margin" if len(trial) <= LIMIT*0.95 else ""))
    if len(trial) <= LIMIT * 0.95:
        DST.write_text(trial)
        print("\nwrote %s: %d chars, %d under the limit (%.0f%% smaller than the original)"
              % (DST.name, len(trial), LIMIT-len(trial), 100*(1-len(trial)/start)))
        sys.exit(0)
print("\ncould not reach a 5 percent margin")
sys.exit(1)
