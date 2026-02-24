"""Generate Open Graph images for AI Pulse articles."""
import textwrap

from PIL import Image, ImageDraw, ImageFont
import os

# ── Dimensions ──
W, H = 1200, 630

# ── Palette (matching site CSS) ──
BG      = (10, 10, 10)       # #0a0a0a
BG2     = (17, 17, 17)       # #111111
ACCENT  = (232, 84, 58)      # #e8543a
TEXT    = (232, 228, 222)     # #e8e4de
SOFT    = (136, 136, 128)    # #888880
FAINT   = (68, 68, 64)       # #444440
BORDER  = (34, 34, 34)       # #222222

# ── Windows system fonts ──
FONTS = "C:/Windows/Fonts/"


def load_fonts():
    try:
        return {
            "brand":    ImageFont.truetype(FONTS + "segoeuib.ttf", 18),
            "tag":      ImageFont.truetype(FONTS + "consola.ttf", 15),
            "heading":  ImageFont.truetype(FONTS + "segoeuib.ttf", 44),
            "heading2": ImageFont.truetype(FONTS + "segoeuil.ttf", 44),
            "sub":      ImageFont.truetype(FONTS + "segoeuil.ttf", 21),
            "meta":     ImageFont.truetype(FONTS + "consola.ttf", 14),
        }
    except Exception:
        f = ImageFont.load_default()
        return {k: f for k in ["brand","tag","heading","heading2","sub","meta"]}


def draw_og(title_bold, title_italic, subtitle, tags, meta_lines, filename):
    fonts = load_fonts()
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ── Accent stripe at top ──
    draw.rectangle([0, 0, W, 4], fill=ACCENT)

    # ── Subtle border rectangle ──
    draw.rectangle([40, 30, W-40, H-30], outline=BORDER, width=1)

    # ── Inner bg panel ──
    draw.rectangle([41, 31, W-41, H-31], fill=BG2)

    # ── Brand ──
    x, y = 72, 56
    draw.text((x, y), "AI PULSE", fill=ACCENT, font=fonts["brand"])
    # Dot separator
    bw = draw.textlength("AI PULSE", font=fonts["brand"])
    draw.text((x + bw + 12, y), "·", fill=FAINT, font=fonts["brand"])
    draw.text((x + bw + 28, y + 2), "ISSUE #" + filename.split("-")[0].replace("og/","").replace("og\\",""), fill=SOFT, font=fonts["tag"])

    # ── Tag line ──
    y = 96
    draw.text((x, y), tags, fill=SOFT, font=fonts["tag"])

    # ── Accent bar ──
    y = 128
    draw.rectangle([x, y, x + 60, y + 3], fill=ACCENT)

    # ── Main heading (bold part) ──
    y = 152
    wrapped_bold = textwrap.fill(title_bold, width=32)
    for line in wrapped_bold.split("\n"):
        draw.text((x, y), line, fill=TEXT, font=fonts["heading"])
        y += 56

    # ── Main heading (italic/light part) ──
    wrapped_ital = textwrap.fill(title_italic, width=36)
    for line in wrapped_ital.split("\n"):
        draw.text((x, y), line, fill=ACCENT, font=fonts["heading2"])
        y += 56

    # ── Subtitle ──
    y += 12
    wrapped_sub = textwrap.fill(subtitle, width=65)
    for line in wrapped_sub.split("\n"):
        draw.text((x, y), line, fill=SOFT, font=fonts["sub"])
        y += 30

    # ── Bottom metadata ──
    y = H - 80
    draw.line([x, y, W - 72, y], fill=BORDER, width=1)
    y += 16
    meta_text = "  ·  ".join(meta_lines)
    draw.text((x, y), meta_text, fill=FAINT, font=fonts["meta"])

    # ── Bottom accent stripe ──
    draw.rectangle([0, H-4, W, H], fill=ACCENT)

    # Save
    os.makedirs("og", exist_ok=True)
    path = os.path.join("og", filename)
    img.save(path, "PNG", quality=95)
    print(f"✓ Generated {path} ({W}x{H})")


# ────────────────────────────────────────────
# Issue #002
# ────────────────────────────────────────────
draw_og(
    title_bold   = "Anthropic's Two-Front War —",
    title_italic = "And the Week Everything Escalated",
    subtitle     = "China stole its AI. The Pentagon threatened to blacklist it. India bet $200 billion on an AI future. And the agents nobody can control went live.",
    tags         = "Analysis  ·  Geopolitics  ·  AI Agents  ·  February 2026",
    meta_lines   = ["Based on events from Feb 13–24, 2026", "23 sources cited", "~12 min read"],
    filename     = "002-anthropic-two-front-war.png",
)

# ────────────────────────────────────────────
# Issue #001
# ────────────────────────────────────────────
draw_og(
    title_bold   = "AI Built Itself —",
    title_italic = "And the World Is Only Starting to Notice",
    subtitle     = "How ten days of quiet announcements shook global markets, wiped ₹2 lakh crore from Indian IT, and confirmed something researchers have been warning about for years.",
    tags         = "Analysis  ·  Markets  ·  Deep Tech  ·  February 2026",
    meta_lines   = ["Based on events from Feb 1–11, 2026", "10 sources cited", "~10 min read"],
    filename     = "001-ai-built-itself.png",
)

# ────────────────────────────────────────────
# Index / Homepage
# ────────────────────────────────────────────
draw_og(
    title_bold   = "AI Pulse",
    title_italic = "What's Happening in AI, Explained Simply",
    subtitle     = "A portal for AI updates. Weekly deep-dives into the developments reshaping technology, markets, and how we work — explained honestly.",
    tags         = "Weekly Publication  ·  Deep Analysis  ·  No Hype",
    meta_lines   = ["jeev-jo.github.io/ai-pulse", "New issues every week"],
    filename     = "index.png",
)

print("\nAll OG images generated in ./og/")
