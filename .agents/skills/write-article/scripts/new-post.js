#!/usr/bin/env node

/**
 * Scaffolds a new blog post in content/posts/
 * Usage: node .agents/skills/write-article/scripts/new-post.js "My New Post Title"
 */

const fs = require('fs');
const path = require('path');

function slugify(text) {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '');
}

function formatDate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

const titleArg = process.argv.slice(2).join(' ').trim();
if (!titleArg) {
  console.error('Error: Please provide a title for the new post.');
  console.log('Usage: node .agents/skills/write-article/scripts/new-post.js "Your Article Title"');
  process.exit(1);
}

const slug = slugify(titleArg);
const today = formatDate(new Date());
const filename = `${today}-${slug}.md`;

const postsDir = path.resolve(process.cwd(), 'content', 'posts');
if (!fs.existsSync(postsDir)) {
  fs.mkdirSync(postsDir, { recursive: true });
}

const targetPath = path.join(postsDir, filename);

if (fs.existsSync(targetPath)) {
  console.error(`Error: File already exists at ${targetPath}`);
  process.exit(1);
}

const templatePath = path.resolve(
  __dirname,
  '..',
  'resources',
  'article-template.md'
);

let content = '';
if (fs.existsSync(templatePath)) {
  content = fs.readFileSync(templatePath, 'utf8');
  content = content
    .replace(/title:\s*".*?"/, `title: "${titleArg.replace(/"/g, '\\"')}"`)
    .replace(/slug:\s*".*?"/, `slug: "${slug}"`)
    .replace(/date:\s*".*?"/, `date: "${today}"`);
} else {
  content = `---
title: "${titleArg}"
slug: "${slug}"
date: "${today}"
description: "A short synopsis of this article."
tags:
  - Notes
author: "The AI Artisan"
draft: true
readingTime: 3
---

Write your article here...
`;
}

fs.writeFileSync(targetPath, content, 'utf8');
console.log(`\x1b[32m✔ Post created successfully:\x1b[0m ${targetPath}`);
console.log(`Edit your article in: content/posts/${filename}`);
