import os
import json
import math
import urllib.request
import urllib.error
import re
import textwrap
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import shutil

USERNAME = os.getenv("GITHUB_USERNAME", "RishvinReddy")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "scripts", "project_config.json")
README_PATH = os.path.join(BASE_DIR, "README.md")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "projects")
TEMP_DIR = os.path.join(BASE_DIR, ".tmp", "project-cards")
MANIFEST_PATH = os.path.join(ASSETS_DIR, "manifest.json")

START_MARKER = "<!-- STARRED_REPOS_START -->"
END_MARKER = "<!-- STARRED_REPOS_END -->"

SYSTEM_FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
MONO_FONT = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"

PALETTES = {
    "dark": {
        "bg_base": "#000000",
        "bg_surface": "#000000",
        "surface_elevated": "#0A0A0A",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "border": "#1E293B"
    },
    "light": {
        "bg_base": "#000000",
        "bg_surface": "#000000",
        "surface_elevated": "#F1F5F9",
        "text_primary": "#0F172A",
        "text_secondary": "#475569",
        "border": "#CBD5E1"
    }
}

ACCENTS = {
    "cybersecurity": {"dark": "#38BDF8", "light": "#0284C7", "label": "CYBERSECURITY"},
    "iot": {"dark": "#22C55E", "light": "#15803D", "label": "IOT SYSTEM"},
    "blockchain": {"dark": "#A78BFA", "light": "#7C3AED", "label": "BLOCKCHAIN"},
    "backend": {"dark": "#60A5FA", "light": "#2563EB", "label": "BACKEND SYSTEM"},
    "automation": {"dark": "#F59E0B", "light": "#B45309", "label": "AUTOMATION"},
    "algorithms": {"dark": "#F472B6", "light": "#BE185D", "label": "ALGORITHMS"},
    "web": {"dark": "#2DD4BF", "light": "#0F766E", "label": "FULL-STACK / WEB"},
    "default": {"dark": "#38BDF8", "light": "#1D4ED8", "label": "FEATURED REPOSITORY"}
}

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not load config: {e}")
        exit(1)

def github_api_get(url):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"[ERROR] API request failed for {url}: {e}")
        return None

def fetch_repositories():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USERNAME}/repos?type=owner&sort=updated&per_page=100&page={page}"
        print(f"[INFO] Fetching page {page}...")
        data = github_api_get(url)
        if data is None: return None
        if not data: break
        repos.extend(data)
        if len(data) < 100: break
        page += 1
    return repos

def is_eligible(repo, config):
    if repo.get("fork") or repo.get("archived") or repo.get("disabled") or repo.get("private"):
        return False
    if repo.get("stargazers_count", 0) < config.get("minimum_stars", 1):
        return False
    
    name = repo.get("name", "")
    if name == USERNAME: return False
    if name in config.get("blacklist", []): return False
        
    for pattern in config.get("excluded_name_patterns", []):
        if name.lower() == pattern.lower() or name.lower().endswith(pattern.lower()):
            return False
    return True

def score_repository(repo, config):
    score = 0
    stars = repo.get("stargazers_count", 0)
    score += math.log2(stars + 1) * 40

    pushed_at_str = repo.get("pushed_at")
    if pushed_at_str:
        pushed_at = datetime.strptime(pushed_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        days_ago = (datetime.now(timezone.utc) - pushed_at).days
        if days_ago <= 30: score += 30
        elif days_ago <= 90: score += 22
        elif days_ago <= 180: score += 14
        elif days_ago <= 365: score += 7
        
    if repo.get("size", 0) > 0: score += 10
    if repo.get("description"): score += 8
    if repo.get("homepage"): score += 5
        
    topics = repo.get("topics", [])
    topic_priority = set(config.get("topic_priority", []))
    topic_matches = sum(1 for t in topics if t.lower() in topic_priority)
    score += min(topic_matches * 3, 15)
    
    if repo.get("name") in config.get("priority_repositories", []):
        score += 20
    return score

def slugify_repository_name(name):
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', name)
    return slug.strip('-').lower()

def sanitize_svg_text(text):
    if not text: return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def wrap_description(text, config):
    if not text: return []
    width = 54 # approx character width for description
    max_lines = config.get("card", {}).get("max_description_lines", 3)
    lines = textwrap.wrap(text, width=width, break_long_words=False)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        if len(lines[-1]) > width - 3:
            lines[-1] = lines[-1][:width-3] + "..."
        else:
            lines[-1] = lines[-1] + "..."
    return lines

def detect_project_domain(repo, config):
    name = repo.get("name", "")
    domain_overrides = config.get("domain_overrides", {})
    if name in domain_overrides:
        return domain_overrides[name]
        
    topics = [t.lower() for t in repo.get("topics", [])]
    
    # Priority mapping
    mapping = {
        "cybersecurity": ["cybersecurity", "security", "network-security"],
        "iot": ["iot", "embedded", "esp32", "arduino"],
        "blockchain": ["blockchain", "crypto"],
        "algorithms": ["algorithms", "dsa"],
        "automation": ["automation", "n8n"],
        "backend": ["backend", "api"],
        "web": ["web", "full-stack", "react", "nextjs", "frontend"]
    }
    
    for domain, keywords in mapping.items():
        if any(k in topics for k in keywords):
            return domain
            
    desc = (repo.get("description") or "").lower()
    for domain, keywords in mapping.items():
        if any(k in desc for k in keywords):
            return domain
            
    for domain, keywords in mapping.items():
        if any(k in name.lower() for k in keywords):
            return domain
            
    return "default"

def build_project_metadata(repo, config):
    name = repo.get("name")
    if len(name) > 36:
        name = name[:35] + "…"
        
    domain = detect_project_domain(repo, config)
    
    # Language & Topics
    lang = repo.get("language")
    stack_items = [lang] if lang else ["Engineering"]
    topics = repo.get("topics", [])
    max_topics = config.get("card", {}).get("max_topics", 2)
    for t in topics:
        if len(stack_items) < max_topics + 1 and t.lower() not in [s.lower() for s in stack_items]:
            stack_items.append(t.title())
    stack_str = " • ".join(stack_items)
    if len(stack_str) > 40:
        stack_str = stack_str[:38] + "…"
        
    # Stars
    stars = repo.get("stargazers_count", 0)
    if stars >= 10000:
        star_str = f"★ {round(stars/1000)}k"
    elif stars >= 1000:
        star_str = f"★ {round(stars/1000, 1)}k"
    else:
        star_str = f"★ {stars}"
        
    # Date
    updated_str = ""
    pushed_at_str = repo.get("pushed_at")
    if pushed_at_str:
        pushed_at = datetime.strptime(pushed_at_str, "%Y-%m-%dT%H:%M:%SZ")
        updated_str = f"Updated {pushed_at.strftime('%b %Y')}"
        
    meta_str = f"{star_str}   {updated_str}"
    
    return {
        "repo_name": name,
        "description": wrap_description(repo.get("description"), config),
        "stack_str": stack_str,
        "meta_str": meta_str,
        "domain": domain,
        "slug": slugify_repository_name(repo.get("name")),
        "url": repo.get("html_url")
    }

def render_project_svg(meta, theme):
    colors = PALETTES[theme]
    accent = ACCENTS[meta["domain"]][theme]
    eyebrow = ACCENTS[meta["domain"]]["label"]
    
    tspans = []
    for i, line in enumerate(meta["description"]):
        tspans.append(f'<text x="0" y="{i * 24}" font-family="{SYSTEM_FONT}" font-size="15" font-weight="400" fill="{colors["text_secondary"]}">{sanitize_svg_text(line)}</text>')
    desc_svg = "\n      ".join(tspans)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 230" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{colors["bg_surface"]}" />
      <stop offset="100%" stop-color="{colors["bg_base"]}" />
    </linearGradient>
    <clipPath id="cardClip">
      <rect x="0" y="0" width="560" height="230" rx="16" />
    </clipPath>
  </defs>
  
  <rect x="0" y="0" width="560" height="230" rx="16" fill="url(#bgGradient)" stroke="{colors["border"]}" stroke-width="1.5"/>
  <rect x="0" y="0" width="4" height="230" fill="{accent}" clip-path="url(#cardClip)"/>
  
  <g transform="translate(32, 32)">
    <text x="0" y="10" font-family="{SYSTEM_FONT}" font-size="12" font-weight="700" fill="{accent}" letter-spacing="1.5">{sanitize_svg_text(eyebrow)}</text>
    <text x="0" y="44" font-family="{MONO_FONT}" font-size="22" font-weight="700" fill="{colors["text_primary"]}">{sanitize_svg_text(meta["repo_name"])}</text>
    <g transform="translate(0, 78)">
      {desc_svg}
    </g>
    <g transform="translate(0, 168)">
      <text x="0" y="0" font-family="{MONO_FONT}" font-size="14" font-weight="500" fill="{colors["text_secondary"]}">{sanitize_svg_text(meta["stack_str"])}</text>
      <text x="496" y="0" font-family="{SYSTEM_FONT}" font-size="14" font-weight="500" fill="{colors["text_secondary"]}" text-anchor="end">{sanitize_svg_text(meta["meta_str"])}</text>
    </g>
  </g>
</svg>"""
    return svg

def validate_svg(svg_content):
    if not svg_content or "<svg" not in svg_content or "</svg>" not in svg_content:
        return False
    try:
        ET.fromstring(svg_content)
        return True
    except ET.ParseError:
        return False

def generate_readme_grid(projects):
    lines = []
    lines.append(START_MARKER)
    lines.append("## ✦ Featured Projects")
    lines.append("<table>")
    
    for i in range(0, len(projects), 2):
        lines.append("<tr>")
        for j in range(2):
            if i + j < len(projects):
                p = projects[i + j]
                url = p['url']
                alt = sanitize_svg_text(f"{p['repo_name']} - Engineering project")
                light_src = f"./assets/projects/{p['light']}"
                dark_src = f"./assets/projects/{p['dark']}"
                
                cell = f"""<td width="50%" valign="top">
<a href="{url}">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{dark_src}">
  <source media="(prefers-color-scheme: light)" srcset="{light_src}">
  <img alt="{alt}" src="{light_src}" width="100%">
</picture>
</a>
</td>"""
                lines.append(cell)
            else:
                lines.append('<td width="50%" valign="top"></td>')
        lines.append("</tr>")
        
    lines.append("</table>")
    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"

def replace_marker_section(new_content):
    if not os.path.exists(README_PATH):
        print("[ERROR] README.md not found.")
        return False
        
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)
    
    if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
        print("[ERROR] Invalid markers in README.md.")
        return False
        
    before = content[:start_idx]
    after = content[end_idx + len(END_MARKER):]
    
    if not before.endswith("\n"): before += "\n"
    if not after.startswith("\n"): after = "\n" + after
        
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(before + new_content + after)
    return True

def cleanup_assets():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

def main():
    config = load_config()
    print(f"[INFO] Fetching repositories for {USERNAME}")
    repos = fetch_repositories()
    if repos is None:
        print("[ERROR] API failure.")
        exit(1)
        
    eligible = []
    for r in repos:
        if is_eligible(r, config):
            r["_computed_score"] = score_repository(r, config)
            eligible.append(r)
            
    eligible.sort(key=lambda x: (
        x.get("_computed_score", 0),
        x.get("stargazers_count", 0),
        x.get("pushed_at", "")
    ), reverse=True)
    
    max_projects = config.get("max_projects", 8)
    featured = eligible[:max_projects]
    
    if not featured:
        print("[WARNING] Zero eligible repositories.")
        exit(1)
        
    cleanup_assets()
    
    manifest = {
        "generated_by": "scripts/update_projects.py",
        "projects": []
    }
    
    generated_projects = []
    
    for repo in featured:
        meta = build_project_metadata(repo, config)
        
        # Ensure unique slugs
        slug = meta["slug"]
        while slug in [p["slug"] for p in generated_projects]:
            slug += "-x"
        meta["slug"] = slug
        
        light_filename = f"project-{slug}-light.svg"
        dark_filename = f"project-{slug}-dark.svg"
        
        light_svg = render_project_svg(meta, "light")
        dark_svg = render_project_svg(meta, "dark")
        
        if not validate_svg(light_svg) or not validate_svg(dark_svg):
            print(f"[ERROR] SVG validation failed for {slug}")
            exit(1)
            
        with open(os.path.join(TEMP_DIR, light_filename), "w", encoding="utf-8") as f:
            f.write(light_svg)
        with open(os.path.join(TEMP_DIR, dark_filename), "w", encoding="utf-8") as f:
            f.write(dark_svg)
            
        generated_projects.append({
            "repository": repo.get("name"),
            "slug": slug,
            "url": meta["url"],
            "repo_name": meta["repo_name"],
            "light": light_filename,
            "dark": dark_filename
        })
        
        manifest["projects"].append({
            "repository": repo.get("name"),
            "slug": slug,
            "light": light_filename,
            "dark": dark_filename
        })
        
    # Copy from TEMP to ASSETS
    for p in generated_projects:
        shutil.copy(os.path.join(TEMP_DIR, p["light"]), os.path.join(ASSETS_DIR, p["light"]))
        shutil.copy(os.path.join(TEMP_DIR, p["dark"]), os.path.join(ASSETS_DIR, p["dark"]))
        
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    # Cleanup stale assets
    valid_files = set([MANIFEST_PATH])
    for p in manifest["projects"]:
        valid_files.add(os.path.join(ASSETS_DIR, p["light"]))
        valid_files.add(os.path.join(ASSETS_DIR, p["dark"]))
        
    for filename in os.listdir(ASSETS_DIR):
        filepath = os.path.join(ASSETS_DIR, filename)
        if filepath not in valid_files and filename.endswith(".svg") and filename.startswith("project-"):
            print(f"[INFO] Removing stale asset {filename}")
            os.remove(filepath)
            
    readme_content = generate_readme_grid(generated_projects)
    if not replace_marker_section(readme_content):
        exit(1)
        
    print("[INFO] Project generation complete.")

if __name__ == "__main__":
    main()
