import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

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
        "card_inner_bg": "#FAFAFA"
    }
}

def render_svg(theme):
    colors = PALETTES[theme]
    
    # Text styles
    hdr = f'font-family="{MONO_FONT}" font-size="12" font-weight="bold" fill="{colors["accent_cyan"]}" letter-spacing="1.5"'
    hdr_right = f'font-family="{MONO_FONT}" font-size="12" font-weight="bold" fill="{colors["accent_cyan"]}" letter-spacing="1.5" text-anchor="end"'
    title = f'font-family="{SERIF_FONT}" font-size="40" font-weight="bold" fill="{colors["text_primary"]}" letter-spacing="-0.5"'
    subtitle = f'font-family="{SYSTEM_FONT}" font-style="italic" font-size="18" fill="{colors["text_secondary"]}"'
    subhdr = f'font-family="{SERIF_FONT}" font-size="16" font-weight="bold" fill="{colors["text_primary"]}" letter-spacing="2"'
    body = f'font-family="{SYSTEM_FONT}" font-size="18" font-weight="400" fill="{colors["text_primary"]}"'
    
    # Focus boxes
    def focus_box(x, y, num, title_text, desc_text):
        return f"""
        <rect x="{x}" y="{y}" width="300" height="70" rx="4" fill="{colors["card_inner_bg"]}" stroke="{colors["border"]}" stroke-width="1" />
        <text x="{x + 20}" y="{y + 28}" font-family="{MONO_FONT}" font-size="16" font-weight="bold" fill="{colors["accent_cyan"]}">{num}</text>
        <text x="{x + 50}" y="{y + 28}" font-family="{SERIF_FONT}" font-size="16" font-weight="bold" fill="{colors["text_primary"]}">{title_text}</text>
        <text x="{x + 50}" y="{y + 50}" font-family="{SYSTEM_FONT}" font-size="15" fill="{colors["text_secondary"]}">{desc_text}</text>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 700" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="10" flood-opacity="{0.3 if theme == 'dark' else 0.04}" flood-color="#000000" />
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="800" height="700" fill="{colors["bg_base"]}" />
  
  <!-- Profile Container -->
  <rect x="40" y="20" width="720" height="660" rx="4" fill="{colors["bg_surface"]}" stroke="{colors["border"]}" stroke-width="1" filter="url(#shadow)" />

  <g transform="translate(90, 60)">
    <!-- Header -->
    <text x="0" y="0" {hdr}>✦ ABOUT ME</text>
    <text x="620" y="0" {hdr_right}>01 / PROFILE</text>
    
    <line x1="0" y1="15" x2="620" y2="15" stroke="{colors["border"]}" stroke-width="1" />
    
    <!-- Title Section -->
    <text x="0" y="65" {title}>Erolla Rishvin Reddy</text>
    <text x="0" y="95" {subtitle}>Computer Science &amp; Engineering · Class of 2028</text>
    <text x="0" y="120" {subtitle}>Woxsen University</text>
    
    <!-- Specialization -->
    <text x="0" y="170" {subhdr}>SPECIALIZATION</text>
    
    <g transform="translate(0, 190)">
      <rect x="0" y="0" width="105" height="28" rx="2" fill="{colors["accent_blue"]}" fill-opacity="0.1" stroke="{colors["accent_cyan"]}" stroke-width="1"/>
      <text x="52.5" y="18" font-family="{MONO_FONT}" font-size="13" font-weight="bold" fill="{colors["accent_cyan"]}" text-anchor="middle">BLOCKCHAIN</text>
      
      <rect x="115" y="0" width="55" height="28" rx="2" fill="{colors["accent_blue"]}" fill-opacity="0.1" stroke="{colors["accent_cyan"]}" stroke-width="1"/>
      <text x="142.5" y="18" font-family="{MONO_FONT}" font-size="13" font-weight="bold" fill="{colors["accent_cyan"]}" text-anchor="middle">IoT</text>
      
      <rect x="180" y="0" width="135" height="28" rx="2" fill="{colors["accent_blue"]}" fill-opacity="0.1" stroke="{colors["accent_cyan"]}" stroke-width="1"/>
      <text x="247.5" y="18" font-family="{MONO_FONT}" font-size="13" font-weight="bold" fill="{colors["accent_cyan"]}" text-anchor="middle">CYBERSECURITY</text>
    </g>
    
    <!-- Bio Paragraph -->
    <text x="0" y="260" {body}>I build across the hardware-to-software spectrum — from embedded prototypes</text>
    <text x="0" y="285" {body}>and sensor-driven automation to backend systems, web applications, security</text>
    <text x="0" y="310" {body}>tooling, and blockchain-oriented engineering projects.</text>
    
    <!-- Engineering Focus -->
    <text x="0" y="365" {subhdr}>ENGINEERING FOCUS</text>
    
    {focus_box(0, 385, "01", "Cybersecurity", "Network Security &amp; Tools")}
    {focus_box(320, 385, "02", "IoT / Embedded", "Sensor Systems &amp; Automation")}
    {focus_box(0, 470, "03", "Blockchain", "Applied Decentralized Systems")}
    {focus_box(320, 470, "04", "Full-Stack", "Backend Systems &amp; APIs")}
    
    <!-- Quote -->
    <line x1="0" y1="565" x2="0" y2="605" stroke="{colors["accent_cyan"]}" stroke-width="4" />
    <text x="20" y="582" font-family="{SYSTEM_FONT}" font-style="italic" font-size="20" fill="{colors["text_primary"]}">"I do not just write code.</text>
    <text x="20" y="605" font-family="{SERIF_FONT}" font-weight="bold" font-size="20" fill="{colors["text_primary"]}">I design systems that solve real problems."</text>
  </g>
</svg>"""
    return svg

def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    light_svg = render_svg("light")
    dark_svg = render_svg("dark")
    
    with open(os.path.join(ASSETS_DIR, "about_light.svg"), "w", encoding="utf-8") as f:
        f.write(light_svg)
        
    with open(os.path.join(ASSETS_DIR, "about_dark.svg"), "w", encoding="utf-8") as f:
        f.write(dark_svg)
        
    print("[INFO] Generated about_light.svg and about_dark.svg")

if __name__ == "__main__":
    main()
