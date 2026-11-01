#!/usr/bin/env node
// Writes public/sitemap.xml. <lastmod> is the last git commit date of each page's
// source file (git log -1 --format=%cs), never the build time. Runs as `predeploy`.
import { execFileSync } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const HOST = 'https://yilian.defiabell.com';
const PAGES = [
  { path: '/', src: 'public/index.html' },
];

const git = (...args) => execFileSync('git', ['-C', ROOT, ...args], { encoding: 'utf8' }).trim();

const urls = PAGES.map(({ path, src }) => {
  const date = git('log', '-1', '--format=%cs', '--', src);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error(`sitemap: ${src} has no commit; commit it before deploying`);
  if (git('status', '--porcelain', '--', src)) console.warn(`sitemap: ${src} has uncommitted changes; lastmod ${date} is its last commit`);
  return `  <url>\n    <loc>${HOST}${path}</loc>\n    <lastmod>${date}</lastmod>\n  </url>`;
});

const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.join('\n')}\n</urlset>\n`;
writeFileSync(resolve(ROOT, 'public/sitemap.xml'), xml);
process.stdout.write(xml);
