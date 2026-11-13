import { createRequire } from 'node:module'; import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const require = createRequire(process.env.HOME + '/ariuno-orcamentos/package.json'); const { chromium } = require('playwright');
const raiz=process.argv[2], saida=process.argv[3];
const tipos={'.js':'text/javascript','.css':'text/css','.html':'text/html','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.txt':'text/plain'};
const srv=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);let f=path.join(raiz,p==='/'?'index.html':p);if(!fs.existsSync(f)){r.writeHead(404);return r.end();}r.writeHead(200,{'content-type':tipos[path.extname(f)]||'application/octet-stream'});fs.createReadStream(f).pipe(r);}).listen(0);
const URLB=`http://localhost:${srv.address().port}/`;
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1600,height:900}});const erros=[];pg.on('pageerror',e=>erros.push(e.message));
const ok=[];const log=(m,c)=>ok.push((c?'ok   ':'FALHA ')+m);
await pg.goto(URLB,{waitUntil:'load'});await pg.waitForTimeout(800);
const n=()=>pg.evaluate(()=>[...document.querySelectorAll('.tela')].findIndex(t=>t.classList.contains('ativa'))+1);
const idx=async(tit)=>pg.evaluate(t=>[...document.querySelectorAll('.tela')].findIndex(x=>x.dataset.titulo===t)+1,tit);
const vai=async(i)=>{await pg.evaluate(i=>{location.hash='#'+i},i);await pg.waitForTimeout(800);};
log('abre na capa',await n()===1);
await pg.getByRole('button',{name:/Começar a reunião/}).click();await pg.waitForTimeout(800);log('Começar vai para a agenda',await n()===2);
await pg.waitForTimeout(1300);log('cronômetro começou',/00:0[1-9]/.test(await pg.locator('#relogio').textContent()));
// passo a passo: seta anda passo antes de trocar de tela
const a=await idx('Passo 1 · Ajustes da empresa');await vai(a);
const on=()=>pg.evaluate(()=>[...document.querySelectorAll('.tela.ativa [data-p]')].findIndex(x=>x.classList.contains('on')));
const src=()=>pg.evaluate(()=>document.querySelector('.tela.ativa .vista img').getAttribute('src'));
log('tour começa no passo 1',await on()===0);
const s0=await src();await pg.keyboard.press('ArrowRight');await pg.waitForTimeout(500);log('seta anda um passo',await on()===1);log('passo troca a imagem',(await src())!==s0);
for(let i=0;i<3;i++){await pg.keyboard.press('ArrowRight');await pg.waitForTimeout(150);}log('chega no último passo',await on()===4&&await n()===a);
await pg.keyboard.press('ArrowRight');await pg.waitForTimeout(900);log('depois do último, troca de tela',await n()===a+1);
await pg.keyboard.press('ArrowLeft');await pg.waitForTimeout(900);log('volta uma tela',await n()===a);
// luz dentro do quadro
const luzOk=await pg.evaluate(()=>{const q=document.querySelector('.tela.ativa .quadro').getBoundingClientRect(),l=document.querySelector('.tela.ativa .luz').getBoundingClientRect();return l.width>10&&l.left>=q.left-2&&l.right<=q.right+2&&l.top>=q.top-2&&l.bottom<=q.bottom+2;});log('destaque dentro da tela',luzOk);
// clique em passo e autoplay
await pg.locator('.tela.ativa [data-p]').nth(2).click();await pg.waitForTimeout(400);log('clique escolhe o passo',await on()===2);await pg.waitForTimeout(6500);log('clique para o temporizador',await on()===2);
await vai(await idx('Passo 2 · Convidar o time'));await pg.waitForTimeout(9500);log('temporizador avança sozinho',await on()>=1);
// lightbox
await pg.locator('.tela.ativa .quadro').click();await pg.waitForTimeout(300);log('amplia a imagem',await pg.locator('#caixa.aberta').count()===1);await pg.keyboard.press('Escape');await pg.waitForTimeout(200);log('Esc fecha',await pg.locator('#caixa.aberta').count()===0);
// foco
await vai(await idx('Passo 4 · Clientes e projetos'));log('foco mostra título do passo',(await pg.locator('.tela.ativa .tit').textContent()).length>3);
// permissões
await vai(await idx('Simulador de permissões'));const r0=await pg.locator('#permRes').textContent();
await pg.locator('.area',{hasText:'RH'}).getByRole('button',{name:'Edita'}).click();await pg.waitForTimeout(200);log('liberar área muda contagem',(await pg.locator('#permRes').textContent())!==r0);log('menu mostra RH',await pg.locator('.menu-m .it',{hasText:'RH'}).count()===1);
await pg.locator('.area',{hasText:'Marketing'}).getByRole('button',{name:'Só acompanha'}).click();await pg.waitForTimeout(200);log('só acompanha marca no menu',await pg.locator('.menu-m .it em').count()===1);
// etapas
await vai(await idx('Sugestão de etapas'));await pg.locator('.segs button').nth(1).click();await pg.waitForTimeout(300);log('troca etapas por segmento',(await pg.locator('.col-m h4').first().textContent())==='Solicitação');
// checagem
await vai(await idx('Checagem da configuração'));for(let i=0;i<8;i++){await pg.locator('.chk button').nth(i).click();}await pg.waitForTimeout(500);log('checagem completa',/Empresa pronta/.test(await pg.locator('.barra span').textContent()));
// mini kanban
await vai(await idx('Experimente: arraste o card'));await pg.locator('.mcard .play').click();await pg.waitForTimeout(600);log('play conta tempo',(await pg.locator('.mcard time').textContent())!=='00:00:00');
const arrasta=async(c)=>{const m=await pg.locator('.mcard').boundingBox();const d=await pg.locator('.mk .col').nth(c).boundingBox();await pg.mouse.move(m.x+60,m.y+20);await pg.mouse.down();await pg.mouse.move(d.x+80,d.y+120,{steps:8});await pg.waitForTimeout(80);await pg.screenshot({path:path.join(saida,'arrastando.jpg'),type:'jpeg',quality:60});await pg.mouse.up();await pg.waitForTimeout(250);};
await arrasta(1);log('card foi para Criação',await pg.locator('.mk .col').nth(1).locator('.mcard').count()===1);
await arrasta(3);log('card em Concluído',await pg.locator('.mk .col').nth(3).locator('.mcard').count()===1);log('aviso de pronto',await pg.locator('#mkAviso.ok').count()===1);
const ant=await n();log('arrastar não trocou de tela',ant===await idx('Experimente: arraste o card'));
// automação
await vai(await idx('Monte uma automação'));await pg.locator('.bl[data-k=a] button').nth(1).click();await pg.waitForTimeout(150);log('frase da automação muda',/notificar o responsável/.test(await pg.locator('#autoFrase').textContent()));
// quiz
await vai(await idx('Teste rápido'));for(let i=0;i<4;i++){await pg.locator('.ops button').first().click();await pg.waitForTimeout(120);await pg.locator('#qProx').click();await pg.waitForTimeout(120);}
const t=await pg.locator('#qT').textContent();log('quiz termina: '+t,/Acertou|Gabaritou/.test(t));await pg.locator('#qProx').click();await pg.waitForTimeout(150);log('refazer volta à pergunta 1',(await pg.locator('#qN').textContent())==='1/4');
// sumário
await pg.locator('[data-sumario]').first().click();await pg.waitForTimeout(250);log('sumário abre',await pg.locator('#sumario.aberto').count()===1);await pg.locator('#sumLista button').nth(4).click();await pg.waitForTimeout(800);log('sumário navega',await n()>1&&await pg.locator('#sumario.aberto').count()===0);
// janelas menores
await pg.setViewportSize({width:1024,height:768});await vai(a);await pg.waitForTimeout(500);const g=await pg.evaluate(()=>{const r=document.getElementById('stage').getBoundingClientRect();return [Math.round(r.left),Math.round(innerWidth-r.right),document.documentElement.scrollWidth];});log('centralizado em 1024: '+g,Math.abs(g[0]-g[1])<=1&&g[2]<=1024);
await pg.setViewportSize({width:1600,height:900});await vai(1);await pg.waitForTimeout(400);await pg.screenshot({path:path.join(saida,'capa.jpg'),type:'jpeg',quality:75});
await vai(await idx('Passo 4 · Clientes e projetos'));await pg.waitForTimeout(300);await pg.screenshot({path:path.join(saida,'foco.jpg'),type:'jpeg',quality:75});
await vai(await idx('Passo 2 · Convidar o time'));await pg.locator('.tela.ativa [data-p]').nth(3).click();await pg.waitForTimeout(1000);await pg.screenshot({path:path.join(saida,'tour.jpg'),type:'jpeg',quality:82});
console.log(ok.join('\n'));console.log('erros',erros.slice(0,5));await b.close();srv.close();
