"""The "same room, corrected" strip: five rooms drawn before and after one correction.

They are drawings, not photographs, and the page says so. Each pair shows one
correction from the book, with the page it comes from. build.py drops the markup
into the template at {{rooms}}; the strip's movement is CSS, and a few lines of
script in the template double the track so it can loop.
"""

W, H, FLOOR = 200, 130, 98

COLD_WALL, WARM_WALL, WHITE_WALL, DEEP_WALL = "#DDE2E4", "#F1E6CF", "#F4F4F1", "#2F5A49"
FLOOR_COLD, FLOOR_WARM = "#C9C4BA", "#C8A777"


def room(wall, floor, body):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-hidden="true">'
            '<rect width="%d" height="%d" fill="%s"/><rect y="%d" width="%d" height="%d" fill="%s"/>'
            '<path d="M0 %d H%d" stroke="rgba(0,0,0,.18)" stroke-width="1.5"/>%s</svg>'
            % (W, H, W, H, wall, FLOOR, W, H - FLOOR, floor, FLOOR, W, body))


def sofa(x, y=FLOOR, w=78, c="#8E9A8B", cushions=("#D9C7A3", "#B9744F")):
    s = ('<rect x="%d" y="%d" width="%d" height="20" rx="4" fill="%s"/>'
         '<rect x="%d" y="%d" width="%d" height="13" rx="3" fill="%s"/>'
         '<rect x="%d" y="%d" width="7" height="17" rx="3" fill="%s"/><rect x="%d" y="%d" width="7" height="17" rx="3" fill="%s"/>'
         % (x, y - 32, w, c, x - 3, y - 17, w + 6, c, x - 5, y - 22, c, x + w - 2, y - 22, c))
    s += '<path d="M%d %d v5 M%d %d v5" stroke="#5A4632" stroke-width="2"/>' % (x + 4, y - 4, x + w - 4, y - 4)
    for i, col in enumerate(cushions):
        s += '<rect x="%d" y="%d" width="13" height="12" rx="3" fill="%s"/>' % (x + 8 + i * (w - 30), y - 28, col)
    return s


def glow(x, y, r):
    return '<circle cx="%d" cy="%d" r="%d" fill="url(#rg)"/>' % (x, y, r)


def floor_lamp(x, on=True):
    s = glow(x, FLOOR - 52, 34) if on else ""
    return s + ('<path d="M%d %d V%d M%d %d h12" stroke="#5A4632" stroke-width="1.6"/>'
                '<path d="M%d %d l4 -13 h10 l4 13z" fill="%s"/>'
                % (x, FLOOR, FLOOR - 46, x - 6, FLOOR, x - 9, FLOOR - 44, "#F2D58A" if on else "#CFC8B8"))


def table_lamp(x, y, on=True):
    s = glow(x, y - 14, 24) if on else ""
    return s + ('<rect x="%d" y="%d" width="4" height="9" fill="#B0703C"/><path d="M%d %d l3 -10 h8 l3 10z" fill="%s"/>'
                % (x - 2, y - 9, x - 7, y - 9, "#F2D58A" if on else "#CFC8B8"))


def side_table(x, y=FLOOR):
    return '<rect x="%d" y="%d" width="20" height="3" fill="#8A6A45"/><path d="M%d %d v15 M%d %d v15" stroke="#8A6A45" stroke-width="2"/>' % (x, y - 18, x + 3, y - 15, x + 17, y - 15)


def window(x, y, w, h, night=False):
    g = "#27384A" if night else "#CFE3EC"
    return ('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#FFFFFF" stroke-width="3"/>'
            '<path d="M%d %d V%d M%d %d H%d" stroke="#FFFFFF" stroke-width="2"/>'
            % (x, y, w, h, g, x + w // 2, y, y + h, x, y + h // 2, x + w))


def frame(x, y, w, h, c="#B58A4A", art="#DCCDB0"):
    return '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="2"/>' % (x, y, w, h, art, c)


def plant(x, y=FLOOR):
    return ('<path d="M%d %d q-9 -22 -3 -36 M%d %d q8 -18 12 -30 M%d %d q-1 -22 2 -40" stroke="#3E7A5C" stroke-width="3" fill="none" stroke-linecap="round"/>'
            '<path d="M%d %d h14 l-2 12 h-10z" fill="#B9744F"/>' % (x, y - 12, x + 3, y - 12, x + 1, y - 12, x - 6, y - 12))


def ceiling_light(x, on=True):
    s = '<path d="M%d 0 v10" stroke="#777" stroke-width="1.2"/><path d="M%d 10 h16 l-3 7 h-10z" fill="%s"/>' % (x, x - 8, "#FFFFFF" if on else "#CFC8B8")
    if on:
        s += '<path d="M%d 17 L%d %d H%d Z" fill="rgba(210,225,255,.38)"/>' % (x, x - 62, H, x + 62)
    return s


def light_pair():
    before = room(COLD_WALL, FLOOR_COLD, ceiling_light(100) + sofa(60, c="#9AA3A6", cushions=("#B9BEC0", "#B9BEC0")) + side_table(150))
    after = room(WARM_WALL, FLOOR_WARM, ceiling_light(100, on=False) + floor_lamp(34) + sofa(60) + side_table(150) + table_lamp(160, FLOOR - 18)
                 + '<rect x="52" y="%d" width="96" height="16" rx="2" fill="#B9744F" opacity=".35"/>' % (FLOOR + 6))
    return before, after


def curtain_pair():
    win = window(72, 30, 56, 46)
    before = room(WHITE_WALL, FLOOR_COLD, win + '<path d="M66 29 H134" stroke="#777" stroke-width="2"/>'
                  '<path d="M68 30 h14 v44 h-14z M118 30 h14 v44 h-14z" fill="#B7BCC0"/>' + sofa(20, w=60, c="#9AA3A6", cushions=("#B9BEC0",)))
    after = room(WARM_WALL, FLOOR_WARM, win + '<path d="M44 12 H156" stroke="#5A4632" stroke-width="2.4"/>'
                 '<path d="M48 13 h22 q-3 42 0 %d h-22z M130 13 h22 v%d h-22 q3 -42 0 -%dz" fill="#C9A66B"/>' % (FLOOR - 14, FLOOR - 14, FLOOR - 14)
                 + sofa(20, w=60, cushions=("#B9744F",)))
    return before, after


def art_pair():
    small = "".join(frame(x, y, w, h, c="#333") for x, y, w, h in ((40, 8, 14, 18), (62, 20, 20, 14), (90, 6, 12, 16), (110, 22, 18, 12), (136, 10, 14, 20), (76, 40, 12, 10)))
    before = room(WHITE_WALL, FLOOR_COLD, small + sofa(58, c="#9AA3A6", cushions=("#B9BEC0", "#B9BEC0")))
    after = room(WARM_WALL, FLOOR_WARM, frame(74, 22, 52, 36, art="#7FA38C") + '<path d="M82 50 q10 -18 18 -6 q8 -12 18 6z" fill="#F1E6CF" opacity=".8"/>'
                 '<path d="M30 40 H70" stroke="#C9962B" stroke-width="1" stroke-dasharray="3 3"/>' + sofa(58) + floor_lamp(168))
    return before, after


def rug_pair():
    table = '<rect x="84" y="%d" width="32" height="4" rx="1" fill="#8A6A45"/><path d="M88 %d v8 M112 %d v8" stroke="#8A6A45" stroke-width="2"/>' % (FLOOR + 6, FLOOR + 10, FLOOR + 10)
    before = room(WHITE_WALL, FLOOR_COLD, sofa(56, y=FLOOR - 2, w=88, c="#9AA3A6", cushions=("#B9BEC0", "#B9BEC0"))
                  + '<rect x="86" y="%d" width="28" height="12" rx="1" fill="#8FA0B0"/>' % (FLOOR + 12) + table)
    after = room(WARM_WALL, FLOOR_WARM, '<path d="M26 %d L174 %d L192 %d L8 %d Z" fill="#A9553B"/><path d="M36 %d L164 %d L178 %d L22 %d Z" fill="none" stroke="#E7CFA0" stroke-width="1.5"/>'
                 % (FLOOR - 4, FLOOR - 4, H, H, FLOOR, FLOOR, H - 4, H - 4) + sofa(56, y=FLOOR - 2, w=88) + table + plant(170))
    return before, after


def colour_pair():
    chair = lambda c: '<rect x="84" y="%d" width="32" height="26" rx="5" fill="%s"/><rect x="80" y="%d" width="40" height="12" rx="3" fill="%s"/><path d="M86 %d v6 M114 %d v6" stroke="#5A4632" stroke-width="2"/>' % (FLOOR - 36, c, FLOOR - 16, c, FLOOR - 4, FLOOR - 4)
    before = room("#F6F6F4", "#D8D5CE", '<path d="M0 0 H200" stroke="#fff" stroke-width="8"/>' + chair("#E3E0D8") + frame(88, 26, 24, 18, c="#CFCFCF", art="#EDEDEA"))
    after = room(DEEP_WALL, FLOOR_WARM, '<path d="M0 0 H200" stroke="#284E3F" stroke-width="8"/>' + floor_lamp(44) + chair("#C9962B") + frame(84, 22, 32, 24, c="#E7CFA0", art="#F1E6CF")
                 + side_table(132) + '<rect x="138" y="%d" width="8" height="10" fill="#F7F1E6"/>' % (FLOOR - 28))
    return before, after


ROOMS = (
    ("The light", "One cold ceiling light, or three warm lamps at three heights.", "Page 28 &middot; The three heights", light_pair),
    ("The curtains", "Hung at the frame and short, or hung high, wide and to the floor.", "Page 93 &middot; The drop", curtain_pair),
    ("The wall", "Six small frames up by the ceiling, or one picture at eye height.", "Page 87 &middot; 145 centimetres", art_pair),
    ("The rug", "A little rug floating in the middle, or one the furniture stands on.", "Page 97 &middot; The rug is too small", rug_pair),
    ("The small room", "Painted pale and still small, or painted deep and deliberate.", "Page 57 &middot; A small room painted pale", colour_pair),
)

DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><radialGradient id="rg">'
        '<stop offset="0" stop-color="#FFD98A" stop-opacity=".95"/><stop offset=".45" stop-color="#FFD98A" stop-opacity=".4"/>'
        '<stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient></defs></svg>')


def html():
    cards = []
    for title, line, page, pair in ROOMS:
        b, a = pair()
        cards.append('<figure class="room" tabindex="0"><div class="room-pair">'
                     '<div class="room-half"><span class="tag">Before</span>%s</div>'
                     '<div class="room-half"><span class="tag after">After</span>%s</div></div>'
                     '<figcaption><b>%s</b>%s<small>%s</small></figcaption></figure>' % (b, a, title, line, page))
    return DEFS + '<div class="rooms" id="rooms"><div class="rooms-track">' + "".join(cards) + "</div></div>"


if __name__ == "__main__":
    print(len(html()), "characters")
