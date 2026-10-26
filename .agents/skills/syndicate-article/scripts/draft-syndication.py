#!/usr/bin/env python3
"""
Social Syndication Generator for The AI Artisan Notes
Generates optimized LinkedIn posts and X/Twitter threads from a published article.
"""

import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SITE_URL = "https://bchir.github.io/the-ai-artisan-notes"

def parse_post(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
            for line in fm_text.splitlines():
                if ":" in line and not line.strip().startswith("-"):
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"\'')

    slug = meta.get("slug")
    if not slug:
        basename = os.path.splitext(os.path.basename(filepath))[0]
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', basename)

    title = meta.get("title", slug.replace("-", " ").title())
    desc = meta.get("description", "")
    subtitle = meta.get("subtitle", "")

    # Extract H2s
    h2_matches = [h.strip() for h in re.findall(r'^##\s+(.+)$', body, flags=re.MULTILINE)]
    
    # Extract TL;DR
    tldr_match = re.search(r'>\s*\[!NOTE\]\s*\n>\s*\*\*The Bottom Line \(TL;DR\)\*\*:\s*\n>\s*(.+)', body)
    tldr = tldr_match.group(1).strip() if tldr_match else desc

    article_url = f"{SITE_URL}/articles/{slug}.html"

    return {
        "title": title,
        "slug": slug,
        "subtitle": subtitle,
        "desc": desc,
        "tldr": tldr,
        "h2s": h2_matches[:4],
        "url": article_url
    }

def generate_linkedin(data):
    sections = "\n".join([f"• {h}" for h in data["h2s"]]) if data["h2s"] else "• The breakdown of legacy testing\n• Shifting to behavioral contracts\n• The rise of evaluation harnesses"

    return f"""============================================================
LINKEDIN POST DRAFT
============================================================

{data['title']}

{data['subtitle'] if data['subtitle'] else data['desc']}

We automated code implementation with AI agents, but we kept the verification rituals designed for hand-typed syntax. 

Here is what broke:
When an agent refactors code, it rewrites both the implementation and its unit tests. Everything is green, but user behavior breaks. Green no longer means "nothing broke"—it just means "the code agrees with itself."

The bottom line:
{data['tldr']}

In this new field note for The AI Artisan Notes, I break down:
{sections}

Read the full architectural essay here:
👉 {data['url']}

How is your engineering team adapting your testing pyramid as AI coding agents become the primary implementers?

#SoftwareArchitecture #AIEngineering #SoftwareCraftsmanship #DotNet #Testing
"""

def generate_twitter(data):
    return f"""============================================================
X / TWITTER THREAD DRAFT
============================================================

[Tweet 1 - The Hook]
{data['title']} 🧵

We automated implementation with AI, but kept the verification rituals of the 2010s.

Why traditional unit tests fail in an agentic codebase (and where the unit actually moved): 👇

---

[Tweet 2 - The Friction]
We asked an AI agent to refactor legacy code.
It changed everything: the logic and the unit tests.

All tests passed green. We deployed. Behavior broke.

Green didn't mean "nothing broke." It meant "the machine agrees with itself."

---

[Tweet 3 - The Paradigm Shift]
{data['tldr']}

When code generation is free, testing private methods is waste. The only thing humans can reliably own is the behavioral specification.

---

[Tweet 4 - The Takeaway & Link]
The test pyramid isn't dead—it's evolving into an architectural diamond:
1. Executable behavioral specs at the top
2. Structural architectural rules in the middle
3. Real integration harnesses at the base

Read the complete breakdown on The AI Artisan Notes:
🔗 {data['url']}
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python draft-syndication.py <path-to-post.md>")
        sys.exit(1)

    data = parse_post(sys.argv[1])
    print(generate_linkedin(data))
    print()
    print(generate_twitter(data))

if __name__ == "__main__":
    main()
