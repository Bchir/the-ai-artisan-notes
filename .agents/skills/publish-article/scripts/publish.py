#!/usr/bin/env python3
"""
The AI Artisan Notes - Static Site Publisher
Zero-dependency Python 3 publisher that transforms Markdown drafts into:
- Optimized HTML articles with Open Graph, Twitter Cards, and Schema.org JSON-LD
- Synchronized `posts.js`
- Standard `sitemap.xml`
- AI-friendly `robots.txt`
- `llms.txt` and `llms-full.txt` (per llmstxt.org specification)
- RSS 2.0 `feed.xml`

Usage:
    python .agents/skills/publish-article/scripts/publish.py content/posts/my-post.md
    python .agents/skills/publish-article/scripts/publish.py --all
"""

import os
import sys
import re
import json
from datetime import datetime
import xml.sax.saxutils as saxutils

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
POSTS_DIR = os.path.join(ROOT_DIR, "content", "posts")
ARTICLES_DIR = os.path.join(ROOT_DIR, "articles")
POSTS_JS_PATH = os.path.join(ROOT_DIR, "posts.js")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "resources", "article-template.html")
SITEMAP_PATH = os.path.join(ROOT_DIR, "sitemap.xml")
ROBOTS_PATH = os.path.join(ROOT_DIR, "robots.txt")
LLMS_PATH = os.path.join(ROOT_DIR, "llms.txt")
LLMS_FULL_PATH = os.path.join(ROOT_DIR, "llms-full.txt")
FEED_PATH = os.path.join(ROOT_DIR, "feed.xml")

SITE_CONFIG = {
    "base_url": "https://bchir.github.io/the-ai-artisan-notes",
    "site_name": "The AI Artisan Notes",
    "site_description": "Rethinking Software Standards in the Age of AI — Field notes, architectural patterns, and engineering reflections by Mohamed Amine Bchir.",
    "author_name": "Mohamed Amine Bchir",
    "author_url": "https://tn.linkedin.com/in/mohamed-amine-bchir",
    "author_github": "https://github.com/Bchir",
    "author_title": ".NET Tech Lead & Software Craftsman"
}

def parse_frontmatter(content):
    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
            current_list_key = None
            for line in fm_text.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if stripped.startswith("- ") and current_list_key:
                    item = stripped[2:].strip().strip('"\'')
                    meta[current_list_key].append(item)
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
                        if key in ("minutes", "readingTime"):
                            try:
                                meta["minutes"] = int(val)
                            except ValueError:
                                meta["minutes"] = 5
                        elif key == "draft":
                            meta["draft"] = val.lower() in ("true", "yes", "1")
                        else:
                            meta[key] = val
    return meta, body

def markdown_to_html(md):
    lines = md.splitlines()
    html_lines = []
    in_code_block = False
    in_list = False
    list_type = None
    in_table = False
    table_header_done = False

    for line in lines:
        stripped = line.strip()

        # Code fences
        if stripped.startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                lang = stripped[3:].strip()
                cls = f' class="language-{lang}"' if lang else ''
                html_lines.append(f"<pre><code{cls}>")
                in_code_block = True
            continue

        if in_code_block:
            escaped = (line.replace("&", "&amp;")
                           .replace("<", "&lt;")
                           .replace(">", "&gt;"))
            html_lines.append(escaped)
            continue

        # Close list if line is empty or not a list item
        if in_list and not (stripped.startswith("- ") or stripped.startswith("* ") or re.match(r'^\d+\.\s+', stripped)):
            html_lines.append(f"</{list_type}>")
            in_list = False
            list_type = None

        # Table processing
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped[1:-1].split("|")]
            # Check if this is a separator row like | :--- | :--- |
            is_separator = all(re.match(r'^:?-+:?$', c) for c in cells)
            if is_separator:
                table_header_done = True
                continue

            if not in_table:
                html_lines.append("<table>")
                in_table = True
                table_header_done = False

            if not table_header_done:
                # Header row
                th_elements = "".join(f"<th>{inline_formatting(c)}</th>" for c in cells)
                html_lines.append(f"  <thead><tr>{th_elements}</tr></thead><tbody>")
            else:
                # Body row
                td_elements = "".join(f"<td>{inline_formatting(c)}</td>" for c in cells)
                html_lines.append(f"  <tr>{td_elements}</tr>")
            continue
        elif in_table:
            html_lines.append("  </tbody></table>")
            in_table = False
            table_header_done = False

        if not stripped:
            continue

        # Headers
        if stripped.startswith("#### "):
            html_lines.append(f"<h4>{inline_formatting(stripped[5:])}</h4>")
            continue
        elif stripped.startswith("### "):
            html_lines.append(f"<h3>{inline_formatting(stripped[4:])}</h3>")
            continue
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{inline_formatting(stripped[3:])}</h2>")
            continue
        elif stripped.startswith("# "):
            # Handled by page H1, skip redundant H1 inside body
            continue

        # Callouts & Blockquotes
        if stripped.startswith("> [!NOTE]") or stripped.startswith("> [!IMPORTANT]"):
            html_lines.append('<div class="alert-note">')
            continue
        elif stripped.startswith("> "):
            quote_text = inline_formatting(stripped[2:])
            html_lines.append(f"<blockquote>{quote_text}</blockquote>")
            continue

        # Unordered list
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
                list_type = "ul"
            item = inline_formatting(stripped[2:])
            html_lines.append(f"  <li>{item}</li>")
            continue

        # Ordered list
        m_ol = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if m_ol:
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
                list_type = "ol"
            item = inline_formatting(m_ol.group(2))
            html_lines.append(f"  <li>{item}</li>")
            continue

        # Regular Paragraph
        html_lines.append(f"<p>{inline_formatting(stripped)}</p>")

    if in_list:
        html_lines.append(f"</{list_type}>")
    if in_table:
        html_lines.append("  </tbody></table>")
    if in_code_block:
        html_lines.append("</code></pre>")

    return "\n".join(html_lines)

def inline_formatting(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text

def build_schema_json_ld(title, description, canonical_url, date_iso, tags):
    schema = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": description,
        "url": canonical_url,
        "datePublished": date_iso,
        "dateModified": date_iso,
        "author": {
            "@type": "Person",
            "name": SITE_CONFIG["author_name"],
            "url": SITE_CONFIG["author_url"],
            "sameAs": [
                SITE_CONFIG["author_url"],
                SITE_CONFIG["author_github"]
            ]
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_CONFIG["site_name"],
            "url": SITE_CONFIG["base_url"]
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        }
    }
    if tags:
        schema["keywords"] = ", ".join(tags) if isinstance(tags, list) else str(tags)
    return json.dumps(schema, indent=4)

def publish_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    meta, body = parse_frontmatter(content)

    if meta.get("draft") is True:
        print(f"[SKIP] Draft post: {os.path.basename(filepath)}")
        return None

    slug = meta.get("slug")
    if not slug:
        basename = os.path.splitext(os.path.basename(filepath))[0]
        slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', basename)

    title = meta.get("title")
    if not title:
        # Fallback to first H1
        first_line = body.splitlines()[0] if body else ""
        if first_line.startswith("# "):
            title = first_line[2:].strip()
            # remove that line from body
            body = "\n".join(body.splitlines()[1:]).strip()
        else:
            title = slug.replace("-", " ").title()

    date_str = meta.get("date", datetime.now().strftime("%Y-%m-%d"))
    desc = meta.get("description", "")
    if not desc:
        # Fallback: grab first paragraph
        paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.startswith("#") and not p.startswith(">")]
        desc = paras[0][:160] if paras else "Field notes from The AI Artisan Notes."

    tags = meta.get("tags", ["Software Craftsmanship", "AI Engineering"])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    word_count = len(body.split())
    minutes = meta.get("minutes", max(1, round(word_count / 200)))

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        date_formatted = dt.strftime("%B %d, %Y")
        date_iso = f"{date_str}T00:00:00+01:00"
    except Exception:
        date_formatted = date_str
        date_iso = f"{date_str}T00:00:00+01:00"

    canonical_url = f"{SITE_CONFIG['base_url']}/articles/{slug}.html"

    # Open Graph Tags for tags
    og_tag_elements = "\n  ".join([f'<meta property="article:tag" content="{t}">' for t in tags])

    schema_json_ld = build_schema_json_ld(title, desc, canonical_url, date_iso, tags)
    html_content = markdown_to_html(body)

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    out_html = (template
        .replace("{{TITLE}}", title)
        .replace("{{SUBTITLE}}", meta.get("subtitle", ""))
        .replace("{{DESCRIPTION}}", desc)
        .replace("{{CANONICAL_URL}}", canonical_url)
        .replace("{{DATE_FORMATTED}}", date_formatted)
        .replace("{{DATE_ISO}}", date_iso)
        .replace("{{MINUTES}}", str(minutes))
        .replace("{{AUTHOR_NAME}}", SITE_CONFIG["author_name"])
        .replace("{{AUTHOR_URL}}", SITE_CONFIG["author_url"])
        .replace("{{OG_TAGS}}", og_tag_elements)
        .replace("{{SCHEMA_JSON_LD}}", schema_json_ld)
        .replace("{{CONTENT_HTML}}", html_content)
    )

    os.makedirs(ARTICLES_DIR, exist_ok=True)
    out_file = os.path.join(ARTICLES_DIR, f"{slug}.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(out_html)

    print(f"[OK] Generated: articles/{slug}.html")

    return {
        "title": title,
        "url": f"articles/{slug}.html",
        "canonical_url": canonical_url,
        "slug": slug,
        "date": date_str,
        "date_iso": date_iso,
        "minutes": minutes,
        "description": desc,
        "tags": tags,
        "raw_body": body
    }

def update_posts_js(all_posts):
    # Sort posts by date descending
    sorted_posts = sorted(all_posts, key=lambda x: x["date"], reverse=True)
    registry_entries = []
    for p in sorted_posts:
        registry_entries.append({
            "title": p["title"],
            "url": p["url"],
            "date": p["date"],
            "minutes": p["minutes"],
            "description": p["description"]
        })

    posts_json = json.dumps(registry_entries, indent=2)
    js_content = f"/**\n * Posts Registry\n * Automatically updated by publish skill\n */\nwindow.POSTS = {posts_json};\n"
    with open(POSTS_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"[OK] Updated: posts.js ({len(sorted_posts)} posts)")

def generate_sitemap(all_posts):
    urls = [
        f"""  <url>
    <loc>{SITE_CONFIG['base_url']}/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]

    for p in all_posts:
        urls.append(f"""  <url>
    <loc>{p['canonical_url']}</loc>
    <lastmod>{p['date']}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{os.linesep.join(urls)}
</urlset>
"""
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("[OK] Generated: sitemap.xml")

def generate_robots():
    robots_content = f"""User-agent: *
Allow: /

# Welcoming AI & Generative Search Engines
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: {SITE_CONFIG['base_url']}/sitemap.xml
"""
    with open(ROBOTS_PATH, "w", encoding="utf-8") as f:
        f.write(robots_content)
    print("[OK] Generated: robots.txt")

def generate_llms_txt(all_posts):
    """
    Standard llms.txt & llms-full.txt following the llmstxt.org specification.
    """
    sorted_posts = sorted(all_posts, key=lambda x: x["date"], reverse=True)
    
    # llms.txt (index)
    lines = [
        f"# {SITE_CONFIG['site_name']}",
        f"> {SITE_CONFIG['site_description']}",
        "",
        f"Author: {SITE_CONFIG['author_name']} ({SITE_CONFIG['author_title']})",
        f"Profile: {SITE_CONFIG['author_url']}",
        "",
        "## Core Principles & Philosophy",
        "- The Three Shifts: Deprecated syntactic rituals, altered specification-driven architecture, and created evaluation harnesses for AI.",
        "- Spec-Driven Engineering: Behavioral contracts are the persistent source of truth; implementations are disposable artifacts.",
        "- Production Reality Over Demo Magic: High determinism, observability, and craftsmanship over brittle AI wrappers.",
        "",
        "## Articles & Field Notes"
    ]

    for p in sorted_posts:
        lines.append(f"- [{p['title']}]({p['canonical_url']}): {p['description']}")

    with open(LLMS_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("[OK] Generated: llms.txt (Standard AI Agent Directory)")

    # llms-full.txt (aggregated full text for single-shot LLM ingestion)
    full_lines = [
        f"# {SITE_CONFIG['site_name']} - Full Content Ingestion",
        f"> Aggregated corpus of all notes and architectural essays for AI crawlers and LLM analysis.",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        ""
    ]

    for p in sorted_posts:
        full_lines.append(f"# {p['title']}")
        full_lines.append(f"URL: {p['canonical_url']}")
        full_lines.append(f"Date: {p['date']} | Reading Time: {p['minutes']} min | Author: {SITE_CONFIG['author_name']}")
        full_lines.append(f"Synopsis: {p['description']}")
        full_lines.append("")
        full_lines.append(p["raw_body"])
        full_lines.append("\n---\n")

    with open(LLMS_FULL_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(full_lines))
    print("[OK] Generated: llms-full.txt (Aggregated Corpus)")

def generate_feed(all_posts):
    """
    RSS 2.0 Feed for feed readers, newsletters, and syndication bots.
    """
    sorted_posts = sorted(all_posts, key=lambda x: x["date"], reverse=True)
    items = []

    for p in sorted_posts:
        try:
            dt = datetime.strptime(p["date"], "%Y-%m-%d")
            pub_date = dt.strftime("%a, %d %b %Y 00:00:00 +0100")
        except Exception:
            pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0100")

        item_xml = f"""    <item>
      <title>{saxutils.escape(p['title'])}</title>
      <link>{p['canonical_url']}</link>
      <guid isPermaLink="true">{p['canonical_url']}</guid>
      <pubDate>{pub_date}</pubDate>
      <author>{saxutils.escape(SITE_CONFIG['author_name'])}</author>
      <description>{saxutils.escape(p['description'])}</description>
    </item>"""
        items.append(item_xml)

    now_rfc = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0100")
    feed_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{saxutils.escape(SITE_CONFIG['site_name'])}</title>
    <link>{SITE_CONFIG['base_url']}/</link>
    <description>{saxutils.escape(SITE_CONFIG['site_description'])}</description>
    <language>en-us</language>
    <lastBuildDate>{now_rfc}</lastBuildDate>
    <atom:link href="{SITE_CONFIG['base_url']}/feed.xml" rel="self" type="application/rss+xml" />
{os.linesep.join(items)}
  </channel>
</rss>
"""
    with open(FEED_PATH, "w", encoding="utf-8") as f:
        f.write(feed_content)
    print("[OK] Generated: feed.xml (RSS 2.0)")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        print("Usage: python publish.py <path-to-post.md> | --all")
        sys.exit(0)

    all_posts = []
    
    # Process all posts in POSTS_DIR to keep registry and site artifacts comprehensive
    if os.path.exists(POSTS_DIR):
        for fname in sorted(os.listdir(POSTS_DIR)):
            if fname.endswith(".md"):
                filepath = os.path.join(POSTS_DIR, fname)
                post_data = publish_file(filepath)
                if post_data:
                    all_posts.append(post_data)

    if all_posts:
        update_posts_js(all_posts)
        generate_sitemap(all_posts)
        generate_robots()
        generate_llms_txt(all_posts)
        generate_feed(all_posts)
        print("\nAll site artifacts synchronized successfully!")

if __name__ == "__main__":
    main()
