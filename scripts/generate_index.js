const fs = require('fs');
const path = require('path');

(async function(){
  try {
    const postsDir = path.join(__dirname, '..', 'docs', 'posts');
    const outFile = path.join(__dirname, '..', 'docs', 'index.html');

    const files = await fs.promises.readdir(postsDir);
    const posts = [];

    for (const f of files) {
      if (!f.toLowerCase().endsWith('.html')) continue;
      const full = path.join(postsDir, f);
      const content = await fs.promises.readFile(full, 'utf8');

      // Extract title
      const titleMatch = content.match(/<h1[^>]*class=["']post-title["'][^>]*>([\s\S]*?)<\/h1>/i);
      const title = titleMatch ? titleMatch[1].trim() : f;

      // Extract datetime
      const timeMatch = content.match(/<time[^>]*class=["']post-date["'][^>]*datetime=["']([^"']+)["'][^>]*>([\s\S]*?)<\/time>/i);
      const datetime = timeMatch ? timeMatch[1].trim() : null;
      const displayDate = timeMatch ? timeMatch[2].trim() : (datetime || (await fs.promises.stat(full)).mtime.toISOString().slice(0,10));

      posts.push({ file: f, title, datetime: datetime || (await fs.promises.stat(full)).mtime.toISOString(), displayDate });
    }

    posts.sort((a,b) => (a.datetime < b.datetime ? 1 : -1));

    const listItems = posts.map(p => `  <li><a href="posts/${p.file}">${p.title}</a> <small>${p.displayDate}</small></li>`).join('\n');

    const html = `<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>ブログ記事一覧</title>
</head>
<body>
  <h1>ブログ記事一覧</h1>
  <ul>
${listItems}
  </ul>
</body>
</html>`;

    await fs.promises.writeFile(outFile, html, 'utf8');
    console.log('Generated', outFile);
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
})();
