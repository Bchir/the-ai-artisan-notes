# GEO & SEO Guide for Technical Publications

This guide outlines how to maximize discoverability across traditional search engines (Google, Bing, DuckDuckGo) and Generative Search / Answer Engines (Perplexity, ChatGPT Search, Claude, Google AI Overviews).

---

## 1. How Generative Engines (GEO / AEO) Read Content

AI search models crawl web pages, strip boilerplate markup, and evaluate text through semantic vector embeddings and LLM retrieval-augmented generation (RAG) pipelines.

### What AI Engines Look For
1. **Definitive Claims & Clear Definitions**: AI models favor content that states principles directly (e.g. *"A unit test in an agentic codebase is an invariant contract over system behavior, not an assertion over method calls."*).
2. **Compact Answer Capsules**: When answering queries like "Why are unit tests failing with AI code generation?", an LLM looks for 2–4 sentences directly beneath an introduction or H2 heading that concisely answers the query.
3. **Structured Matrices & Tables**: Comparison tables provide high-density semantic facts that are easy for RAG chunking algorithms to score as high-relevance.
4. **Code with Context**: Code snippets surrounded by brief explanations of the pattern or anti-pattern are prioritized in technical answers.

---

## 2. The Traditional SEO Foundation

While AI search is surging, classic search engine fundamentals remain the prerequisite for indexation:

- **Single H1 Rule**: The HTML document must have exactly one `<h1>`, containing the primary article title and target keywords.
- **Title Tag**: 40 to 65 characters. Keep primary keywords towards the front.
- **Meta Description**: 130 to 160 characters. Must clearly state what the reader will learn or solve.
- **Descriptive Anchor Text**: Never link the words "here" or "this link". Instead, link the concept: e.g., `[read Martin Fowler's testing pyramid breakdown](https://...)`.
- **Clean Canonical URLs**: Prevent duplicate content penalties across domains or parameter queries.

---

## 3. The Symbiosis: Writing for Craftsmen and Bots

Writing for AI bots does not mean dumbing down content or writing dry, repetitive text. In fact, modern LLMs reward:
- **Originality & Practitioner Perspective**: Real debugging stories, concrete architectural experiments, and field observations cannot be hallucinated.
- **Pragmatic Nuance**: Nuanced trade-offs (e.g., *"This works when building Greenfields, but fails when maintaining monolithic databases"*) signal authentic human authority.
