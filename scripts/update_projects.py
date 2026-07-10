import os
import json
import math
import urllib.request
import urllib.error
from datetime import datetime, timezone

USERNAME = os.getenv("GITHUB_USERNAME", "RishvinReddy")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "project_config.json")
README_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")

START_MARKER = "<!-- STARRED_REPOS_START -->"
END_MARKER = "<!-- STARRED_REPOS_END -->"

BOOST_TOPICS = {
    "cybersecurity", "security", "iot", "embedded", "esp32", "arduino", 
    "blockchain", "backend", "api", "automation", "n8n", 
    "network-security", "full-stack"
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

def fetch_all_repos():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USERNAME}/repos?type=owner&sort=updated&per_page=100&page={page}"
        print(f"[INFO] Fetching page {page}...")
        data = github_api_get(url)
        if data is None:
            return None # Failure
        if not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return repos

def is_eligible(repo, config):
    if repo.get("fork") or repo.get("archived") or repo.get("disabled") or repo.get("private"):
        return False
    if repo.get("stargazers_count", 0) < config.get("minimum_stars", 1):
        return False
    
    name = repo.get("name", "")
    
    if name == USERNAME:
        return False
        
    if name in config.get("blacklist", []):
        return False
        
    for pattern in config.get("excluded_name_patterns", []):
        if pattern.lower() in name.lower():
            # Be conservative: only exact matches or matches that indicate it's a specific excluded type
            # For simplicity in this script, we'll exclude if it's an exact match or ends with the pattern
            if name.lower() == pattern.lower() or name.lower().endswith(pattern.lower()):
                return False

    return True

def score_repo(repo, config):
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
        
    # Assume repos with size > 0 have at least some docs/README
    if repo.get("size", 0) > 0:
        score += 10
        
    if repo.get("description"):
        score += 8
        
    if repo.get("homepage"):
        score += 5
        
    topics = repo.get("topics", [])
    topic_matches = sum(1 for t in topics if t.lower() in BOOST_TOPICS)
    score += min(topic_matches * 3, 15)
    
    if repo.get("name") in config.get("priority_repositories", []):
        score += 20
        
    return score

def generate_markdown(repos):
    lines = []
    lines.append(START_MARKER)
    lines.append("## ✦ Featured Projects")
    lines.append("| Project | Description | Primary Stack | Stars | Updated |")
    lines.append("|---|---|---|---:|---|")
    
    for r in repos:
        name = r.get("name")
        url = r.get("html_url")
        desc = r.get("description") or ""
        if len(desc) > 120:
            desc = desc[:117] + "..."
        desc = desc.replace("|", "\\|").replace("\n", " ").strip()
        
        lang = r.get("language") or ""
        stack_items = []
        if lang:
            stack_items.append(lang)
        
        topics = r.get("topics", [])
        for t in topics:
            if len(stack_items) < 3 and t.lower() not in [s.lower() for s in stack_items]:
                stack_items.append(t.title())
                
        stack_str = " • ".join(stack_items)
        if not stack_str:
            stack_str = "N/A"
            
        stars = r.get("stargazers_count", 0)
        
        pushed_at_str = r.get("pushed_at")
        updated_str = ""
        if pushed_at_str:
            pushed_at = datetime.strptime(pushed_at_str, "%Y-%m-%dT%H:%M:%SZ")
            updated_str = pushed_at.strftime("%b %Y")
            
        lines.append(f"| [{name}]({url}) | {desc} | {stack_str} | ⭐ {stars} | {updated_str} |")
        
    lines.append("<sub>Automatically selected from public, non-fork repositories with at least one star.</sub>")
    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"

def update_readme(markdown_content):
    if not os.path.exists(README_PATH):
        print("[ERROR] README.md not found.")
        exit(1)
        
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)
    
    if start_idx == -1 or end_idx == -1:
        print("[ERROR] Missing markers in README.md.")
        exit(1)
        
    before = content[:start_idx]
    after = content[end_idx + len(END_MARKER):]
    
    # ensure clean line breaks
    if not before.endswith("\n"):
        before += "\n"
    if not after.startswith("\n"):
        after = "\n" + after
        
    new_content = before + markdown_content + after
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("[INFO] README.md section updated successfully.")

def main():
    config = load_config()
    print(f"[INFO] Fetching repositories for {USERNAME}")
    repos = fetch_all_repos()
    if repos is None:
        exit(1)
        
    print(f"[INFO] Retrieved {len(repos)} repositories")
    
    eligible = []
    for r in repos:
        if is_eligible(r, config):
            score = score_repo(r, config)
            r["_computed_score"] = score
            eligible.append(r)
            
    print(f"[INFO] Eligible repositories: {len(eligible)}")
    
    # Sort: 1. score (desc), 2. stars (desc), 3. pushed_at (desc), 4. name (asc)
    eligible.sort(key=lambda x: (
        x.get("_computed_score", 0),
        x.get("stargazers_count", 0),
        x.get("pushed_at", ""),
    ), reverse=True)
    
    # Secondary sort by name (ascending) handled by taking negative of other fields or just keeping stable sort
    # Actually, Python sort is stable, so we can sort in multiple passes or just use negative values for desc
    
    def sort_key(x):
        return (
            -x.get("_computed_score", 0),
            -x.get("stargazers_count", 0),
            x.get("pushed_at", "") # desc because we want reverse=False on the main sort? Wait, pushed_at is a string like "2026-07...", sorting descending means negative or reverse=True.
        )
    
    eligible.sort(key=lambda x: (
        x.get("_computed_score", 0),
        x.get("stargazers_count", 0),
        x.get("pushed_at", "")
    ), reverse=True)
    
    max_projects = config.get("max_projects", 8)
    featured = eligible[:max_projects]
    
    print(f"[INFO] Selected featured projects: {len(featured)}")
    for f in featured:
        print(f"[SELECTED] {f['name']} | score={f.get('_computed_score', 0):.1f} | stars={f.get('stargazers_count', 0)}")
        
    if not featured:
        print("[WARNING] Zero eligible repositories. Preserving current section.")
        exit(0)
        
    markdown = generate_markdown(featured)
    update_readme(markdown)

if __name__ == "__main__":
    main()
