import os

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
        
    start_str = "## ✦ Selected Engineering Projects\n\n"
    end_str = "</table>\n\n⸻"
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    if start_idx != -1 and end_idx != -1:
        before = content[:start_idx + len(start_str)]
        after = content[end_idx + len("</table>\n\n"):]
        
        replacement = "<!-- STARRED_REPOS_START -->\n<!-- STARRED_REPOS_END -->\n\n"
        
        new_content = before + replacement + after
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated README markers.")
    else:
        print("Could not find table")

update_readme()
