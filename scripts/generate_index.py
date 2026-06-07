#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / 'docs' / 'posts'
OUT_FILE = ROOT / 'docs' / 'index.html'

title_re = re.compile(r'<h1[^>]*class=["\']post-title["\'][^>]*>([\s\S]*?)</h1>', re.I)
time_re = re.compile(r'<time[^>]*class=["\']post-date["\'][^>]*datetime=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</time>', re.I)

posts = []
for p in POSTS_DIR.iterdir():
    if p.suffix.lower() != '.html' or not p.is_file():
        continue
    text = p.read_text(encoding='utf-8')
    m = title_re.search(text)
    title = m.group(1).strip() if m else p.stem
    tm = time_re.search(text)
    if tm:
        datetime = tm.group(1).strip()
        display = tm.group(2).strip()
    else:
        stat = p.stat()
        datetime = stat.st_mtime
        # fallback ISO date
        from datetime import datetime as _dt
        display = _dt.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
        datetime = _dt.fromtimestamp(stat.st_mtime).isoformat()
    posts.append({'file': p.name, 'title': title, 'datetime': datetime, 'display': display})

posts.sort(key=lambda x: x['datetime'], reverse=True)

items = []
for it in posts:
    items.append(f'  <li><a href="posts/{it["file"]}">{it["title"]}</a> <small>{it["display"]}</small></li>')

html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>ブログ記事一覧</title>
</head>
<body>
  <h1>ブログ記事一覧</h1>
  <ul>
{os.linesep.join(items)}
  </ul>
</body>
</html>
"""

OUT_FILE.write_text(html, encoding='utf-8')
print('Generated', OUT_FILE)
