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
        "accent_blue": "#61AFEF",
        "accent_green": "#98C379",
        "accent_purple": "#C678DD",
        "card_inner_bg": "#1E212B",
        "surface_elevated": "#1E212B"
    },
    "light": {
        "bg_base": "#F7F7F8",
        "bg_surface": "#FFFFFF",
        "border": "#E2E8F0",
        "text_primary": "#1A202C",
        "text_secondary": "#4A5568",
        "accent_cyan": "#2C5282",
        "accent_blue": "#EBF8FF",
        "accent_green": "#059669",
        "accent_purple": "#6D28D9",
        "card_inner_bg": "#FAFAFA",
        "surface_elevated": "#FAFAFA"
    }
}

CATEGORIES = [
    {"id": "01", "name": "LANGUAGES", "items": ["Python", "JavaScript", "C", "Java", "SQL"]},
    {"id": "02", "name": "WEB ENGINEERING", "items": ["HTML5", "CSS3", "Flask", "FastAPI", "PHP", "Node.js"]},
    {"id": "03", "name": "IOT + EMBEDDED", "items": ["Arduino", "ESP32", "ESP8266", "Sensors", "Embedded Prototyping"]},
    {"id": "04", "name": "SECURITY", "items": ["Wireshark", "Snort", "Burp Suite", "Network Analysis", "Cryptography"]},
    {"id": "05", "name": "DATA + VISION", "items": ["NumPy", "OpenCV"]},
    {"id": "06", "name": "DATABASES", "items": ["MySQL", "SQLite", "PostgreSQL"]},
    {"id": "07", "name": "INFRA + AUTOMATION", "items": ["n8n", "Git", "Linux", "Docker"]},
    {"id": "08", "name": "DEPLOYMENT", "items": ["GitHub Pages", "Vercel", "XAMPP"]},
    {"id": "09", "name": "CURRENT FOCUS", "items": ["Cybersecurity", "IoT", "Blockchain", "Backend Systems"]}
]

def render_matrix(theme):
    c = PALETTES[theme]
    
    # SVG constraints
    width = 800
    height = 540
    
    hdr_left = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["accent_cyan"]}" letter-spacing="2">✦ ENGINEERING CAPABILITY MATRIX</text>'
    hdr_right = f'<text x="768" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["text_secondary"]}" letter-spacing="2" text-anchor="end">STACK / 2026</text>'
    subtitle = f'<text x="32" y="60" font-family="{SERIF_FONT}" font-size="14" font-weight="500" fill="{c["text_secondary"]}">Technologies across software, systems, security and connected engineering</text>'
    
    grid = ""
    start_x = 32
    start_y = 90
    box_w = 232
    box_h = 120
    gap_x = 20
    gap_y = 20
    
    for i, cat in enumerate(CATEGORIES):
        col = i % 3
        row = i // 3
        x = start_x + col * (box_w + gap_x)
        y = start_y + row * (box_h + gap_y)
        
        # Box background
        grid += f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="4" fill="{c['card_inner_bg']}" stroke="{c["border"]}" stroke-width="1.5"/>'
        
        # Header
        grid += f'<text x="{x+16}" y="{y+26}" font-family="{MONO_FONT}" font-size="12" font-weight="700" fill="{c["accent_cyan"]}">{cat["id"]}</text>'
        grid += f'<text x="{x+42}" y="{y+26}" font-family="{MONO_FONT}" font-size="13" font-weight="700" fill="{c["text_primary"]}" letter-spacing="1">{cat["name"]}</text>'
        
        # Items
        item_y = y + 50
        for item in cat["items"]:
            grid += f'<text x="{x+16}" y="{item_y}" font-family="{SYSTEM_FONT}" font-size="13" font-weight="500" fill="{c["text_secondary"]}">{item}</text>'
            item_y += 20
            
    footer_y = height - 24
    footer = f'<text x="400" y="{footer_y}" font-family="{MONO_FONT}" font-size="12" font-weight="600" fill="{c["text_secondary"]}" letter-spacing="2" text-anchor="middle">SOFTWARE  •  SECURITY  •  CONNECTED SYSTEMS  •  INFRASTRUCTURE</text>'
    
    full_width = width + 80
    full_height = height + 40
    shadow_opacity = 0.3 if theme == "dark" else 0.04
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {full_width} {full_height}" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="10" flood-opacity="{shadow_opacity}" flood-color="#000000" />
    </filter>
  </defs>
  <rect x="0" y="0" width="{full_width}" height="{full_height}" fill="{c['bg_base']}" />
  <rect x="40" y="20" width="{width}" height="{height}" rx="4" fill="{c['bg_surface']}" stroke="{c['border']}" stroke-width="1" filter="url(#shadow)"/>
  <g transform="translate(40, 20)">
    {hdr_left}
    {hdr_right}
    {subtitle}
    {grid}
    {footer}
  </g>
</svg>"""
    return svg

def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    light_svg = render_matrix("light")
    dark_svg = render_matrix("dark")
    
    with open(os.path.join(ASSETS_DIR, "tech_stack_light.svg"), "w", encoding="utf-8") as f:
        f.write(light_svg)
        
    with open(os.path.join(ASSETS_DIR, "tech_stack_dark.svg"), "w", encoding="utf-8") as f:
        f.write(dark_svg)
        
    print("[INFO] Generated tech_stack_light.svg and tech_stack_dark.svg")

if __name__ == "__main__":
    main()
