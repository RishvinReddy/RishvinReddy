import urllib.request
import json
import os
import html
import base64
from datetime import datetime, timezone
from pathlib import Path

USERNAME = "RishvinReddy"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CACHE_FILE = Path("cache/stats.json")

def get_base64_image(image_path="icon.png"):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"Error loading image: {e}")
        return ""

def fetch_github_data():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        req_user = urllib.request.Request(f"https://api.github.com/users/{USERNAME}", headers=headers)
        with urllib.request.urlopen(req_user, timeout=10) as response:
            user_data = json.loads(response.read().decode())
        
        req_repos = urllib.request.Request(f"https://api.github.com/users/{USERNAME}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(req_repos, timeout=10) as response:
            repos_data = json.loads(response.read().decode())

        stars = sum(repo.get('stargazers_count', 0) for repo in repos_data if not repo.get('fork', False))

        # Commits (search API)
        commits = 0
        try:
            req_commits = urllib.request.Request(f"https://api.github.com/search/commits?q=author:{USERNAME}", headers=headers)
            with urllib.request.urlopen(req_commits, timeout=10) as response:
                commits_data = json.loads(response.read().decode())
                commits = commits_data.get("total_count", 0)
        except Exception as ce:
            print(f"Could not fetch commits: {ce}")

        stats = {
            "repos": user_data.get("public_repos", 0),
            "commits": commits,
            "followers": user_data.get("followers", 0),
            "stars": stars
        }
        
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w") as f:
            json.dump(stats, f)
            
        return stats
    
    except Exception as e:
        print(f"Error fetching from GitHub API: {e}")
        if CACHE_FILE.exists():
            print("Loading from cache.")
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        else:
            print("No cache available. Using N/A.")
            return {"repos": "N/A", "commits": "N/A", "followers": "N/A", "stars": "N/A"}

def dotted_row(label, value, width=65):
    prefix = f"{label}: "
    dots = "." * max(2, width - len(prefix) - len(str(value)))
    return f"{prefix}{dots} {value}"

def generate_svg(stats, img_b64, is_dark_mode=True):
    bg_color = "#000000" if is_dark_mode else "#ffffff"
    text_color = "#c9d1d9" if is_dark_mode else "#24292f"
    accent_green = "#2ea043"
    accent_orange = "#d29922"
    accent_blue = "#58a6ff"
    dim_color = "#8b949e" if is_dark_mode else "#6e7781"

    svg_width = 1150
    svg_height = 540
    
    lines = [
        {"type": "header", "label": "rishvin@reddy", "value": "────────────────────────────────────────────────────", "color": accent_green},
        {"type": "empty"},
        {"type": "row", "label": "OS", "value": "macOS"},
        {"type": "row", "label": "Education", "value": "B.Tech CSE"},
        {"type": "row", "label": "University", "value": "Woxsen University"},
        {"type": "row", "label": "Track", "value": "Blockchain, IoT & Cybersecurity"},
        {"type": "row", "label": "CGPA", "value": "9.01 / 10"},
        {"type": "row", "label": "IDE", "value": "Antigravity IDE"},
        {"type": "empty"},
        {"type": "row", "label": "Languages.Programming", "value": "Java, Python, JavaScript, C/C++"},
        {"type": "row", "label": "Languages.Web", "value": "HTML, CSS, JavaScript"},
        {"type": "row", "label": "Technologies", "value": "IoT, Cybersecurity, Blockchain"},
        {"type": "row", "label": "Development", "value": "Full-Stack, Automation, Systems"},
        {"type": "empty"},
        {"type": "row", "label": "Focus.Security", "value": "Cybersecurity Engineering"},
        {"type": "row", "label": "Focus.Hardware", "value": "IoT & Embedded Systems"},
        {"type": "row", "label": "Focus.Web3", "value": "Blockchain Development"},
        {"type": "row", "label": "Focus.Software", "value": "Full-Stack Engineering"},
        {"type": "empty"},
        {"type": "header", "label": "— Contact", "value": "──────────────────────────────────────────", "color": accent_blue},
        {"type": "row", "label": "Portfolio", "value": "Rishvin Reddy"},
        {"type": "row", "label": "GitHub", "value": "RishvinReddy"},
        {"type": "row", "label": "LinkedIn", "value": "Rishvin Reddy"},
        {"type": "empty"},
        {"type": "header", "label": "— GitHub Stats", "value": "─────────────────────────────────────", "color": accent_orange},
        {"type": "row", "label": "Repos", "value": stats.get("repos", 0)},
        {"type": "row", "label": "Commits", "value": stats.get("commits", 0)},
        {"type": "row", "label": "Stars", "value": stats.get("stars", 0)},
        {"type": "row", "label": "Followers", "value": stats.get("followers", 0)},
    ]

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
    <rect width="{svg_width}" height="{svg_height}" fill="{bg_color}" rx="10"/>
    <style>
        .text {{ font-family: 'Courier New', Courier, monospace; font-size: 14px; fill: {text_color}; }}
        .dim {{ fill: {dim_color}; }}
    </style>
    
    <defs>
        <clipPath id="avatarClip">
            <circle cx="260" cy="270" r="230"/>
        </clipPath>
    </defs>
    
    <!-- Image -->
    <image href="data:image/png;base64,{img_b64}" x="30" y="40" width="460" height="460" preserveAspectRatio="xMidYMid slice" clip-path="url(#avatarClip)"/>
    
    <!-- Profile Info -->
    <g transform="translate(540, 40)">'''

    for i, line_data in enumerate(lines):
        y_pos = i * 16
        if line_data["type"] == "header":
            lbl = html.escape(line_data["label"])
            val = html.escape(line_data["value"])
            col = line_data["color"]
            svg_content += f'\n        <text x="0" y="{y_pos}" class="text" xml:space="preserve"><tspan style="fill: {col}; font-weight: bold;">{lbl}</tspan> <tspan class="dim">{val}</tspan></text>'
        elif line_data["type"] == "row":
            raw_str = dotted_row(line_data["label"], line_data["value"])
            parts = raw_str.split(":", 1)
            lbl = html.escape(parts[0])
            rest = parts[1].strip()
            dots_end = next((j for j, char in enumerate(rest) if char != '.'), 0)
            dots = rest[:dots_end]
            val = html.escape(rest[dots_end:].strip())
            svg_content += f'\n        <text x="0" y="{y_pos}" class="text" xml:space="preserve">{lbl}: <tspan class="dim">{dots}</tspan> {val}</text>'
        # empty lines do nothing but advance `i`

    svg_content += '''
    </g>
</svg>'''
    return svg_content

if __name__ == "__main__":
    stats = fetch_github_data()
    img_b64 = get_base64_image("icon.png")
    
    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg(stats, img_b64, is_dark_mode=True))
        
    with open("light_mode.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg(stats, img_b64, is_dark_mode=False))
