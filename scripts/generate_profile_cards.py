import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "cards")

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
        "accent_green": "#22C55E",
        "accent_purple": "#A78BFA"
    },
    "light": {
        "bg_base": "#000000",
        "bg_surface": "#000000",
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
        ("EMAIL", "rishvinreddy@gmail.com")
    ]
    
    end_svg = ""
    for i, (k, v) in enumerate(endpoints):
        y = 75 + i*28
        end_svg += f'<text x="450" y="{y}" font-family="{MONO_FONT}" font-size="13" font-weight="700" fill="{c["accent_cyan"]}">{k}</text>'
        end_svg += f'<text x="540" y="{y}" font-family="{MONO_FONT}" font-size="13" fill="{c["text_primary"]}">{v}</text>'
        
    return svg_base(800, 160, theme, hdr + name + focus + end_svg)

def render_direction(theme):
    c = PALETTES[theme]
    hdr = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["accent_cyan"]}" letter-spacing="2">✦ ENGINEERING DIRECTION</text>'
    
    tracks = [
        ("01", "SECURITY", "Secure Architectures • Network Analysis • Security Automation"),
        ("02", "EMBEDDED", "Sensor-Driven IoT • ESP32 Systems • Hardware-Software Integration"),
        ("03", "BLOCKCHAIN", "Applied Blockchain Engineering • Distributed Systems"),
        ("04", "SOFTWARE", "Backend APIs • Full-Stack Systems • Modular Architecture"),
        ("05", "AUTOMATION", "n8n Workflows • Engineering Automation • AI-Assisted Systems"),
        ("06", "GROWTH", "Production Engineering • Deployment • Open Source • Research")
    ]
    
    grid = ""
    for i, tr in enumerate(tracks):
        x = 32 + (i % 2) * 380
        y = 70 + (i // 2) * 65
        grid += f"""
        <rect x="{x}" y="{y}" width="350" height="50" rx="6" fill="{c["border"]}" fill-opacity="0.1" stroke="{c["border"]}" stroke-width="1"/>
        <text x="{x+16}" y="{y+20}" font-family="{MONO_FONT}" font-size="12" font-weight="700" fill="{c["accent_cyan"]}">{tr[0]}</text>
        <text x="{x+42}" y="{y+20}" font-family="{MONO_FONT}" font-size="13" font-weight="700" fill="{c["text_primary"]}" letter-spacing="1">{tr[1]}</text>
        <text x="{x+16}" y="{y+40}" font-family="{SYSTEM_FONT}" font-size="11" fill="{c["text_secondary"]}">{tr[2]}</text>
        """
        
    return svg_base(800, 280, theme, hdr + grid)


def render_engineering_profile(theme):
    c = PALETTES[theme]
    hdr = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["accent_cyan"]}" letter-spacing="2">✦ ENGINEERING PROFILE</text>'
    
    data = [
        ("Name", "Erolla Rishvin Reddy"),
        ("Degree", "B.Tech in Computer Science and Engineering"),
        ("Specialization", "Blockchain • IoT • Cybersecurity"),
        ("University", "Woxsen University"),
        ("Class", "2028"),
        ("CGPA", "9.01 / 10"),
        ("Career Track", "Industry-Oriented Engineering"),
        ("Core Focus", "Secure Systems • IoT • Blockchain • Full-Stack"),
        ("Mindset", "Build useful systems. Secure them. Document them. Improve them.")
    ]
    
    grid = ""
    for i, (k, v) in enumerate(data):
        y = 75 + i*28
        grid += f'<text x="32" y="{y}" font-family="{MONO_FONT}" font-size="13" font-weight="700" fill="{c["accent_cyan"]}">{k}</text>'
        if k == "Mindset":
            grid += f'<text x="220" y="{y}" font-family="{SYSTEM_FONT}" font-style="italic" font-size="14" fill="{c["text_primary"]}">{v}</text>'
        else:
            grid += f'<text x="220" y="{y}" font-family="{MONO_FONT}" font-size="13" fill="{c["text_primary"]}">{v}</text>'
            
    return svg_base(800, 340, theme, hdr + grid)

def render_what_i_build(theme):
    c = PALETTES[theme]
    hdr = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["accent_cyan"]}" letter-spacing="2">✦ WHAT I BUILD</text>'
    
    blocks = [
        ("🔐 Security Systems", ["Network analysis", "Security automation", "Attack-surface workflows", "Authentication systems", "Threat-aware architectures"]),
        ("🔌 IoT Systems", ["Arduino prototypes", "ESP32 systems", "Sensor integration", "Embedded automation", "Hardware-software workflows"]),
        ("⛓️ Blockchain Systems", ["Blockchain applications", "Decentralized concepts", "Secure transaction logic", "Applied distributed systems", "Research-driven prototypes"]),
        ("🌐 Software Systems", ["Backend services", "Web applications", "REST APIs", "Database-backed platforms", "Automation workflows"])
    ]
    
    grid = ""
    for i, (title, items) in enumerate(blocks):
        x = 32 + (i % 2) * 380
        y = 70 + (i // 2) * 140
        grid += f'<rect x="{x}" y="{y}" width="350" height="120" rx="6" fill="{c["border"]}" fill-opacity="0.1" stroke="{c["border"]}" stroke-width="1"/>'
        grid += f'<text x="{x+16}" y="{y+24}" font-family="{SYSTEM_FONT}" font-size="14" font-weight="700" fill="{c["text_primary"]}">{title}</text>'
        
        for j, item in enumerate(items):
            grid += f'<text x="{x+16}" y="{y+46 + j*16}" font-family="{MONO_FONT}" font-size="11" fill="{c["text_secondary"]}">> {item}</text>'
            
    return svg_base(800, 380, theme, hdr + grid)

def render_technical_domains(theme):
    c = PALETTES[theme]
    hdr = f'<text x="32" y="32" font-family="{MONO_FONT}" font-size="13" font-weight="600" fill="{c["accent_cyan"]}" letter-spacing="2">✦ TECHNICAL DOMAINS</text>'
    
    domains = [
        ("01", "CYBERSECURITY", "Network Security • Traffic Analysis • IDS Concepts • Cryptography"),
        ("02", "IOT &amp; EMBEDDED", "Arduino • ESP32 • Sensors • Actuators • Embedded Prototyping"),
        ("03", "BLOCKCHAIN", "Blockchain Fundamentals • Distributed Systems • Decentralized Architecture"),
        ("04", "FULL-STACK", "HTML • CSS • JavaScript • Backend Logic • APIs • Database Integration"),
        ("05", "BACKEND SYSTEMS", "Python • Flask • FastAPI • REST APIs • Modular Application Logic"),
        ("06", "DSA &amp; ALGORITHMS", "Tries • KMP • Search Algorithms • Scheduling Algorithms"),
        ("07", "INTELLIGENT SYSTEMS", "AI-Assisted Automation • OpenCV • Applied ML Integration")
    ]
    
    grid = ""
    for i, tr in enumerate(domains):
        x = 32 + (i % 2) * 380
        y = 70 + (i // 2) * 65
        grid += f'<rect x="{x}" y="{y}" width="350" height="50" rx="6" fill="{c["border"]}" fill-opacity="0.1" stroke="{c["border"]}" stroke-width="1"/>'
        grid += f'<text x="{x+16}" y="{y+20}" font-family="{MONO_FONT}" font-size="12" font-weight="700" fill="{c["accent_cyan"]}">{tr[0]}</text>'
        grid += f'<text x="{x+42}" y="{y+20}" font-family="{MONO_FONT}" font-size="13" font-weight="700" fill="{c["text_primary"]}" letter-spacing="1">{tr[1]}</text>'
        grid += f'<text x="{x+16}" y="{y+40}" font-family="{SYSTEM_FONT}" font-size="11" fill="{c["text_secondary"]}">{tr[2]}</text>'
        
    return svg_base(800, 350, theme, hdr + grid)

def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    cards = {
        "engineering_philosophy": render_philosophy,
        "rishvin_labs": render_labs,
        "academic_journey": render_academic,
        "open_to": render_opento,
        "connect": render_connect,
        "engineering_direction": render_direction,
        "engineering_profile": render_engineering_profile,
        "what_i_build": render_what_i_build,
        "technical_domains": render_technical_domains
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
