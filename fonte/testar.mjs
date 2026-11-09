// Abre o deck local, percorre as telas e aponta o que transborda ou se sobrepõe.
import { createRequire } from 'node:module'; import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const require = createRequire(process.env.HOME + '/ariuno-orcamentos/package.json'); const { chromium } = require('playwright');
const raiz=process.argv[2], saida=process.argv[3]; fs.mkdirSync(saida,{recursive:true});
const tipos={'.js':'text/javascript','.css':'text/css','.html':'text/html','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.txt':'text/plain'};
const srv=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);let f=path.join(raiz,p==='/'?'index.html':p);if(!fs.existsSync(f)){r.writeHead(404);return r.end();}r.writeHead(200,{'content-type':tipos[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r);}).listen(0);
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1600,height:900}});const erros=[];pg.on('pageerror',e=>erros.push(e.message));pg.on('console',m=>{if(m.type()==='error'&&!/fonts|404/.test(m.text()))erros.push(m.text());});
await pg.goto(`http://localhost:${srv.address().port}/?pdf=1#1`,{waitUntil:'load'});await pg.waitForTimeout(1200);
const total=await pg.evaluate(()=>document.querySelectorAll('.tela').length);const prob=[];
for(let n=1;n<=total;n++){await pg.evaluate(n=>{location.hash='#'+n},n);await pg.waitForTimeout(900);
 if(n===1)console.log('erros iniciais',erros.slice(0,4));
 const r=await pg.evaluate(()=>{const t=document.querySelector('.tela.ativa');if(!t)return {tit:'sem tela',out:['sem tela ativa'],h:0};const out=[];const lim={b:900-46};
  const vis=[...t.querySelectorAll('h1,h2,h3,p,li,.passo,.area,.quadro,.expl,.par,.dia,.pap,.bl,.frase,.barra,.aviso,.ops button')].filter(e=>e.offsetParent&&!e.closest('.vista'));
  for(const e of vis){const q=e.getBoundingClientRect();if(q.bottom>lim.b+1&&!t.classList.contains('l-foco')&&!t.classList.contains('s-capa')&&!t.classList.contains('s-fim'))out.push('passa do pé: '+(e.textContent||e.className).trim().slice(0,40)+' '+Math.round(q.bottom));if(q.right>1600-30)out.push('passa da direita: '+(e.textContent||e.className).trim().slice(0,40)+' '+Math.round(q.right));}
  const h=[...t.querySelectorAll('h2')].filter(e=>e.offsetParent);
  return {tit:t.dataset.titulo,out,h:h[0]?Math.round(h[0].getBoundingClientRect().height):0};});
 if(r.out.length)prob.push(n+' '+r.tit+': '+[...new Set(r.out)].slice(0,4).join(' | '));
 await pg.screenshot({path:path.join(saida,String(n).padStart(2,'0')+'.jpg'),type:'jpeg',quality:60});}
console.log('telas',total);console.log(prob.join('\n')||'sem transbordo');console.log('erros',erros.slice(0,6));
await b.close();srv.close();
