# Frontmatter Schema Reference

Every markdown article in `content/posts/` must start with a YAML frontmatter block enclosed within triple dashes (`---`).

---

## Fields Specification

| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `title` | string | **Yes** | The full, reader-facing headline of the article. | `"Designing Deterministic AI Toolchains"` |
| `slug` | string | **Yes** | URL-safe identifier for the post. | `"designing-deterministic-ai-toolchains"` |
| `date` | string (ISO 8601) | **Yes** | Publication date in `YYYY-MM-DD` format. | `"2026-10-26"` |
| `description` | string | **Yes** | 1-2 sentence synopsis used for index cards, RSS feed, and SEO meta tags. | `"A practical guide to building robust agent toolchains that fail gracefully."` |
| `tags` | array of strings | **Yes** | Category tags for discovery and filtering. | `["Agents", "System Architecture"]` |
| `author` | string | No (default: blog owner) | Author display name. | `"The AI Artisan"` |
| `draft` | boolean | No (default: false) | If `true`, article is hidden from the production build index. | `true` |
| `readingTime` | number | No | Estimated read time in minutes (calculated if omitted). | `6` |
| `canonicalUrl` | string | No | Optional canonical URL if cross-posted from another platform. | `"https://..."` |

---

## Example Frontmatter

```yaml
---
title: "Building Resilient Agent Workflows with Antigravity Skills"
slug: "building-resilient-agent-workflows"
date: "2026-10-26"
description: "How to structure modular, progressive agent skills that maintain high precision without bloating context."
tags:
  - Antigravity
  - Agent Architecture
  - LLM Engineering
author: "The AI Artisan"
draft: false
readingTime: 6
---
```
