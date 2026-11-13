(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const stage=$('#stage'), telas=$$('.tela'), wipe=$('#wipe'), prog=$('#prog i'), cont=$('#cont'), capTxt=$('#capTxt');
const modoPdf=new URLSearchParams(location.search).has('pdf');
if(modoPdf)document.documentElement.classList.add('pdf');
const reduz=matchMedia('(prefers-reduced-motion: reduce)').matches||modoPdf;
let atual=0, escalaAtual=1, emTransicao=false, pendente=null;
const total=telas.length, dd=n=>String(n).padStart(2,'0');
const IMG='assets/telas/';

/* palco */
function escala(){escalaAtual=Math.min(innerWidth/1600,innerHeight/900);stage.style.transform='scale('+escalaAtual+')';}
addEventListener('resize',escala);escala();

/* navegação */
const aoEntrar=new Map();
function aplicar(n){
  pararAutos();
  telas[atual].classList.remove('ativa');
  atual=n;const t=telas[n];
  t.classList.add('ativa');
  stage.className='t-'+(t.dataset.tema||'claro')+(t.classList.contains('l-foco')?' t-foco':'');
  capTxt.textContent=t.dataset.cap||'';
  prog.style.width=((n+1)/total*100)+'%';
  cont.textContent=dd(n+1)+' / '+dd(total);
  $('#ant').disabled=n===0;$('#prox').disabled=n===total-1;
  $$('#sumLista button').forEach(b=>b.classList.toggle('atual',+b.dataset.i===n));
  history.replaceState(null,'','#'+(n+1));
  $$('img[data-src]',t).forEach(im=>{im.src=im.dataset.src;im.removeAttribute('data-src');});
  const bv=$('#btVideo');if(bv){const v=t.dataset.video;bv.hidden=!v;if(v)bv.dataset.v=v;}
  const fn=aoEntrar.get(t);if(fn)fn();
  iniciarAutos(t);
  [telas[n+1]].forEach(prox=>{if(prox)$$('[data-precarrega]',prox).forEach(e=>e.dispatchEvent(new Event('precarrega')));});
  if(n>0)ligarRelogio();
}
function ir(n){
  n=Math.max(0,Math.min(total-1,n));
  if(emTransicao){pendente=n;return;}
  if(n===atual)return;
  if(reduz||!wipe.animate){aplicar(n);return;}
  const dir=n>atual?1:-1;
  const de=dir>0?'inset(0 0 0 100%)':'inset(0 100% 0 0)', meio='inset(0 0 0 0)', para=dir>0?'inset(0 100% 0 0)':'inset(0 0 0 100%)';
  emTransicao=true;const ease='cubic-bezier(.7,0,.3,1)';
  wipe.animate([{clipPath:de},{clipPath:meio}],{duration:230,easing:ease,fill:'forwards'}).onfinish=()=>{
    aplicar(n);
    wipe.animate([{clipPath:meio},{clipPath:para}],{duration:260,easing:ease,fill:'forwards'}).onfinish=()=>{emTransicao=false;if(pendente!==null){const p=pendente;pendente=null;ir(p);}};
  };
}
// Seta para frente: dentro de um passo a passo, anda um passo; no fim, troca de tela.
function avancar(d){
  const t=telas[atual], tr=tours.get(t);
  if(tr){pararAutos();const j=tr.i+d;if(j>=0&&j<tr.n){tr.mostra(j);return;}}
  ir(atual+d);
}
addEventListener('hashchange',()=>{const n=parseInt(location.hash.slice(1),10);if(!isNaN(n))ir(n-1);});
$('#ant').addEventListener('click',e=>{e.stopPropagation();avancar(-1);});
$('#prox').addEventListener('click',e=>{e.stopPropagation();avancar(1);});
$$('[data-ir]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();ir(+b.dataset.ir-1);}));
$$('[data-ir-titulo]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();const i=telas.findIndex(t=>t.dataset.titulo===b.dataset.irTitulo);if(i>=0)ir(i);}));

/* sumário */
const sum=$('#sumario'), lista=$('#sumLista');let capAnt='';
telas.forEach((t,i)=>{
  const c=(t.dataset.cap||'').match(/^(\d+) · (.*)$/);
  if(c&&c[1]!==capAnt){capAnt=c[1];const h=document.createElement('li');h.className='cap-s';h.textContent=c[1]+' · '+c[2];lista.appendChild(h);}
  if(t.classList.contains('s-cap'))return;
  const li=document.createElement('li'), b=document.createElement('button');
  b.innerHTML='<b>'+dd(i+1)+'</b>';b.append(t.dataset.titulo||'');b.dataset.cursor='Ir';b.dataset.i=i;
  if(t.hasAttribute('data-novo')){const nv=document.createElement('span');nv.className='novo';nv.textContent='Novo';b.appendChild(nv);}
  b.addEventListener('click',e=>{e.stopPropagation();fecharSum();setTimeout(()=>ir(i),60);});
  li.appendChild(b);lista.appendChild(li);
});
function abrirSum(){sum.classList.add('aberto');}

/* tela de índice: capítulos em três colunas, cada linha leva à tela */
(function(){
  const caixas=$$('.ind');if(!caixas.length)return;
  const todos=[];let g=null;
  telas.forEach((t,i)=>{
    const c=(t.dataset.cap||'').match(/^(\d+) · (.*)$/);
    if(t.classList.contains('s-cap')&&c){g={n:c[1],nome:c[2],i,dur:($('.dur',t)||{}).textContent||'',itens:[]};todos.push(g);return;}
    if(!g||t.classList.contains('s-indice'))return;
    g.itens.push({i,tit:t.dataset.titulo||'',novo:t.hasAttribute('data-novo')});
  });
  const ir2=(b,i)=>{b.dataset.cursor='Ir';b.addEventListener('click',e=>{e.stopPropagation();ir(i);});};
  const peso=x=>1.5+x.itens.length;
  // N colunas seguidas, com a altura mais parecida possível
  function dividir(gs,n){
    if(n<=1||gs.length<=1)return[gs];let melhor=null;
    for(let a=1;a<=gs.length-n+1;a++){const resto=dividir(gs.slice(a),n-1),cols=[gs.slice(0,a),...resto],m=Math.max(...cols.map(c=>c.reduce((s,x)=>s+peso(x),0)));if(!melhor||m<melhor.m)melhor={m,cols};}
    return melhor.cols;}
  caixas.forEach(box=>{
  const [de,ate]=(box.dataset.caps||'1-99').split('-').map(Number);
  const grupos=todos.filter(x=>+x.n>=de&&+x.n<=ate);
  dividir(grupos,+box.dataset.cols||3).forEach(col=>{
    const d=document.createElement('div');d.className='colx';
    col.forEach(x=>{
      const gr=document.createElement('div');gr.className='gr';
      const h=document.createElement('button');h.className='gr-t';h.innerHTML='<u>'+x.n+'</u>';h.append(x.nome);
      const sm=document.createElement('small');sm.textContent=x.dur;h.appendChild(sm);ir2(h,x.i);gr.appendChild(h);
      x.itens.forEach(it=>{const b=document.createElement('button');b.className='it';b.innerHTML='<b>'+dd(it.i+1)+'</b>';const sp=document.createElement('span');sp.textContent=it.tit;b.appendChild(sp);
        if(it.novo){const nv=document.createElement('em');nv.className='novo';nv.textContent='Novo';b.appendChild(nv);}ir2(b,it.i);gr.appendChild(b);});
      d.appendChild(gr);});
    box.appendChild(d);});
  });
})();
function fecharSum(){sum.classList.remove('aberto');}
$$('[data-sumario]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();abrirSum();}));
$('.fechar',sum).addEventListener('click',e=>{e.stopPropagation();fecharSum();});

/* player dos vídeos curtos do manual */
const player=$('#player'),plVideo=$('#plVideo');
window.abrirVideo=id=>{const d=(window.VIDEOS||{})[id];if(!d)return;$('#plTit').textContent=d.titulo;$('#plSub').textContent=d.sub||'';
  plVideo.poster='assets/videos/'+id+'.jpg';plVideo.src='assets/videos/'+id+'.mp4';player.classList.add('aberto');plVideo.play().catch(()=>{});};
function fecharPlayer(){plVideo.pause();plVideo.removeAttribute('src');plVideo.load();player.classList.remove('aberto');}
$('.fechar',player).addEventListener('click',e=>{e.stopPropagation();fecharPlayer();});
player.addEventListener('click',e=>{if(e.target===player)fecharPlayer();});
const btv=$('#btVideo');if(btv)btv.addEventListener('click',e=>{e.stopPropagation();pararAutos();abrirVideo(btv.dataset.v);});
$$('[data-abre-video]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();pararAutos();abrirVideo(b.dataset.abreVideo);}));

/* lightbox */
const caixa=$('#caixa');
function fecharCaixa(){caixa.classList.remove('aberta');}
caixa.addEventListener('click',()=>fecharCaixa());

/* teclado, clique e toque */
addEventListener('keydown',e=>{
  if(player.classList.contains('aberto')){if(e.key==='Escape')fecharPlayer();return;}
  if(caixa.classList.contains('aberta')){if(e.key==='Escape')fecharCaixa();return;}
  if(sum.classList.contains('aberto')){if(e.key==='Escape')fecharSum();return;}
  if(['ArrowRight','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();avancar(1);}
  else if(['ArrowLeft','PageUp','Backspace'].includes(e.key)){e.preventDefault();avancar(-1);}
  else if(e.key==='Home')ir(0);else if(e.key==='End')ir(total-1);
  else if(e.key==='m'||e.key==='M')sum.classList.contains('aberto')?fecharSum():abrirSum();
});
const INTERATIVO='a,button,input,[data-cursor],.mcard,.quadro';
$('#wrap').addEventListener('click',e=>{
  if(e.target.closest(INTERATIVO)||sum.classList.contains('aberto')||player.classList.contains('aberto'))return;
  avancar(e.clientX>innerWidth/2?1:-1);
});
let x0=null,y0=null;
addEventListener('touchstart',e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)&&!e.target.closest('.mcard'))avancar(dx<0?1:-1);x0=null;});

/* cursor em dois tons: aparece sobre qualquer cor */
const cur=$('#cursor'),anel=$('#anel'),anelTxt=$('#anelTxt');let mx=innerWidth/2,my=innerHeight/2,ax=mx,ay=my;
addEventListener('mousemove',e=>{
  document.body.classList.add('tem-mouse');mx=e.clientX;my=e.clientY;
  cur.style.transform='translate('+mx+'px,'+my+'px)';
  const alvo=e.target.closest('[data-cursor],a,button,.quadro,.mcard');
  anel.classList.toggle('sobre',!!alvo);
  anelTxt.textContent=alvo?(alvo.dataset.cursor||''):'';
},{passive:true});
(function segue(){ax+=(mx-ax)*.24;ay+=(my-ay)*.24;anel.style.transform='translate('+ax+'px,'+ay+'px)';requestAnimationFrame(segue);})();

/* cronômetro da reunião: começa ao sair da capa, clique pausa */
const rel=$('#relogio');let iniciou=false,segCorridos=0,corre=false,tick=null;
function pintarRelogio(){const m=Math.floor(segCorridos/60),s=segCorridos%60;rel.textContent=dd(m)+':'+dd(s)+' de 60:00';rel.classList.toggle('passou',segCorridos>3600);}
function ligarRelogio(){if(iniciou||modoPdf)return;iniciou=true;corre=true;rel.classList.add('corre');tick=setInterval(()=>{if(corre){segCorridos++;pintarRelogio();}},1000);}
if(rel)rel.addEventListener('click',e=>{e.stopPropagation();if(!iniciou){ligarRelogio();return;}corre=!corre;rel.classList.toggle('corre',corre);});

/* temporizador: abre um passo por vez, no tempo de leitura; o primeiro clique para */
const autos=new Map();let autoAtivos=[];
const leitura=txt=>Math.max(4800,Math.min(12000,3200+String(txt||'').replace(/\s+/g,' ').trim().length*48));
function pararAutos(){autoAtivos.forEach(clearTimeout);autoAtivos=[];$$('.relogio-auto').forEach(r=>r.remove());}
function iniciarAutos(t){
  if(modoPdf)return;const cfg=autos.get(t);if(!cfg)return;
  const itens=cfg.itens(),n=itens.length;if(n<2)return;
  let i=0;
  function barra(k,dur){const a=itens[k];if(!a)return;const r=document.createElement('i');r.className='relogio-auto';a.appendChild(r);r.style.transitionDuration=dur+'ms';void r.offsetWidth;r.classList.add('corre');}
  function passo(){if(i+1>=n)return;$$('.relogio-auto',t).forEach(r=>r.remove());i++;cfg.vai(i);if(i+1>=n)return;const d=leitura(cfg.texto(i));barra(i,d);autoAtivos.push(setTimeout(passo,d));}
  const d=leitura(cfg.texto(0))+600;barra(0,d);autoAtivos.push(setTimeout(passo,d));
}
stage.addEventListener('pointerdown',e=>{if(e.isTrusted&&e.target.closest('.tela.ativa'))pararAutos();},true);
function roteiro(t,cfg){autos.set(t,cfg);}
// PDF: uma página por passo
window.__pdfEstados=()=>{const c=autos.get(telas[atual]);if(!c)return 0;const n=c.itens().length;return n>1?n:0;};
window.__pdfEstado=k=>{autos.get(telas[atual]).vai(k);};

/* passo a passo sobre a tela real */
const tours=new Map();
function montarTour(sec){
  const nome=sec.dataset.tour, cx=(window.CAIXAS||{})[nome]||[];
  const quadro=$('.quadro',sec), vista=$('.vista',sec), img=$('img',vista), luz=$('.luz',sec);
  const ops={regiao:sec.dataset.regiao?sec.dataset.regiao.split(',').map(Number):null,max:+sec.dataset.max||2.5,semLuz:sec.hasAttribute('data-semluz')};
  const passos=$$('[data-p]',sec), textos=$$('[data-txt]',sec).map(e=>e.textContent);
  const n=Math.min(cx.length,passos.length||textos.length);
  const fotos=[...new Set(cx.map(c=>c.f))];
  const carregar=()=>fotos.forEach(f=>{const im=new Image();im.src=IMG+f;});
  quadro.setAttribute('data-precarrega','');quadro.addEventListener('precarrega',carregar);
  const st={i:0,n,mostra};
  function mostra(i){
    st.i=i;const c=cx[i];if(!c)return;
    if(img.getAttribute('src')!==IMG+c.f)img.setAttribute('src',IMG+c.f);
    const W=quadro.clientWidth,H=quadro.clientHeight,k=W/1600,Himg=1000*k;
    let s,tx,ty;
    const foco=ops.regiao?{x:ops.regiao[0],y:ops.regiao[1],w:ops.regiao[2],h:ops.regiao[3]}:c;
    const cheia=sec.classList.contains('l-foco');
    s=Math.max(1,Math.min(ops.max,W*(cheia?.54:.8)/(foco.w*k),H*.72/(foco.h*k)));
    if(ops.regiao)s=Math.max(1,Math.min(W/(foco.w*k),H/(foco.h*k)));
    const a=(foco.x+foco.w/2)*k,b=(foco.y+foco.h/2)*k;
    const topoLivre=sec.classList.contains('l-foco')?92:0; // na tela cheia, o que está no alto da imagem desce para não ficar atrás do menu
    // na tela cheia o destaque vai para o lado oposto ao do cartão, para nunca ficar embaixo dele
    const cartaoEsq=a>W/2, centroX=cheia?(cartaoEsq?W*.67:W*.33):W/2;
    tx=Math.min(0,Math.max(W-W*s,centroX-a*s));ty=Math.min(topoLivre,Math.max(H-Himg*s,H/2-b*s));
    vista.style.transform='translate('+tx+'px,'+ty+'px) scale('+s+')';
    if(luz){
      if(ops.semLuz)luz.style.display='none';
      else{luz.style.left=(c.x*k*s+tx)+'px';luz.style.top=(c.y*k*s+ty)+'px';luz.style.width=(c.w*k*s)+'px';luz.style.height=(c.h*k*s)+'px';}
    }
    passos.forEach((p,j)=>{p.classList.toggle('on',j===i);p.classList.toggle('feito',j<i);});
    const atual=$('.atual',sec);
    if(atual){$('i',atual).textContent=i+1;$('b',atual).textContent=$('[data-t]',passos[i]||sec)?.textContent||textos[i]||'';$('span',atual).textContent=$('[data-d]',passos[i]||sec)?.textContent||'';}
    const expl=$('.expl',sec);
    if(expl){const p=passos[i];$('b',expl).textContent=p.dataset.tt||p.textContent;$('p',expl).textContent=p.dataset.dd||'';const sm=$('small',expl);if(sm)sm.textContent=p.dataset.ini||'';}
    const num=$('.num',sec);if(num)num.textContent='Passo '+(i+1)+' de '+n;
    const tit=$('.tit',sec),des=$('.des',sec);
    if(tit){tit.textContent=passos[i].dataset.tt;des.textContent=passos[i].dataset.dd;}
    const cart=$('.cartao',sec);
    if(cart){ // o cartão fica sempre do lado oposto ao destaque
      const ly=c.y*k*s+ty;const cW=430;
      let left=cartaoEsq?70:W-cW-70;
      cart.style.left=left+'px';cart.style.top=Math.max(84,Math.min(H-cart.offsetHeight-54,ly-40))+'px';
    }
  }
  passos.forEach((p,j)=>p.addEventListener('click',e=>{e.stopPropagation();pararAutos();mostra(j);}));
  quadro.addEventListener('click',e=>{e.stopPropagation();pararAutos();const c=cx[st.i];if(!c)return;$('#cxImg').src=IMG+c.f;caixa.classList.add('aberta');});
  tours.set(sec,st);
  aoEntrar.set(sec,()=>{carregar();requestAnimationFrame(()=>mostra(0));});
  roteiro(sec,{itens:()=>passos,texto:j=>passos[j].dataset.dd||passos[j].textContent,vai:j=>mostra(j)});
}
$$('[data-tour]').forEach(montarTour);

/* abas simples (cadeia e etapas por segmento) */
$$('[data-abas]').forEach(sec=>{
  const bts=$$(sec.dataset.abas,sec);if(!bts.length)return;
  const vai=i=>{bts.forEach((b,j)=>b.classList.toggle('on',j===i));sec.dispatchEvent(new CustomEvent('aba',{detail:i}));};
  bts.forEach((b,i)=>b.addEventListener('click',e=>{e.stopPropagation();pararAutos();vai(i);}));
  aoEntrar.set(sec,()=>vai(0));
  roteiro(sec,{itens:()=>bts,texto:i=>bts[i].dataset.t||'texto de apoio da etapa em exibição',vai});
});
const cadeia=$('.s-cadeia');
if(cadeia)cadeia.addEventListener('aba',e=>{const b=$$('.elo',cadeia)[e.detail];$('#cTit').textContent=b.textContent.trim();$('#cO').textContent=b.dataset.o;$('#cEx').textContent=b.dataset.ex;});
const SEG={
  ag:[['Briefing','Pedido entra aqui, com objetivo e prazo.'],['Criação','Quem produz puxa o card.'],['Aprovação interna','Revisão antes de sair de casa.'],['Aprovação do cliente','Aguardando retorno.'],['Produção','Aprovado, em execução.'],['Concluído','Entregue.']],
  ind:[['Solicitação','Área pede, com escopo.'],['Análise','Viabilidade e custo.'],['Execução','Time responsável.'],['Validação','Quem pediu confere.'],['Concluído','Pronto e registrado.']],
  serv:[['Entrada','Novo atendimento.'],['Diagnóstico','Entender o caso.'],['Em andamento','Trabalho rodando.'],['Aguardando cliente','Depende de retorno.'],['Concluído','Caso fechado.'],['Perdido','Não seguiu.']]};
const seg=$('.s-etapas');
if(seg)seg.addEventListener('aba',e=>{const k=$$('.segs button',seg)[e.detail].dataset.s,box=$('.col-m',seg);box.innerHTML='';SEG[k].forEach((c,i)=>{const d=document.createElement('div');d.style.animationDelay=(i*50)+'ms';if(/Conclu/.test(c[0]))d.className='fim';const h=document.createElement('h4');h.textContent=c[0];const p=document.createElement('p');p.textContent=c[1];d.append(h,p);box.appendChild(d);});});

/* tarefa principal, subtarefa e checklist */
const plan=$('.s-plan');
if(plan)plan.addEventListener('aba',e=>{const b=$$('.pl-l',plan)[e.detail];plan.classList.add('tem-foco');$$('.mc',plan).forEach(c=>c.classList.toggle('on',c.dataset.r===String(e.detail)));$('#plN').textContent='Linha '+b.dataset.n+' da planilha';$('#plT').textContent=b.dataset.tt;$('#plP').textContent=b.dataset.dd;});
/* matriz de papéis, os 15 pedidos e os departamentos */
const mz=$('.s-matriz');
if(mz)mz.addEventListener('aba',e=>{mz.dataset.col=e.detail;$('#mzTxt').textContent=$$('.mz-p',mz)[e.detail].dataset.t;});
const sg=$('.s-gifs');
if(sg)sg.addEventListener('aba',e=>{const b=$$('.gl button',sg)[e.detail];$('#gifAtual').src=b.dataset.gif;});
const sol=$('.s-solic');
if(sol)sol.addEventListener('aba',e=>{$('#sqR').textContent=$$('.sq',sol)[e.detail].dataset.r;});
const dps=$('.s-deptos');
if(dps)dps.addEventListener('aba',e=>{const b=$$('.dp',dps)[e.detail];$('#dpN').textContent=b.textContent;$('#dpO').textContent=b.dataset.o;$('#dpP').textContent=b.dataset.p;});
const hier=$('.s-hier');
if(hier)hier.addEventListener('aba',e=>{const b=$$('.niv',hier)[e.detail];hier.dataset.foco=b.dataset.n;$('#hNome').textContent=b.dataset.nome;$('#hO').textContent=b.dataset.o;$('#hOnde').textContent=b.dataset.onde;$('#hQ').textContent=b.dataset.q;});

/* onde isso entra: um caso por vez */
(function(){
  const s=$('.s-onde');if(!s)return;const C=JSON.parse($('#ondeDados').textContent);let i=0,resp=false,acertos=0;
  const bs=$$('.tres button',s),fila=$('#oFila');
  fila.innerHTML=C.map(()=>'<i></i>').join('');
  function pinta(){resp=false;$('#oN').textContent='Caso '+(i+1)+' de '+C.length;$('#oT').textContent=C[i].t;$('#oP').textContent='';bs.forEach(b=>b.className='');$$('i',fila).forEach((x,k)=>{if(k===i)x.className='agora';});}
  bs.forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();pararAutos();
    if(resp){if(i+1<C.length){i++;pinta();}else{i=0;acertos=0;$$('i',fila).forEach(x=>x.className='');pinta();}return;}
    resp=true;const c=+b.dataset.c,ok=c===C[i].c;if(ok)acertos++;
    bs[C[i].c].classList.add('certa');if(!ok)b.classList.add('errada');
    $$('i',fila)[i].className=ok?'ok':'nao';
    $('#oP').textContent=(ok?'Isso. ':'Quase. ')+C[i].p+(i+1<C.length?' Clique em qualquer opção para o próximo caso.':' Fim: '+acertos+' de '+C.length+'. Clique para recomeçar.');}));
  pinta();
  if(modoPdf){bs[C[0].c].classList.add('certa');$('#oP').textContent=C[0].p;}
})();

/* simulador de permissões */
(function(){
  const s=$('.s-perm');if(!s)return;
  const FIXOS=['Mural & Recados','Relatórios','Tarefas','Timesheet','Planner','Projetos','Clientes','Solicitações','Meu Portal'];
  const AREAS=['Comercial','Compras','Criação','Estoque','Impulsionamento','Marketing','RH','RP','Social Mídia','Tráfego'];
  const est={Criação:'edita'};
  const box=$('.areas',s),menu=$('.menu-m',s),res=$('#permRes');
  AREAS.forEach(a=>{
    const d=document.createElement('div');d.className='area';d.dataset.a=a;d.innerHTML='<span></span><div class="ch"></div>';d.firstChild.textContent=a;
    [['','Sem acesso'],['edita','Edita'],['ve','Só acompanha']].forEach(([v,r])=>{const b=document.createElement('button');b.textContent=r;b.dataset.v=v;b.dataset.cursor='';b.addEventListener('click',e=>{e.stopPropagation();pararAutos();if(v)est[a]=v;else delete est[a];pinta(a);});d.lastChild.appendChild(b);});
    box.appendChild(d);
  });
  function pinta(novo){
    $$('.area',box).forEach(d=>{const v=est[d.dataset.a]||'';d.classList.toggle('lig',!!v);$$('button',d).forEach(b=>b.classList.toggle('on',b.dataset.v===v));});
    menu.innerHTML='<h4>Principal</h4>'+FIXOS.map(f=>'<div class="it">'+f+'</div>').join('')+'<h4>Departamentos</h4>';
    const lig=AREAS.filter(a=>est[a]);
    lig.forEach(a=>{const it=document.createElement('div');it.className='it'+(a===novo?' nv':'');it.textContent=a;if(est[a]==='ve'){const m=document.createElement('em');m.textContent='SÓ VÊ';it.appendChild(m);}menu.appendChild(it);});
    if(!lig.length){const it=document.createElement('div');it.className='it';it.textContent='Nenhuma área liberada';menu.appendChild(it);}
    res.textContent=lig.length+(lig.length===1?' área liberada':' áreas liberadas')+' para esta pessoa';
  }
  pinta();
})();

/* mini kanban */
(function(){
  const s=$('.s-mk');if(!s)return;
  const card=$('.mcard',s),cols=$$('.col',s),aviso=$('#mkAviso'),play=$('.play',card),rel=$('time',card);
  let seg2=0,t=null;
  const ROT=['Dê o Play no card: o tempo começa a contar.','Agora arraste o card para a próxima etapa.','Isso. Arraste até Concluído para fechar.','Concluído: o tempo fica registrado no card e vai para os relatórios.'];
  function msg(i,ok){aviso.lastChild.textContent=ROT[i];$('i',aviso).textContent=ok?'Pronto':'Passo '+(i+1);aviso.classList.toggle('ok',!!ok);}
  function fmt(x){return dd(Math.floor(x/3600))+':'+dd(Math.floor(x/60)%60)+':'+dd(x%60);}
  play.addEventListener('click',e=>{e.stopPropagation();pararAutos();if(t){clearInterval(t);t=null;play.classList.remove('on');play.lastChild.textContent='Trabalhar';return;}
    t=setInterval(()=>{seg2+=60;rel.textContent=fmt(seg2);},450);play.classList.add('on');play.lastChild.textContent='Pausar';if(card.parentElement===cols[0])msg(1);});
  card.addEventListener('pointerdown',e=>{
    if(e.target.closest('.play'))return;e.preventDefault();card.setPointerCapture(e.pointerId);
    const orig=card.getBoundingClientRect(),dx=e.clientX-orig.left,dy=e.clientY-orig.top;let solto=false;
    const mov=ev=>{if(!solto){solto=true;card.classList.add('arr');card.style.width=orig.width/escalaAtual+'px';card.style.transformOrigin='0 0';}
      card.style.left='0';card.style.top='0';card.style.transform='translate('+(ev.clientX-dx)+'px,'+(ev.clientY-dy)+'px) scale('+escalaAtual+') rotate(2deg)';
      cols.forEach(c=>c.classList.toggle('sobre',dentro(c,ev)));};
    const dentro=(c,ev)=>{const r=c.getBoundingClientRect();return ev.clientX>=r.left&&ev.clientX<=r.right&&ev.clientY>=r.top&&ev.clientY<=r.bottom;};
    const fim=ev=>{card.removeEventListener('pointermove',mov);card.removeEventListener('pointerup',fim);card.classList.remove('arr');card.style.cssText='';cols.forEach(c=>c.classList.remove('sobre'));
      if(!solto)return;const alvo=cols.find(c=>dentro(c,ev));if(alvo&&alvo!==card.parentElement){alvo.appendChild(card);const i=cols.indexOf(alvo);if(i===cols.length-1){if(t){clearInterval(t);t=null;play.classList.remove('on');play.lastChild.textContent='Trabalhar';}msg(3,true);}else if(i>0)msg(2);}};
    card.addEventListener('pointermove',mov);card.addEventListener('pointerup',fim);
  });
  msg(0);
})();

/* montador de automação */
(function(){
  const s=$('.s-auto');if(!s)return;const f=$('#autoFrase'),esc={};
  const pinta=()=>{const q=esc.q,c=esc.c,a=esc.a;f.innerHTML='<small>A regra que você acabou de montar</small>';f.append('Quando ');const e1=document.createElement('em');e1.textContent=q;f.append(e1,', ');f.append('se ');const e2=document.createElement('em');e2.textContent=c;f.append(e2,', o Ariuno vai ');const e3=document.createElement('em');e3.textContent=a;f.append(e3,'.');};
  $$('.bl',s).forEach(bl=>{const k=bl.dataset.k,bs=$$('button',bl);const marca=b=>{bs.forEach(x=>x.classList.toggle('on',x===b));esc[k]=b.dataset.v;pinta();};bs.forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();pararAutos();marca(b);}));marca(bs[0]);});
})();

/* checagem da implantação */
(function(){
  const s=$('.s-chk');if(!s)return;const bs=$$('.chk button',s),b=$('.barra i',s),t=$('.barra span',s);
  const pinta=()=>{const n=bs.filter(x=>x.classList.contains('on')).length;b.style.width=(n/bs.length*100)+'%';t.textContent=n===bs.length?'Empresa pronta. Pode chamar o time.':n+' de '+bs.length+' passos feitos';};
  bs.forEach(x=>x.addEventListener('click',e=>{e.stopPropagation();pararAutos();x.classList.toggle('on');$('i',x).textContent=x.classList.contains('on')?'✓':'';pinta();}));
  if(modoPdf)bs.slice(0,0).forEach(x=>x.click());
  pinta();
})();

/* teste rápido */
(function(){
  const s=$('.s-quiz');if(!s)return;
  const Q=JSON.parse($('#quizDados').textContent);let i=0,pts=0,resp=false,fim=false;
  const tit=$('#qT'),ops=$('.ops',s),num=$('#qN'),por=$('#qP'),prox=$('#qProx');
  function pinta(){resp=false;const q=Q[i];num.textContent=(i+1)+'/'+Q.length;tit.textContent=q.q;por.textContent='';prox.style.display='none';ops.innerHTML='';
    q.a.forEach((a,j)=>{const b=document.createElement('button');b.textContent=a;b.dataset.cursor='';b.addEventListener('click',e=>{e.stopPropagation();pararAutos();if(resp)return;resp=true;if(j===q.c)pts++;[...ops.children].forEach((x,k)=>{if(k===q.c)x.classList.add('certa');else if(k===j)x.classList.add('errada');});por.textContent=q.p;prox.style.display='';prox.firstChild.textContent=i+1<Q.length?'Próxima pergunta →':'Ver resultado →';});ops.appendChild(b);});}
  prox.addEventListener('click',e=>{e.stopPropagation();
    if(fim){fim=false;i=0;pts=0;pinta();return;}
    if(i+1<Q.length){i++;pinta();return;}
    fim=true;tit.textContent=pts===Q.length?'Gabaritou. O time está pronto.':'Acertou '+pts+' de '+Q.length+'. Revise os passos no índice.';num.textContent=pts+'/'+Q.length;ops.innerHTML='';por.textContent='';prox.firstChild.textContent='Refazer o teste';});
  pinta();
  if(modoPdf)ops.firstChild&&ops.children[Q[0].c].classList.add('certa');
})();

/* início */
const h=parseInt(location.hash.slice(1),10);
const n0=isNaN(h)?0:Math.max(0,Math.min(total-1,h-1));
atual=n0===0?1:0;telas.forEach(t=>t.classList.remove('ativa'));aplicar(n0);
if(n0===0&&total>1)telas[1].classList.remove('ativa');
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(()=>{const st=tours.get(telas[atual]);if(st)st.mostra(st.i);});
})();
