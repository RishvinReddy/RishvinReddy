import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "cards")

SYSTEM_FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
MONO_FONT = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"

PALETTES = {
    "dark": {
        "bg_base": "#020617",
        "bg_surface": "#0C1527",
        "border": "#1E293B",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "accent_cyan": "#38BDF8",
        "accent_blue": "#1D4ED8",
        "accent_green": "#22C55E",
        "accent_purple": "#A78BFA"
    },
    "light": {
        "bg_base": "#F8FAFC",
        "bg_surface": "#FFFFFF",
        "border": "#CBD5E1",
        "text_primary": "#0F172A",
        "text_secondary": "#475569",
        "accent_cyan": "#0284C7",
        "accent_blue": "#1D4ED8",
        "accent_green": "#15803D",
        "accent_purple": "#7C3AED"
    }
}

def svg_base(width, height, theme, content):
    c = PALETTES[theme]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c['bg_surface']}" />
      <stop offset="100%" stop-color="{c['bg_base']}" />
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" rx="12" fill="url(#bg)" stroke="{c['border']}" stroke-width="1.5"/>
  <line x1="0" y1="50" x2="{width}" y2="50" stroke="{c['border']}" stroke-width="1" stroke-dasharray="4 4" opacity="0.6"/>
  {content}
</svg>"""

def render_philosophy(theme):
    c = PALETTES[theme]
    hdr = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["accent_cyan"]}" letter-spacing="2">✦ ENGINEERING PHILOSOPHY</text>'
    
    stages = ["PROBLEM", "ARCHITECTURE", "IMPLEMENTATION", "SECURITY", "VALIDATION", "IMPACT"]
    pipeline = ""
    x_offset = 32
    for i, stage in enumerate(stages):
        # Box
        w = len(stage) * 8 + 30
        pipeline += f'<rect x="{x_offset}" y="80" width="{w}" height="28" rx="4" fill="{c["accent_blue"]}" fill-opacity="0.1" stroke="{c["accent_cyan"]}" stroke-width="1"/>'
        pipeline += f'<text x="{x_offset + w/2}" y="99" font-family="{MONO_FONT}" font-size="12" font-weight="600" fill="{c["accent_cyan"]}" text-anchor="middle">{stage}</text>'
        x_offset += w
        if i < len(stages) - 1:
            pipeline += f'<text x="{x_offset + 12}" y="99" font-family="{MONO_FONT}" font-size="12" fill="{c["text_secondary"]}">──▶</text>'
            x_offset += 34
            
    statements = [
        "Code is an implementation detail. Architecture determines how the system evolves.",
        "Security determines how the system survives.",
        "Validation determines whether the system can be trusted.",
        "Impact determines whether the system was worth building."
    ]
    
    body = f'<rect x="32" y="140" width="736" height="110" rx="8" fill="transparent" stroke="{c["border"]}" stroke-width="1"/>'
    for i, s in enumerate(statements):
        body += f'<text x="56" y="{170 + i*24}" font-family="{MONO_FONT}" font-size="13" fill="{c["text_secondary"]}">{s}</text>'
        
    return svg_base(800, 282, theme, hdr + pipeline + body)

def render_labs(theme):
    c = PALETTES[theme]
    hdr = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["accent_purple"]}" letter-spacing="2">✦ RISHVIN LABS</text>'
    
    status = f"""
    <circle cx="630" cy="28" r="4" fill="{c["accent_green"]}"/>
    <text x="644" y="32" font-family="{MONO_FONT}" font-size="12" font-weight="600" fill="{c["accent_green"]}" letter-spacing="1">FOUNDER / BUILDER</text>
    """
    
    title = f'<text x="32" y="100" font-family="{SYSTEM_FONT}" font-size="28" font-weight="800" fill="{c["text_primary"]}">Rishvin Labs</text>'
    mission = f'<text x="32" y="140" font-family="{SYSTEM_FONT}" font-size="16" font-weight="400" fill="{c["text_secondary"]}">Engineering-focused initiative for useful, secure, and scalable systems.</text>'
    
    domains_txt = "Software Systems  •  Web Engineering  •  IoT Solutions  •  Cybersecurity  •  Automation"
    domains = f"""
    <rect x="32" y="170" width="736" height="40" rx="6" fill="{c["accent_blue"]}" fill-opacity="0.05" stroke="{c["border"]}" stroke-width="1"/>
    <text x="400" y="195" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["text_primary"]}" text-anchor="middle">{domains_txt}</text>
    """
    
    return svg_base(800, 250, theme, hdr + status + title + mission + domains)

def render_academic(theme):
    c = PALETTES[theme]
    hdr = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["accent_blue"]}" letter-spacing="2">✦ ACADEMIC JOURNEY</text>'
    
    stats = f"""
    <rect x="520" y="16" width="248" height="26" rx="4" fill="{c["border"]}" fill-opacity="0.3"/>
    <text x="644" y="33" font-family="{MONO_FONT}" font-size="12" font-weight="600" fill="{c["text_primary"]}" text-anchor="middle">B.TECH CSE · CLASS OF 2028</text>
    """
    
    modules = [
        ("01", "CYBERSECURITY", "Network Security, Cryptography"),
        ("02", "INTERNET OF THINGS", "Sensors, Embedded Systems"),
        ("03", "BLOCKCHAIN", "Distributed Systems, Architecture"),
        ("04", "ALGORITHMS", "Data Structures, Complexity"),
        ("05", "SYSTEMS", "Operating Systems, Databases"),
        ("06", "SOFTWARE ENG", "Web Systems, APIs, Deployment")
    ]
    
    grid = ""
    for i, mod in enumerate(modules):
        x = 32 + (i % 3) * 245
        y = 75 + (i // 3) * 75
        grid += f"""
        <rect x="{x}" y="{y}" width="230" height="60" rx="6" fill="transparent" stroke="{c["border"]}" stroke-width="1"/>
        <text x="{x+12}" y="{y+26}" font-family="{MONO_FONT}" font-size="12" font-weight="700" fill="{c["accent_cyan"]}">{mod[0]}</text>
        <text x="{x+36}" y="{y+26}" font-family="{SYSTEM_FONT}" font-size="13" font-weight="700" fill="{c["text_primary"]}">{mod[1]}</text>
        <text x="{x+12}" y="{y+46}" font-family="{SYSTEM_FONT}" font-size="12" fill="{c["text_secondary"]}">{mod[2]}</text>
        """
        
    cgpa = f'<text x="32" y="250" font-family="{MONO_FONT}" font-size="14" font-weight="600" fill="{c["accent_blue"]}">CGPA: 9.01 / 10</text>'
    
    return svg_base(800, 280, theme, hdr + stats + grid + cgpa)

def render_opento(theme):
    c = PALETTES[theme]
    hdr = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["accent_green"]}" letter-spacing="2">✦ OPPORTUNITIES</text>'
    
    status = f"""
    <circle cx="580" cy="28" r="4" fill="{c["accent_green"]}">
      <animate attributeName="opacity" values="1;0;1" dur="2s" repeatCount="indefinite" />
    </circle>
    <text x="594" y="32" font-family="{MONO_FONT}" font-size="12" font-weight="600" fill="{c["accent_green"]}" letter-spacing="1">OPEN TO OPPORTUNITIES</text>
    """
    
    desc = f"""
    <text x="32" y="90" font-family="{SYSTEM_FONT}" font-size="16" fill="{c["text_secondary"]}">I am particularly interested in opportunities where I can contribute to:</text>
    """
    
    tags = ["Cybersecurity", "IoT Engineering", "Blockchain Systems", "Backend Engineering", "Full-Stack Systems", "Engineering Automation"]
    tag_svg = ""
    x = 32
    for t in tags:
        w = len(t) * 9 + 20
        tag_svg += f'<rect x="{x}" y="115" width="{w}" height="32" rx="16" fill="{c["border"]}" fill-opacity="0.2" stroke="{c["border"]}" stroke-width="1"/>'
        tag_svg += f'<text x="{x + w/2}" y="136" font-family="{MONO_FONT}" font-size="13" font-weight="500" fill="{c["text_primary"]}" text-anchor="middle">{t}</text>'
        x += w + 12
        
    return svg_base(800, 180, theme, hdr + status + desc + tag_svg)

def render_connect(theme):
    c = PALETTES[theme]
    hdr = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["text_primary"]}" letter-spacing="2">✦ CONNECT</text>'
    
    name = f'<text x="32" y="95" font-family="{SYSTEM_FONT}" font-size="24" font-weight="800" fill="{c["text_primary"]}">Erolla Rishvin Reddy</text>'
    focus = f'<text x="32" y="125" font-family="{MONO_FONT}" font-size="14" fill="{c["text_secondary"]}">Software Engineering • Cybersecurity • IoT</text>'
    
    endpoints = [
        ("GITHUB", "github.com/RishvinReddy"),
        ("LINKEDIN", "linkedin.com/in/rishvin-reddy"),
        ("EMAIL", "rishvin18@gmail.com")
    ]
    
    end_svg = ""
    for i, (k, v) in enumerate(endpoints):
        y = 75 + i*28
        end_svg += f'<text x="450" y="{y}" font-family="{MONO_FONT}" font-size="13" font-weight="700" fill="{c["accent_cyan"]}">{k}</text>'
        end_svg += f'<text x="540" y="{y}" font-family="{MONO_FONT}" font-size="13" fill="{c["text_primary"]}">{v}</text>'
        
    return svg_base(800, 160, theme, hdr + name + focus + end_svg)

def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    cards = {
        "engineering_philosophy": render_philosophy,
        "rishvin_labs": render_labs,
        "academic_journey": render_academic,
        "open_to": render_opento,
        "connect": render_connect
    }
    
    for name, func in cards.items():
        for theme in ["light", "dark"]:
            filename = f"{name}_{theme}.svg"
            filepath = os.path.join(ASSETS_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(func(theme))
            print(f"[INFO] Generated {filename}")

if __name__ == "__main__":
    main()
