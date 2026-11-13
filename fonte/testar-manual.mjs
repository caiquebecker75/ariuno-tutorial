// Testa o que o manual avançado trouxe: índices, player de vídeo, GIFs e telas interativas novas.
//   node fonte/testar-manual.mjs <pasta do deck> <pasta de saída>
import { createRequire } from 'node:module'; import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const require = createRequire(process.env.HOME + '/ariuno-orcamentos/package.json'); const { chromium } = require('playwright');
const raiz = process.argv[2], saida = process.argv[3]; fs.mkdirSync(saida, { recursive: true });
const tipos = { '.js': 'text/javascript', '.css': 'text/css', '.html': 'text/html', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.txt': 'text/plain', '.json': 'application/json', '.mp4': 'video/mp4', '.gif': 'image/gif' };
const srv = http.createServer((q, r) => {
  const p = decodeURIComponent(q.url.split('?')[0]); const f = path.join(raiz, p === '/' ? 'index.html' : p);
  if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  const tam = fs.statSync(f).size, rg = q.headers.range;
  if (rg) { const [a, b] = rg.replace('bytes=', '').split('-'); const ini = +a, fim = b ? +b : tam - 1; r.writeHead(206, { 'content-type': tipos[path.extname(f)] || 'application/octet-stream', 'content-range': `bytes ${ini}-${fim}/${tam}`, 'accept-ranges': 'bytes', 'content-length': fim - ini + 1 }); return fs.createReadStream(f, { start: ini, end: fim }).pipe(r); }
  r.writeHead(200, { 'content-type': tipos[path.extname(f)] || 'application/octet-stream', 'content-length': tam, 'accept-ranges': 'bytes' }); fs.createReadStream(f).pipe(r);
}).listen(0);
const U = `http://localhost:${srv.address().port}/`;
const b = await chromium.launch({ channel: 'chrome' }).catch(() => chromium.launch());
const pg = await b.newPage({ viewport: { width: 1600, height: 900 } }); const erros = []; pg.on('pageerror', (e) => erros.push(e.message));
const ok = []; const log = (m, c) => ok.push((c ? 'ok    ' : 'FALHA ') + m);
await pg.goto(U, { waitUntil: 'load' }); await pg.waitForTimeout(800);
const n = () => pg.evaluate(() => [...document.querySelectorAll('.tela')].findIndex((t) => t.classList.contains('ativa')) + 1);
const idx = (tit) => pg.evaluate((t) => [...document.querySelectorAll('.tela')].findIndex((x) => x.dataset.titulo === t) + 1, tit);
const vai = async (i) => { await pg.evaluate((i) => { location.hash = '#' + i; }, i); await pg.waitForTimeout(900); };
// índice da reunião e do manual avançado
await vai(3);
log('índice da reunião lista capítulos 1 a 6', (await pg.locator('.tela.ativa .gr-t').count()) === 6);
await pg.locator('.tela.ativa .it', { hasText: 'Cards em massa' }).click(); await pg.waitForTimeout(900);
log('índice leva à tela certa', (await n()) === (await idx('Cards em massa por planilha')));
await vai(3); await pg.getByRole('button', { name: /Manual avançado, capítulos/ }).click(); await pg.waitForTimeout(900);
log('botão leva ao manual avançado', (await n()) === (await idx('Manual avançado')));
log('índice avançado lista capítulos 7 a 14', (await pg.locator('.tela.ativa .gr-t').count()) === 8);
await pg.screenshot({ path: path.join(saida, 'indice-avancado.jpg'), type: 'jpeg', quality: 70 });
// player
await vai(await idx('Cards em massa por planilha'));
log('chip de vídeo aparece na tela com vídeo', await pg.locator('#btVideo').isVisible());
await pg.locator('#btVideo').click(); await pg.waitForTimeout(2500);
const tocou = await pg.evaluate(() => { const v = document.getElementById('plVideo'); return { t: v.currentTime, err: v.error && v.error.code, rs: v.readyState }; });
log('vídeo abre e toca (t=' + tocou.t.toFixed(1) + ', readyState ' + tocou.rs + ')', tocou.t > 0.3 && !tocou.err);
await pg.screenshot({ path: path.join(saida, 'player.jpg'), type: 'jpeg', quality: 70 });
await pg.keyboard.press('Escape'); await pg.waitForTimeout(300);
log('Esc fecha o player e para o vídeo', !(await pg.locator('#player.aberto').count()));
await vai(await idx('Quem pode o quê'));
log('chip some em tela sem vídeo', !(await pg.locator('#btVideo').isVisible()));
// matriz
await pg.locator('.mz-p').nth(1).click(); await pg.waitForTimeout(300);
log('matriz destaca o papel Admin', (await pg.locator('.tela.ativa').getAttribute('data-col')) === '1' && /Configura a empresa/.test(await pg.locator('#mzTxt').textContent()));
// 15 pedidos e departamentos
await vai(await idx('Os 15 pedidos')); await pg.locator('.sq').nth(2).click(); await pg.waitForTimeout(300);
log('pedidos mostram a regra do RH', /Atestado/.test(await pg.locator('#sqR').textContent()));
log('são 15 pedidos', (await pg.locator('.tela.ativa .sq li').count()) === 15);
await vai(await idx('Quem vê cada departamento')); await pg.locator('.dp', { hasText: 'Compras' }).click(); await pg.waitForTimeout(300);
log('departamento mostra o primeiro clique', (await pg.locator('#dpN').textContent()) === 'Compras');
// vídeos e GIFs
await vai(await idx('Vídeos do manual'));
log('lista tem os 24 vídeos', (await pg.locator('.tela.ativa .vlist button').count()) === 24);
await pg.locator('.tela.ativa .vlist button').nth(15).click(); await pg.waitForTimeout(1500);
log('vídeo da lista abre', await pg.locator('#player.aberto').count() === 1);
await pg.keyboard.press('Escape'); await pg.waitForTimeout(300);
await vai(await idx('GIFs para compartilhar')); await pg.waitForTimeout(1500);
const gif = await pg.evaluate(() => { const i = document.getElementById('gifAtual'); return { src: i.getAttribute('src'), w: i.naturalWidth }; });
log('GIF carrega na tela (' + gif.src + ')', gif.w > 100);
await pg.screenshot({ path: path.join(saida, 'gifs.jpg'), type: 'jpeg', quality: 70 });
// página de vídeos
await pg.goto(U + 'videos.html', { waitUntil: 'load' }); await pg.waitForTimeout(600);
log('videos.html tem 24 vídeos', (await pg.locator('video').count()) === 24);
log('videos.html tem GIFs', (await pg.locator('#gifs img').count()) >= 20);
await pg.setViewportSize({ width: 390, height: 844 }); await pg.waitForTimeout(400);
log('videos.html cabe no celular', (await pg.evaluate(() => document.documentElement.scrollWidth)) <= 390);
await pg.screenshot({ path: path.join(saida, 'videos-celular.jpg'), type: 'jpeg', quality: 70 });
console.log(ok.join('\n')); console.log('erros', erros.slice(0, 5));
await b.close(); srv.close();
