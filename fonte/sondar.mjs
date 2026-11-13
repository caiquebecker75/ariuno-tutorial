// Lista o que existe de verdade em cada tela da demonstração: itens do menu e botões da área principal.
//   node fonte/sondar.mjs <dist do Ariuno> "Item do menu,Outro item"
import { createRequire } from 'node:module';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const require = createRequire(process.env.HOME + '/ariuno-orcamentos/package.json');
const { chromium } = require('playwright');
const raiz = process.argv[2]; const itens = (process.argv[3] || '').split(',').filter(Boolean);
const tipos = { '.js': 'text/javascript', '.css': 'text/css', '.html': 'text/html', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png' };
const srv = http.createServer((q, r) => { const p = decodeURIComponent(q.url.split('?')[0]); let f = path.join(raiz, p); if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) f = path.join(raiz, 'index.html'); r.writeHead(200, { 'content-type': tipos[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(0);
const b = await chromium.launch(); const c = await b.newContext({ viewport: { width: 1600, height: 1000 }, serviceWorkers: 'block', locale: 'pt-BR' });
const p = await c.newPage(); p.on('dialog', (d) => d.accept().catch(() => {}));
await p.goto(`http://localhost:${srv.address().port}/?demo=1`, { waitUntil: 'domcontentloaded', timeout: 90000 });
await p.waitForFunction(() => document.body.innerText.includes('Tarefas'), null, { timeout: 90000 }); await p.waitForTimeout(1500);
await p.addStyleTag({ content: '#task-onboarding-tour-root{display:none!important}' });
await p.evaluate(() => { for (const bt of document.querySelectorAll('button')) { const t = (bt.textContent || '').trim(); if (/^(Departamentos|Administração)$/i.test(t)) bt.click(); } }); await p.waitForTimeout(500);
const menu = await p.evaluate(() => [...document.querySelectorAll('aside button')].filter((x) => x.offsetParent).map((x) => (x.textContent || '').trim().replace(/\s+/g, ' ')).filter(Boolean));
console.log('MENU:', JSON.stringify(menu));
for (const it of itens) {
  const ok = await p.evaluate((r) => { const bt = [...document.querySelectorAll('aside button')].find((x) => (x.textContent || '').trim().replace(/\s*\d+$/, '') === r); if (bt) { bt.click(); return true; } return false; }, it);
  await p.waitForTimeout(1800);
  const bts = await p.evaluate(() => [...document.querySelectorAll('main button, main [role=tab]')].filter((x) => x.offsetParent).map((x) => ((x.textContent || '').trim().replace(/\s+/g, ' ') || ('[' + (x.getAttribute('title') || x.getAttribute('aria-label') || '?') + ']')).slice(0, 40)));
  const tit = await p.evaluate(() => [...document.querySelectorAll('main h1, main h2')].slice(0, 3).map((x) => x.textContent.trim().slice(0, 40)));
  console.log(`\n== ${it} (${ok ? 'abriu' : 'SEM MENU'}) títulos ${JSON.stringify(tit)}\n${JSON.stringify([...new Set(bts)].slice(0, 70))}`);
}
await b.close(); srv.close();
