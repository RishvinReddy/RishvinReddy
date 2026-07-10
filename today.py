import urllib.request
import json
import os
import html
from datetime import datetime, timezone
from pathlib import Path

USERNAME = "RishvinReddy"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CACHE_FILE = Path("cache/stats.json")

ASCII_PORTRAIT = """
             @@@@@@@@@@@@@@@@@@@             
          @@@@@@@@@@@@@@@@@@@@@@@@@          
       %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%       
     %@@@@@@@@@@@@@@%####%@@@@@@@%@@@@%%     
    @@@@@@@@@@@@@#=.     .-+@@@@@@@%%@@@%    
   @@@@@@@@@@@@@=           :#@@@@@@%%%@@%   
  @@@@@@@@@@@@@*    .....    =@@@@@@@%%%@@%  
 @@@@@@@@@@@@@@- :=*#####*+. *@@@@@@@%%%%%@% 
@@@@@@@@@@@@@@@*-****###++++-%@@@@@@@@%%%%@%%
@@@@@@@@@@@@@@@@+#+=-+#+-==*+%@@@@@@@%%%%%%@%
@@@@@@@@@@@@@@@@**#####**##*+@@@@@@@@%%%%%%%%
@@@@@@@@@@@@@@@@#=#%#++==*#=*@@@@@@@@@%%%%%%%
@@@@@@@@@@@@@@@@@*=*+***++=-@@@@@@@@@@%%%%%%%
@@@@@@@@@@@@@@@@@@=:=+---:.+@@@@@@@@@@%%%%%%%
@@@@@@@@@@@@@@@@#.:*-:...=*..*%@@@@@@%%%%%%%%
@@@@@@@@@@@@#+:    +#%####=    .-+#%@@@%%%%%%
 @@@@@@@#=:        :=#%%%+.         :=%@%%%% 
  @@@@%:            .+###-            .#@%%  
   @@@:               -*-               +@   
    @=                 .                     
                                             
                                             
"""

def fetch_github_data():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    try:
        # Fetch user data
        req_user = urllib.request.Request(f"https://api.github.com/users/{USERNAME}", headers=headers)
        with urllib.request.urlopen(req_user, timeout=10) as response:
            user_data = json.loads(response.read().decode())
        
        # Fetch repos data (for stars)
        req_repos = urllib.request.Request(f"https://api.github.com/users/{USERNAME}/repos?per_page=100", headers=headers)
        with urllib.request.urlopen(req_repos, timeout=10) as response:
            repos_data = json.loads(response.read().decode())

        stars = sum(repo.get('stargazers_count', 0) for repo in repos_data if not repo.get('fork', False))

        stats = {
            "repos": user_data.get("public_repos", 0),
            "followers": user_data.get("followers", 0),
            "stars": stars
        }
        
        # Write to cache
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w") as f:
            json.dump(stats, f)
            
        return stats
    
    except Exception as e:
        print(f"Error fetching from GitHub API: {e}")
        # Try to load from cache
        if CACHE_FILE.exists():
            print("Loading from cache.")
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        else:
            print("No cache available. Using N/A.")
            return {"repos": "N/A", "followers": "N/A", "stars": "N/A"}

def dotted_row(label, value, width=58):
    prefix = f"{label}: "
    dots = "." * max(2, width - len(prefix) - len(str(value)))
    return f"{prefix}{dots} {value}"

def generate_svg(stats, is_dark_mode=True):
    # Colors
    bg_color = "#0d1117" if is_dark_mode else "#ffffff"
    text_color = "#c9d1d9" if is_dark_mode else "#24292f"
    accent_green = "#2ea043"
    accent_orange = "#d29922"
    accent_blue = "#58a6ff"
    dim_color = "#8b949e" if is_dark_mode else "#6e7781"

    # SVG Template structure
    svg_width = 850
    svg_height = 420

    # Process ASCII art
    ascii_lines = ASCII_PORTRAIT.strip('\n').split('\n')
    
    # Profile Info
    profile_lines = [
        dotted_row("OS", "macOS"),
        dotted_row("University", "Woxsen University"),
        dotted_row("Degree", "B.Tech CSE"),
        dotted_row("Track", "Blockchain, IoT & Cybersecurity"),
        dotted_row("CGPA", "9.01 / 10"),
        dotted_row("Graduation", "2028"),
        dotted_row("IDE", "Antigravity IDE"),
        dotted_row("Focus.Security", "Cybersecurity, IoT, Blockchain"),
        dotted_row("Focus.Software", "Full-Stack Development, Automation, Systems"),
    ]
    
    stats_lines = [
        dotted_row("Repos", stats["repos"]),
        dotted_row("Stars", stats["stars"]),
        dotted_row("Followers", stats["followers"]),
    ]
    
    contact_lines = [
        dotted_row("Portfolio", f"{USERNAME.lower()}.github.io"),
        dotted_row("GitHub", USERNAME),
        dotted_row("LinkedIn", "Rishvin Reddy"),
    ]

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
    <rect width="{svg_width}" height="{svg_height}" fill="{bg_color}" rx="10"/>
    <style>
        .text {{ font-family: 'Courier New', Courier, monospace; font-size: 14px; fill: {text_color}; }}
        .dim {{ fill: {dim_color}; }}
        .green {{ fill: {accent_green}; font-weight: bold; }}
        .orange {{ fill: {accent_orange}; font-weight: bold; }}
        .blue {{ fill: {accent_blue}; font-weight: bold; }}
        .header {{ font-weight: bold; font-size: 14px; fill: {text_color}; }}
    </style>
    <g transform="translate(30, 40)">
        <!-- ASCII Portrait -->
        <g class="text dim">'''

    for i, line in enumerate(ascii_lines):
        line = line.replace(' ', '&#160;')
        line = line.replace('<', '&lt;').replace('>', '&gt;')
        svg_content += f'\n            <text x="0" y="{i * 16}" xml:space="preserve">{line}</text>'

    svg_content += f'''
        </g>
        
        <!-- Profile Info -->
        <g transform="translate(390, 0)">
            <text x="0" y="0" class="text"><tspan class="green">rishvin@reddy</tspan> <tspan class="dim">────────────────────────────────────────</tspan></text>'''

    for i, line in enumerate(profile_lines):
        parts = line.split(":", 1)
        label = parts[0]
        rest = parts[1].strip()
        dots_end = next((j for j, char in enumerate(rest) if char != '.'), 0)
        dots = rest[:dots_end]
        value = rest[dots_end:].strip()
        svg_content += f'\n            <text x="0" y="{(i + 2) * 16}" class="text" xml:space="preserve">{html.escape(label)}: <tspan class="dim">{dots}</tspan> {html.escape(value)}</text>'

    svg_content += f'''
            <text x="0" y="{(len(profile_lines) + 3) * 16}" class="text"><tspan class="dim">—</tspan> <tspan class="blue">Contact</tspan> <tspan class="dim">────────────────────────────────────────────</tspan></text>'''

    for i, line in enumerate(contact_lines):
        parts = line.split(":", 1)
        label = parts[0]
        rest = parts[1].strip()
        dots_end = next((j for j, char in enumerate(rest) if char != '.'), 0)
        dots = rest[:dots_end]
        value = rest[dots_end:].strip()
        svg_content += f'\n            <text x="0" y="{(len(profile_lines) + 5 + i) * 16}" class="text" xml:space="preserve">{html.escape(label)}: <tspan class="dim">{dots}</tspan> {html.escape(value)}</text>'

    svg_content += f'''
            <text x="0" y="{(len(profile_lines) + len(contact_lines) + 6) * 16}" class="text"><tspan class="dim">—</tspan> <tspan class="orange">GitHub Stats</tspan> <tspan class="dim">───────────────────────────────────────</tspan></text>'''

    for i, line in enumerate(stats_lines):
        parts = line.split(":", 1)
        label = parts[0]
        rest = parts[1].strip()
        dots_end = next((j for j, char in enumerate(rest) if char != '.'), 0)
        dots = rest[:dots_end]
        value = rest[dots_end:].strip()
        svg_content += f'\n            <text x="0" y="{(len(profile_lines) + len(contact_lines) + 8 + i) * 16}" class="text" xml:space="preserve">{html.escape(label)}: <tspan class="dim">{dots}</tspan> {html.escape(str(value))}</text>'

    svg_content += '''
        </g>
    </g>
</svg>'''
    return svg_content

if __name__ == "__main__":
    stats = fetch_github_data()
    
    with open("dark_mode.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg(stats, is_dark_mode=True))
        
    with open("light_mode.svg", "w", encoding="utf-8") as f:
        f.write(generate_svg(stats, is_dark_mode=False))
