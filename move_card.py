import re

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# The card block
card_block = """<picture>
  <source
    media="(prefers-color-scheme: dark)"
    srcset="./dark_mode.svg"
  />
  <source
    media="(prefers-color-scheme: light)"
    srcset="./light_mode.svg"
  />
  <img
    src="./dark_mode.svg"
    alt="Rishvin Reddy — Engineering Profile"
    width="100%"
  />
</picture>"""

# Remove from top
content = content.replace(card_block, "", 1)

# Find the section starting with ## ✦ About Me up to ## ✦ Tech Stack
start_marker = "## ✦ About Me"
end_marker = "## ✦ Tech Stack"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    before = content[:start_idx]
    after = content[end_idx:]
    
    new_middle = f"## ✦ About Me\n\n<div align=\"center\">\n{card_block}\n</div>\n\n⸻\n\n"
    
    content = before + new_middle + after

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated README")
