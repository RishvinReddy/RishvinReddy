import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

SYSTEM_FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
MONO_FONT = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"

PALETTES = {
    "dark": {
        "bg_base": "#000000",
        "bg_surface": "#000000",
        "border": "#1E293B",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "accent_cyan": "#38BDF8",
        "accent_blue": "#1D4ED8",
        "accent_dim": "#334155"
    },
    "light": {
        "bg_base": "#000000",
        "bg_surface": "#000000",
        "border": "#CBD5E1",
        "text_primary": "#0F172A",
        "text_secondary": "#475569",
        "accent_cyan": "#0284C7",
        "accent_blue": "#1D4ED8",
        "accent_dim": "#CBD5E1"
    }
}

def render_svg(theme):
    colors = PALETTES[theme]
    
    # Text styles
    hdr = f'font-family="{MONO_FONT}" font-size="14" font-weight="600" fill="{colors["accent_cyan"]}" letter-spacing="2"'
    hdr_right = f'font-family="{MONO_FONT}" font-size="14" font-weight="600" fill="{colors["text_secondary"]}" letter-spacing="2" text-anchor="end"'
    title = f'font-family="{SYSTEM_FONT}" font-size="28" font-weight="800" fill="{colors["text_primary"]}" letter-spacing="1"'
    subtitle = f'font-family="{MONO_FONT}" font-size="16" font-weight="500" fill="{colors["text_secondary"]}"'
    subhdr = f'font-family="{MONO_FONT}" font-size="14" font-weight="600" fill="{colors["text_secondary"]}" letter-spacing="1.5"'
    body = f'font-family="{SYSTEM_FONT}" font-size="16" font-weight="400" fill="{colors["text_secondary"]}" line-height="1.5"'
    
    # Focus boxes
    def focus_box(x, y, num, title_text, desc_text):
        return f"""
        <rect x="{x}" y="{y}" width="330" height="70" rx="8" fill="transparent" stroke="{colors["border"]}" stroke-width="1.5" />
        <text x="{x + 16}" y="{y + 30}" font-family="{MONO_FONT}" font-size="14" font-weight="700" fill="{colors["accent_cyan"]}">{num}</text>
        <text x="{x + 46}" y="{y + 30}" font-family="{SYSTEM_FONT}" font-size="15" font-weight="700" fill="{colors["text_primary"]}">{title_text}</text>
        <text x="{x + 46}" y="{y + 52}" font-family="{SYSTEM_FONT}" font-size="14" font-weight="400" fill="{colors["text_secondary"]}">{desc_text}</text>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 680" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{colors["bg_surface"]}" />
      <stop offset="100%" stop-color="{colors["bg_base"]}" />
    </linearGradient>
  </defs>
  
  <rect x="0" y="0" width="800" height="680" rx="16" fill="url(#bgGradient)" stroke="{colors["border"]}" stroke-width="1.5"/>
  
  <!-- Subtle Grid Pattern Background -->
  <line x1="0" y1="60" x2="800" y2="60" stroke="{colors["border"]}" stroke-width="1" stroke-dasharray="4 4" opacity="0.5"/>
  
  <g transform="translate(48, 40)">
    <!-- Header -->
    <text x="0" y="0" {hdr}>✦ ABOUT ME</text>
    <text x="704" y="0" {hdr_right}>01 / PROFILE</text>
    
    <!-- Title Section -->
    <text x="0" y="56" {title}>EROLLA RISHVIN REDDY</text>
    <text x="0" y="86" {subtitle}>Computer Science &amp; Engineering · Class of 2028</text>
    <text x="0" y="110" {subtitle}>Woxsen University</text>
    
    <!-- Specialization -->
    <text x="0" y="160" {subhdr}>SPECIALIZATION</text>
    
    <g transform="translate(0, 180)">
      <rect x="0" y="0" width="126" height="30" rx="4" fill="{colors["accent_blue"]}" fill-opacity="0.1" stroke="{colors["accent_cyan"]}" stroke-width="1"/>
      <text x="63" y="19" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{colors["accent_cyan"]}" text-anchor="middle">BLOCKCHAIN</text>
      
      <rect x="142" y="0" width="70" height="30" rx="4" fill="{colors["accent_blue"]}" fill-opacity="0.1" stroke="{colors["accent_cyan"]}" stroke-width="1"/>
      <text x="177" y="19" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{colors["accent_cyan"]}" text-anchor="middle">IoT</text>
      
      <rect x="228" y="0" width="150" height="30" rx="4" fill="{colors["accent_blue"]}" fill-opacity="0.1" stroke="{colors["accent_cyan"]}" stroke-width="1"/>
      <text x="303" y="19" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{colors["accent_cyan"]}" text-anchor="middle">CYBERSECURITY</text>
    </g>
    
    <!-- Bio Paragraph -->
    <text x="0" y="250" {body}>I build across the hardware-to-software spectrum —</text>
    <text x="0" y="274" {body}>from embedded prototypes and sensor-driven automation</text>
    <text x="0" y="298" {body}>to backend systems, web applications, security tooling,</text>
    <text x="0" y="322" {body}>and blockchain-oriented engineering projects.</text>
    
    <!-- Engineering Focus -->
    <text x="0" y="380" {subhdr}>ENGINEERING FOCUS</text>
    {focus_box(0, 400, "01", "CYBERSECURITY", "Network Security &amp; Tools")}
    {focus_box(350, 400, "02", "IoT / EMBEDDED", "Sensor Systems &amp; Automation")}
    {focus_box(0, 486, "03", "BLOCKCHAIN", "Applied Decentralized Systems")}
    {focus_box(350, 486, "04", "FULL-STACK", "Backend Systems &amp; APIs")}
    
    <!-- Quote -->
    <line x1="0" y1="586" x2="4" y2="586" stroke="{colors["accent_cyan"]}" stroke-width="4" />
    <line x1="2" y1="586" x2="2" y2="626" stroke="{colors["accent_cyan"]}" stroke-width="4" />
    
    <text x="24" y="602" font-family="{SYSTEM_FONT}" font-size="16" font-weight="400" font-style="italic" fill="{colors["text_primary"]}">"I do not just write code.</text>
    <text x="24" y="626" font-family="{SYSTEM_FONT}" font-size="16" font-weight="700" font-style="italic" fill="{colors["text_primary"]}">I design systems that solve real problems."</text>
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
