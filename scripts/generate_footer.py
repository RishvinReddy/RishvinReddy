import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "cards")

SYSTEM_FONT = "'Times New Roman', Times, serif"
MONO_FONT = "'Courier New', Courier, monospace"
SERIF_FONT = "Georgia, serif"


PALETTES = {
    "dark": {
        "bg_base": "#0B0C10",
        "bg_surface": "#15171E",
        "border": "#2B2F3A",
        "text_primary": "#FFFFFF",
        "text_secondary": "#8B92A5",
        "accent_cyan": "#56B6C2",
    },
    "light": {
        "bg_base": "#F7F7F8",
        "bg_surface": "#FFFFFF",
        "border": "#E2E8F0",
        "text_primary": "#1A202C",
        "text_secondary": "#4A5568",
        "accent_cyan": "#2C5282",
    }
}

def svg_base(width, height, theme, content):
    c = PALETTES[theme]
    full_width = width + 80
    full_height = height + 40
    shadow_opacity = 0.3 if theme == "dark" else 0.04
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {full_width} {full_height}" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="10" flood-opacity="{shadow_opacity}" flood-color="#000000" />
    </filter>
  </defs>
  <rect x="0" y="0" width="{full_width}" height="{full_height}" fill="{c["bg_base"]}" />
  <rect x="40" y="20" width="{width}" height="{height}" rx="4" fill="{c["bg_surface"]}" stroke="{c["border"]}" stroke-width="1" filter="url(#shadow)"/>
  <g transform="translate(40, 20)">
    {content}
  </g>
</svg>"""


def render_footer(theme):
    c = PALETTES[theme]
    
    # We will center the text in a 800x80 card
    content = f"""
    <text x="400" y="47" font-family="{SERIF_FONT}" font-weight="bold" font-size="20" fill="{c['text_primary']}" letter-spacing="1" text-anchor="middle">Secure systems. Scalable engineering. Real-world impact.</text>
    """
    return svg_base(800, 80, theme, content)

def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    for theme in ["light", "dark"]:
        with open(os.path.join(ASSETS_DIR, f"footer_{theme}.svg"), "w") as f:
            f.write(render_footer(theme))
            print(f"Generated footer_{theme}.svg")

if __name__ == "__main__":
    main()
