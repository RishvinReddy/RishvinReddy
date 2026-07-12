import os
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYTICS_DIR = os.path.join(BASE_DIR, "assets", "analytics")

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
        "accent_purple": "#C678DD"
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
        "accent_purple": "#6D28D9"
    }
}

URLS = {
    "views": "https://komarev.com/ghpvc/?username=RishvinReddy&label=PROFILE%20VIEWS&color=0ea5e9&style=for-the-badge",
    "profile_details": "https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=RishvinReddy&theme=tokyonight",
    "stats": "https://github-profile-summary-cards.vercel.app/api/cards/stats?username=RishvinReddy&theme=tokyonight",
    "repos_per_language": "https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=RishvinReddy&theme=tokyonight",
    "most_commit_language": "https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=RishvinReddy&theme=tokyonight",
    "productive_time": "https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=RishvinReddy&theme=tokyonight&utcOffset=5.5",
    "trophies": "https://github-profile-trophy.vercel.app/?username=RishvinReddy&theme=algolia&no-frame=true&margin-w=15&margin-h=15&row=1&column=6",
    "activity_graph": "https://github-readme-activity-graph.vercel.app/graph?username=RishvinReddy&theme=tokyo-night&hide_border=true&area=true"
}

def fetch_svg(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def process_svg(svg_content, theme):
    c = PALETTES[theme]
    
    # Universal Font replacements
    svg_content = re.sub(r'font-family:[^;"]+', f'font-family: \'Times New Roman\', Times, serif', svg_content)
    svg_content = re.sub(r'font-family="[^"]+"', f'font-family="\'Times New Roman\', Times, serif"', svg_content)
    
    # We can add Georgia for specific large texts if needed, but Times New Roman is enough for data.
    
    # Specific color replacements for TokyoNight / Algolia
    # Backgrounds
    svg_content = re.sub(r'(?i)(fill|stroke|stop-color)="?#1a1b27"?', r'\1="' + c["bg_surface"] + '"', svg_content)
    svg_content = re.sub(r'(?i)(fill|stroke|stop-color)="?#050f2c"?', r'\1="' + c["bg_surface"] + '"', svg_content)
    
    # Primary Text (titles)
    svg_content = re.sub(r'(?i)(fill|stroke|stop-color)="?#70a5fd"?', r'\1="' + c["accent_cyan"] + '"', svg_content)
    svg_content = re.sub(r'(?i)(fill|stroke|stop-color)="?#00aeff"?', r'\1="' + c["accent_cyan"] + '"', svg_content)
    
    # Secondary Text (stats/labels)
    svg_content = re.sub(r'(?i)(fill|stroke|stop-color)="?#38bdae"?', r'\1="' + c["text_secondary"] + '"', svg_content)
    svg_content = re.sub(r'(?i)(fill|stroke|stop-color)="?#8be9fd"?', r'\1="' + c["text_secondary"] + '"', svg_content)
    
    # Icons / Trophies
    svg_content = re.sub(r'(?i)(fill|stroke|stop-color)="?#bf91f3"?', r'\1="' + c["accent_purple"] + '"', svg_content)
    
    # Views Badge
    svg_content = re.sub(r'(?i)(fill|stroke|stop-color)="?#0ea5e9"?', r'\1="' + c["accent_cyan"] + '"', svg_content)
    svg_content = re.sub(r'(?i)(fill|stroke|stop-color)="?#555"?', r'\1="' + c["border"] + '"', svg_content)

    # Make trophies background transparent if they have it
    # Trophies are returned wrapped in SVGs
    
    return svg_content

def main():
    os.makedirs(ANALYTICS_DIR, exist_ok=True)
    
    for name, url in URLS.items():
        print(f"Fetching {name}...")
        raw_svg = fetch_svg(url)
        if not raw_svg:
            continue
            
        for theme in ["light", "dark"]:
            themed_svg = process_svg(raw_svg, theme)
            file_path = os.path.join(ANALYTICS_DIR, f"{name}_{theme}.svg")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(themed_svg)
            print(f"  -> Generated {file_path}")

if __name__ == "__main__":
    main()
