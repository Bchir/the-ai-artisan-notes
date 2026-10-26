#!/usr/bin/env python3
"""
SEO & AI Bot Read (GEO) Auditor for The AI Artisan Notes
Analyzes Markdown articles for search engine optimization, AI citation readiness,
and editorial craftsmanship.
"""

import os
import sys
import re
import math

def parse_frontmatter(content):
    meta = {}
    body = content
    has_frontmatter = False
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            has_frontmatter = True
            fm_text = parts[1]
            body = parts[2].strip()
            current_list_key = None
            for line in fm_text.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if stripped.startswith("- ") and current_list_key:
                    meta[current_list_key].append(stripped[2:].strip().strip('"\''))
                    continue
                if ":" in stripped:
                    key, val = stripped.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip('"\'')
                    if val == "" or val.startswith("["):
                        if val.startswith("[") and val.endswith("]"):
                            items = [x.strip().strip('"\'') for x in val[1:-1].split(",") if x.strip()]
                            meta[key] = items
                            current_list_key = None
                        else:
                            meta[key] = []
                            current_list_key = key
                    else:
                        current_list_key = None
                        meta[key] = val
    return has_frontmatter, meta, body

def audit_post(filepath):
    if not os.path.isfile(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return 1

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    has_fm, meta, body = parse_frontmatter(content)
    score = 100
    findings = []
    recommendations = []

    # 1. Frontmatter check
    if not has_fm:
        score -= 25
        findings.append(("[FAIL] Frontmatter", "No YAML frontmatter detected (--- ... ---)."))
        recommendations.append("Add YAML frontmatter with title, slug, date, description, and tags.")
    else:
        findings.append(("[PASS] Frontmatter", "YAML frontmatter present."))

    # Title check
    title = meta.get("title", "")
    if not title:
        first_line = body.splitlines()[0] if body else ""
        if first_line.startswith("# "):
            title = first_line[2:].strip()
            score -= 5
            findings.append(("[WARN] Title", "Title found in H1 body rather than frontmatter."))
            recommendations.append("Move title to frontmatter `title: \"...\"`.")
        else:
            score -= 20
            findings.append(("[FAIL] Title", "No title found."))
            recommendations.append("Add a clear, compelling title in frontmatter.")

    if title:
        t_len = len(title)
        if 35 <= t_len <= 75:
            findings.append(("[PASS] Title Length", f"Title length ({t_len} chars) is optimal for search snippets (35-75 chars)."))
        elif t_len < 35:
            score -= 5
            findings.append(("[WARN] Title Length", f"Title is short ({t_len} chars). Consider adding a specific hook or subtitle."))
            recommendations.append(f"Expand title to provide better context (current: \"{title}\").")
        else:
            score -= 5
            findings.append(("[WARN] Title Length", f"Title is long ({t_len} chars). Search and social previews may truncate past ~70 chars."))
            recommendations.append("Trim title to under 70 chars for crisp display.")

    # Description check
    desc = meta.get("description", "")
    if not desc:
        score -= 15
        findings.append(("[FAIL] Meta Description", "Missing description in frontmatter."))
        recommendations.append("Add a 130-160 character description summarizing the article's core insight.")
    else:
        d_len = len(desc)
        if 110 <= d_len <= 165:
            findings.append(("[PASS] Meta Description", f"Description length ({d_len} chars) is in optimal range (110-165 chars)."))
        elif d_len < 110:
            score -= 5
            findings.append(("[WARN] Meta Description", f"Description is short ({d_len} chars). Expand to ~135-160 chars for higher CTR."))
            recommendations.append("Expand meta description to include primary outcome or audience promise.")
        else:
            score -= 5
            findings.append(("[WARN] Meta Description", f"Description is long ({d_len} chars). Search snippets will truncate at ~160 chars."))
            recommendations.append("Shorten meta description to 155-160 chars.")

    # Word count and reading time
    words = body.split()
    word_count = len(words)
    est_minutes = max(1, math.ceil(word_count / 200))

    if word_count < 300:
        score -= 5
        findings.append(("[WARN] Content Depth", f"Word count ({word_count} words) is brief. (Acceptable for intro posts, but technical essays shine at 1,000+ words)."))
    else:
        findings.append(("[PASS] Content Depth", f"{word_count} words (~{est_minutes} min read). Strong depth."))

    # Headings hierarchy
    h1_matches = re.findall(r'^#\s+(.+)$', body, flags=re.MULTILINE)
    if h1_matches:
        score -= 5
        findings.append(("[WARN] Heading Hierarchy", f"Found {len(h1_matches)} H1 (#) header(s) inside body. HTML template already outputs page H1."))
        recommendations.append("Convert body H1s (#) to H2s (##) for proper semantic hierarchy.")

    h2_matches = re.findall(r'^##\s+(.+)$', body, flags=re.MULTILINE)
    h3_matches = re.findall(r'^###\s+(.+)$', body, flags=re.MULTILINE)
    if len(h2_matches) < 2:
        score -= 5
        findings.append(("[WARN] Subheadings", f"Only {len(h2_matches)} H2 section(s) found. Break content into distinct sections."))
        recommendations.append("Break content into distinct sections with descriptive H2 headings.")
    else:
        findings.append(("[PASS] Subheadings", f"{len(h2_matches)} H2 sections and {len(h3_matches)} H3 sub-sections."))

    # GEO / AI Bot Readability checks
    # 1. Direct Answer Capsule / TL;DR / Executive Summary
    summary_pattern = re.search(r'(##\s*(TL;?DR|Summary|Key Takeaways|Executive Summary|In Brief|At a Glance)|>\s*\[!NOTE\]|>\s*\*\*Key Takeaway|\*\*The bottom line:\*\*)', body, re.IGNORECASE)
    if summary_pattern:
        findings.append(("[PASS] GEO Direct Answer", "Direct answer / TL;DR / key takeaway capsule detected for AI engines & quick readers."))
    else:
        score -= 10
        findings.append(("[WARN] GEO Direct Answer", "No prominent TL;DR, Executive Summary, or Key Takeaways capsule detected."))
        recommendations.append("Add a direct-answer capsule (TL;DR or Key Takeaway callout) in the first 2-3 paragraphs. AI crawlers (Perplexity, ChatGPT, Google AI Overviews) heavily prioritize this for citation snippets.")

    # 2. Code fences language tags (parse line by line to distinguish open vs close)
    untagged_fences = 0
    total_fences = 0
    in_block = False
    for line in body.splitlines():
        if line.startswith("```"):
            if not in_block:
                in_block = True
                total_fences += 1
                lang = line[3:].strip()
                if not lang:
                    untagged_fences += 1
            else:
                in_block = False

    if untagged_fences > 0:
        score -= 5
        findings.append(("[WARN] Code Blocks", f"{untagged_fences} code block(s) lack a language specifier (e.g. ```csharp, ```typescript)."))
        recommendations.append("Add explicit language specifiers to all code blocks for syntax highlighting and AST indexing.")
    elif total_fences > 0:
        findings.append(("[PASS] Code Blocks", f"All {total_fences} code blocks have explicit language specifiers."))

    # 3. Anchor text quality
    bad_anchors = re.findall(r'\[(here|click here|link|this link|read more)\]\(', body, flags=re.IGNORECASE)
    if bad_anchors:
        score -= 5
        findings.append(("[WARN] Anchor Text", f"Found {len(bad_anchors)} generic link text(s) ('{bad_anchors[0]}')."))
        recommendations.append("Use descriptive keyword-rich anchor text instead of 'here' or 'link'.")
    else:
        findings.append(("[PASS] Anchor Text", "Anchor texts are descriptive and clean."))

    # 4. Structured elements (lists, tables, blockquotes)
    has_list = bool(re.search(r'^\s*[-*]\s+', body, re.MULTILINE))
    has_table = bool(re.search(r'\|.+\|.+\|', body))
    has_quote = bool(re.search(r'^\s*>\s+', body, re.MULTILINE))
    findings.append(("[INFO] Scannability", f"Lists: {'Yes' if has_list else 'No'} | Tables: {'Yes' if has_table else 'No'} | Quotes: {'Yes' if has_quote else 'No'}"))

    # Print Report
    print("=" * 60)
    print(f" ARTICLE AUDIT REPORT: {os.path.basename(filepath)}")
    print(f" Overall Optimization Score: {max(0, score)} / 100")
    print("=" * 60)
    print()
    print("CHECKLIST FINDINGS:")
    for status, msg in findings:
        print(f"  {status.ljust(25)} : {msg}")
    print()

    if recommendations:
        print("ACTIONABLE OPTIMIZATION RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        print()
    else:
        print("All audit checks passed! Post is primed for search engines & AI bots.\n")

    return 0 if score >= 80 else 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audit-post.py <path-to-post.md>")
        sys.exit(1)
    sys.exit(audit_post(sys.argv[1]))
