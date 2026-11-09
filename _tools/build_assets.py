"""Builds the website's images and fonts from the GameStudio repo.

WHAT IT DOES
  Makes everything under assets/ plus the favicons and the Open Graph images:
  - Fredoka (OFL) subset to Latin and saved as WOFF2, with its licence;
  - Codex's Tide Trail logo, Pebble the otter and the shells pattern, resized;
  - the Tide Trail app icon (Codex's waving otter, the icon in the build) at 360 px
    for the game page, which rounds its corners in CSS;
  - phone screenshots from the game's real play-test captures;
  - favicon.svg / favicon.ico / apple-touch-icon.png (a simple keep tower:
    the studio logo is still being designed);
  - og-hineskeep.png and og-tidetrail.png (1200 x 630);
  - the press kit (/tidetrail/press/): six real captures at 540 px for the page and
    at full size (1290 x 2796, JPG) for download, the 1024 px app icon and the logo.

HOW TO RUN
  py -3 _tools/build_assets.py --studio C:/dev/GameStudio
  python3 _tools/build_assets.py --studio ~/Developer/GameStudio-web-store --only icon,og
  python3 _tools/build_assets.py --studio ~/Developer/GameStudio-web-store --only press
  Needs Pillow, plus fonttools and brotli for the font step (--only skips what
  isn't named: fonts, art, icon, favicons, og, press). The GameStudio clone needs the LFS files
  for Status/img/2026-11-07_session-17_* and _ArtDevelopment/TideTrail/.

STUDIO RULES
  Never use anything from _ArtDevelopment/References/, any *gate_board* image or
  internal concepts. SHOTS below lists every capture this site publishes.
"""

import argparse
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parent.parent
SAND = (251, 241, 228)
TEAL = (22, 179, 198)
DEEP = (11, 79, 92)
INK = (23, 51, 59)

# The press kit's captures (2026-11-08, round 7): the game's own playtest renders from
# session 24, the newest build with the launch features; part B (about Nov 26 - Dec 2) may swap
# them for session 29's release-candidate frames. (output name, capture file in Status/img/).
PRESS_SHOTS = {
    "clean": "2026-11-08_session-24_playtest_level3_half_drawn.png",
    "stars": "2026-11-08_session-24_playtest_level8_three_stars.png",
    "swimmer": "2026-11-08_session-24_playtest_swim_crab.png",
    "theme": "2026-11-08_session-24_playtest_theme_night_tide.png",
    "daily": "2026-11-08_session-24_playtest_home_daily_streak3.png",
    "gifts": "2026-11-08_session-24_playtest_login_calendar.png",
}

# Published captures: (output name, capture file in Status/img/).
SHOTS = {
    "shot-finish": "2026-11-07_session-17_playtest_level1_finish.png",
    "shot-draw": "2026-11-07_session-17_playtest_level1_ghost_hand.png",
    "shot-clean": "2026-11-07_session-17_playtest_level3_half_drawn.png",
    "shot-swim": "2026-11-07_session-17_playtest_level4_swim.png",
    "shot-currents": "2026-11-07_session-17_playtest_level21_currents.png",
    "shot-tide": "2026-11-07_session-17_playtest_level10_tide_freeze.png",
}


def fonts(art: Path, out: Path):
    """Subsets Fredoka SemiBold and Bold to Basic Latin plus a few marks, as WOFF2."""
    from fontTools import subset
    out.mkdir(parents=True, exist_ok=True)
    text = "".join(chr(c) for c in range(0x20, 0x7F)) + "\u00a0\u00a9\u00b7\u2013\u2014\u2018\u2019\u201c\u201d\u2026\u2192\u00e9"
    for weight, name in (("600", "fredoka_semibold.ttf"), ("700", "fredoka_bold.ttf")):
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga"]
        font = subset.load_font(str(art / "fonts/fredoka" / name), opts)
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(font)
        subset.save_font(font, str(out / f"fredoka-{weight}.woff2"), opts)
    shutil.copy(art / "fonts/fredoka/OFL.txt", out / "Fredoka-OFL.txt")


def fit(path: Path, width: int) -> Image.Image:
    """Opens an image and resizes it to the given width, keeping its shape."""
    im = Image.open(path)
    h = round(im.height * width / im.width)
    return im.resize((width, h), Image.LANCZOS)


def art_images(studio: Path, art: Path, out: Path):
    """Logo, otter, pattern and the phone screenshots."""
    out.mkdir(parents=True, exist_ok=True)
    fit(art / "loading/logo_tide_trail.png", 640).save(out / "tide-trail-logo.png", optimize=True)
    fit(art / "critters/otter/otter_cheer.png", 360).save(out / "pebble-cheer.png", optimize=True)
    fit(art / "critters/otter/otter_float.png", 240).save(out / "pebble-float.png", optimize=True)
    # The shells pattern as a faint tile for page backgrounds.
    fit(art / "patterns/pattern_shells.png", 320).save(out / "pattern-shells.png", optimize=True)
    for name, capture in SHOTS.items():
        src = studio / "Status/img" / capture
        assert "gate_board" not in capture
        im = Image.open(src).convert("RGB")
        im.resize((540, round(im.height * 540 / im.width)), Image.LANCZOS).save(
            out / f"{name}.jpg", quality=84, optimize=True, progressive=True)


def press_kit(studio: Path, art: Path, img_out: Path, kit_out: Path):
    """The press page's screenshots (540 px) and its downloads (full-size JPGs, icon, logo)."""
    img_out.mkdir(parents=True, exist_ok=True)
    kit_out.mkdir(parents=True, exist_ok=True)
    for name, capture in PRESS_SHOTS.items():
        assert "gate_board" not in capture and "References" not in capture
        im = Image.open(studio / "Status/img" / capture).convert("RGB")
        im.resize((540, round(im.height * 540 / im.width)), Image.LANCZOS).save(
            img_out / f"press-{name}.jpg", quality=84, optimize=True, progressive=True)
        im.save(kit_out / f"tide-trail-{name}-{im.width}x{im.height}.jpg", quality=90, optimize=True)
    Image.open(art / "icon/app_icon_1024.png").convert("RGB").save(
        kit_out / "tide-trail-icon-1024.png", optimize=True)
    shutil.copy(art / "loading/logo_tide_trail.png", kit_out / "tide-trail-logo-1024x600.png")


def app_icon(art: Path, out: Path):
    """The App Store icon as built (1024 px, square), at 360 px; the page rounds it."""
    out.mkdir(parents=True, exist_ok=True)
    fit(art / "icon/app_icon_1024.png", 360).convert("RGB").save(out / "app-icon.png", optimize=True)


def tower(size: int) -> Image.Image:
    """The placeholder mark: a white keep tower on a wave, on a teal rounded square."""
    s = size / 64
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=14 * s, fill=TEAL + (255,))
    white = (255, 255, 255, 255)
    # Body and three merlons.
    d.rectangle((20 * s, 22 * s, 44 * s, 48 * s), fill=white)
    for x in (20, 29, 38):
        d.rectangle((x * s, 14 * s, (x + 6) * s, 23 * s), fill=white)
    # Arched door.
    d.rectangle((28.5 * s, 37 * s, 35.5 * s, 48 * s), fill=TEAL + (255,))
    d.ellipse((28.5 * s, 33.5 * s, 35.5 * s, 40.5 * s), fill=TEAL + (255,))
    # Sand-coloured wave across the bottom.
    d.rounded_rectangle((8 * s, 48 * s, 56 * s, 54 * s), radius=3 * s, fill=SAND + (255,))
    return im


def favicons():
    """favicon.ico (16/32/48), apple-touch-icon.png (180, opaque)."""
    big = tower(512)
    big.resize((48, 48), Image.LANCZOS).save(SITE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    touch = Image.new("RGB", (180, 180), TEAL)
    t = tower(512).resize((180, 180), Image.LANCZOS)
    touch.paste(t, (0, 0), t)
    touch.save(SITE / "apple-touch-icon.png", optimize=True)


def pattern_bg(w: int, h: int, art: Path, tile: int = 300) -> Image.Image:
    """Sand with Codex's shells pattern repeated over it."""
    bg = Image.new("RGBA", (w, h), SAND + (255,))
    p = fit(art / "patterns/pattern_shells.png", tile)
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            bg.alpha_composite(p, (x, y))
    return bg


def phone(capture: Path, height: int) -> Image.Image:
    """A capture with rounded corners and a soft shadow, `height` pixels tall."""
    im = Image.open(capture).convert("RGBA")
    w = round(im.width * height / im.height)
    im = im.resize((w, height), Image.LANCZOS)
    r = round(w * 0.11)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, height - 1), radius=r, fill=255)
    pad = 24
    out = Image.new("RGBA", (w + pad * 2, height + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((pad, pad + 8, pad + w, pad + height + 8), radius=r, fill=(23, 51, 59, 60))
    from PIL import ImageFilter
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    frame = Image.new("RGBA", (w + 12, height + 12), (0, 0, 0, 0))
    ImageDraw.Draw(frame).rounded_rectangle((0, 0, w + 11, height + 11), radius=r + 6, fill=(255, 255, 255, 255))
    out.alpha_composite(frame, (pad - 6, pad - 6))
    out.paste(im, (pad, pad), mask)
    return out


def og_images(studio: Path, art: Path):
    """The two 1200 x 630 Open Graph images."""
    bold = str(art / "fonts/fredoka/fredoka_bold.ttf")
    semi = str(art / "fonts/fredoka/fredoka_semibold.ttf")
    img = studio / "Status/img"

    # Tide Trail: logo and line on the left, the real finish screen on the right.
    og = pattern_bg(1200, 630, art)
    logo = fit(art / "loading/logo_tide_trail.png", 520)
    og.alpha_composite(logo, (60, 40))
    d = ImageDraw.Draw(og)
    d.text((70, 380), "Draw one line. Clean the pool.", font=ImageFont.truetype(semi, 40), fill=INK)
    d.text((70, 432), "Watch Pebble swim.", font=ImageFont.truetype(semi, 40), fill=INK)
    pill = ImageFont.truetype(bold, 30)
    label = "December 2026 on iPhone"
    tw = d.textbbox((0, 0), label, font=pill)[2]
    d.rounded_rectangle((70, 512, 70 + tw + 64, 568), radius=28, fill=DEEP)
    d.text((70 + 32 + tw // 2, 540), label, font=pill, fill=(255, 255, 255), anchor="mm")
    p = phone(img / SHOTS["shot-finish"], 560)
    og.alpha_composite(p, (1200 - p.width - 60, (630 - p.height) // 2))
    otter = fit(art / "critters/otter/otter_cheer.png", 200)
    og.alpha_composite(otter, (560, 400))
    og.convert("RGB").save(SITE / "assets/img/og-tidetrail.png", optimize=True)

    # Studio: the mark, the name and the one line, with Pebble.
    og = pattern_bg(1200, 630, art)
    d = ImageDraw.Draw(og)
    mark = tower(512).resize((150, 150), Image.LANCZOS)
    og.alpha_composite(mark, (80, 120))
    d.text((80, 300), "Hines Keep", font=ImageFont.truetype(bold, 104), fill=INK)
    d.text((84, 430), "Calm, friendly games for your phone,", font=ImageFont.truetype(semi, 38), fill=INK)
    d.text((84, 478), "made with care in Michigan.", font=ImageFont.truetype(semi, 38), fill=INK)
    otter = fit(art / "critters/otter/otter_cheer.png", 380)
    og.alpha_composite(otter, (780, 180))
    og.convert("RGB").save(SITE / "assets/img/og-hineskeep.png", optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--studio", required=True, help="path to the GameStudio clone")
    ap.add_argument("--only", default="fonts,art,icon,favicons,og,press",
                    help="comma-separated steps to run (default: all)")
    args = ap.parse_args()
    studio = Path(args.studio)
    art = studio / "_ArtDevelopment/TideTrail"
    steps = {x.strip() for x in args.only.split(",")}
    if "fonts" in steps:
        fonts(art, SITE / "assets/fonts")
    if "art" in steps:
        art_images(studio, art, SITE / "assets/img")
    if "icon" in steps:
        app_icon(art, SITE / "assets/img")
    if "favicons" in steps:
        favicons()
    if "og" in steps:
        og_images(studio, art)
    if "press" in steps:
        press_kit(studio, art, SITE / "assets/img", SITE / "assets/press")
    print("done:", ", ".join(sorted(steps)))


if __name__ == "__main__":
    main()
