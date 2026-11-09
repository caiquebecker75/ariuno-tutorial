// Tira as fotos do passo a passo na DEMONSTRAÇÃO do Ariuno (dados fictícios) e
// guarda, para cada passo, a imagem e o retângulo do elemento a destacar.
//   node fonte/capturar.mjs <pasta dist do Ariuno>
import { createRequire } from 'node:module';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
const require = createRequire(process.env.HOME + '/ariuno-orcamentos/package.json');
const { chromium } = require('playwright');
const raiz = process.argv[2]; const so = process.argv[3] ? process.argv[3].split(',') : null;
const AQUI = path.dirname(fileURLToPath(import.meta.url)); const SAIDA = path.join(AQUI, '../assets/telas'); fs.mkdirSync(SAIDA, { recursive: true });
const tipos = { '.js':'text/javascript','.css':'text/css','.html':'text/html','.json':'application/json','.webmanifest':'application/json','.svg':'image/svg+xml','.png':'image/png' };
const srv = http.createServer((q,r)=>{ let p = decodeURIComponent(q.url.split('?')[0]); let f = path.join(raiz,p); if(!fs.existsSync(f)||fs.statSync(f).isDirectory()) f = path.join(raiz,'index.html'); r.writeHead(200,{'content-type':tipos[path.extname(f)]||'application/octet-stream'}); fs.createReadStream(f).pipe(r); }).listen(0);
const b = await chromium.launch({ headless:true });
const c = await b.newContext({ viewport:{width:1600,height:1000}, deviceScaleFactor:1.5, serviceWorkers:'block', locale:'pt-BR' });
const p = await c.newPage(); const erros=[]; p.on('pageerror',e=>erros.push(String(e).slice(0,200)));
await p.route('**/api/admin/convites', r => r.fulfill({status:200,contentType:'application/json',body:JSON.stringify({ok:true,link:'https://ariuno.com.br/?convite=seu-link-pessoal',emailEnviado:true})}));
await p.route('**/api/empresa/assentos*', r => r.fulfill({status:200,contentType:'application/json',body:JSON.stringify({empresa:'demo',limite:15,ativos:13,livres:2})}));
await p.goto(`http://localhost:${srv.address().port}/?demo=1`,{waitUntil:'domcontentloaded',timeout:90000});
await p.waitForFunction(()=>document.body.innerText.includes('Tarefas'),null,{timeout:90000});
await p.waitForTimeout(900);
await p.addStyleTag({content:`#task-onboarding-tour-root{display:none!important} div.fixed.left-4.z-\\[200\\]{display:none!important} ::-webkit-scrollbar{display:none}`});
// O que só o dono da plataforma enxerga sai da foto: é o que a empresa nova vai ver.
await p.evaluate(()=>{
  const ESCONDER=/^(Visão Master|Financeiro|Importar dados|Diretoria|Backups)$/;
  const limpar=()=>{
    document.querySelectorAll('button').forEach(b=>{ if(ESCONDER.test((b.textContent||'').trim())) b.style.display='none'; });
    document.querySelectorAll('select').forEach(s=>{ const t=s.textContent||''; if(/Agência Demo/.test(t)&&/Todas as empresas/.test(t)) s.style.display='none'; else if(/Agência Demo/.test(t)&&s.closest('aside,nav')){ let n=s; for(let i=0;i<4&&n.parentElement;i++){ n=n.parentElement; if(/Plataforma/i.test(n.textContent||'')) { n.style.display='none'; break; } } } });
    const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
    let n; while(n=w.nextNode()){ const v=n.nodeValue; if(!v||!/Demonstra|Superadmin|Boa tarde, Você|Bom dia, Você|Boa noite, Você/i.test(v)) continue; n.nodeValue=v.replace(/Você \(Demonstração\)/g,'Marina Alves').replace(/Superadmin/gi,'Admin').replace(/(Boa tarde|Bom dia|Boa noite), Você/g,'$1, Marina'); }
  };
  limpar(); setInterval(limpar,120);
});
const dorme=(ms)=>p.waitForTimeout(ms);
await p.evaluate(()=>{ for (const bt of document.querySelectorAll('button')) { const t=(bt.textContent||'').trim(); if (/^(Departamentos|Administração)$/i.test(t)) bt.click(); } }); await dorme(300);

const CAIXAS={}; let tour=null, atual=null, n=0, foto=null;
const seguro=async(f,rot)=>{ try{ return await f(); }catch(e){ console.log('  FALHOU', tour, rot||'', String(e.message).split('\n')[0].slice(0,120)); return null; } };
const menu=async(rot)=>{ const ok=await p.evaluate((r)=>{ const bt=[...document.querySelectorAll('aside button,nav button,button')].find(x=>(x.textContent||'').trim().replace(/\s*\d+$/,'')===r); if(bt){bt.click();return true;} return false; },rot); if(!ok) console.log('  sem menu',rot); await dorme(1300); };
const novoTour=(nome)=>{ tour=nome; CAIXAS[nome]=[]; n=0; foto=null; };
const clicar=(loc)=>loc.first().click({timeout:6000});
async function tirar(){ await dorme(350); n++; const nome=`${tour}-${n}.jpg`; await p.screenshot({path:path.join(SAIDA,nome),type:'jpeg',quality:76}); foto=nome; }
// passo(alvo, {nova}): alvo é um Locator (ou lista, junta os retângulos). nova=true tira foto nova.
async function passo(alvo,{nova=true,folga=8,rolar=true}={}){
  await seguro(async()=>{
    const lista=Array.isArray(alvo)?alvo:[alvo];
    const ret=[]; for(const a of lista){ const l=a.first(); if(rolar) await l.scrollIntoViewIfNeeded({timeout:4000}).catch(()=>{}); }
    await dorme(120);
    for(const a of lista){ const r=await a.first().boundingBox({timeout:4000}); if(r) ret.push(r); }
    if(!ret.length) throw new Error('sem alvo');
    if(nova||!foto) await tirar();
    const x0=Math.max(0,Math.min(...ret.map(r=>r.x))-folga), y0=Math.max(0,Math.min(...ret.map(r=>r.y))-folga);
    const x1=Math.min(1600,Math.max(...ret.map(r=>r.x+r.width))+folga), y1=Math.min(1000,Math.max(...ret.map(r=>r.y+r.height))+folga);
    CAIXAS[tour].push({f:foto,x:Math.round(x0),y:Math.round(y0),w:Math.round(x1-x0),h:Math.round(y1-y0)});
  },'passo '+(CAIXAS[tour].length+1));
}
const bt=(t)=>p.getByRole('button',{name:t});
const btExato=(t)=>p.getByRole('button',{name:t,exact:true});
const ph=(t)=>p.getByPlaceholder(t);
const tx=(t,o)=>p.getByText(t,o);
const modal=()=>p.locator('div.fixed.inset-0').filter({has:p.locator('input,select,textarea')}).last().locator('> div').first();
const fecharCancelar=async()=>{ await seguro(()=>p.locator('div.fixed.inset-0').last().getByRole('button',{name:/Cancelar/}).first().click({timeout:3000}),'cancelar'); await dorme(400); };
const quer=(k)=>!so||so.includes(k);
const limpar=async()=>{ for(let i=0;i<4;i++){ const m=p.locator('div.fixed.inset-0[class*="bg-slate-900"]'); if(!(await m.count())) return; const u=m.last();
  const c=u.getByRole('button',{name:/Cancelar|Concluir|Fechar|Pronto/}); if(await c.count()) await c.first().click({timeout:1500}).catch(()=>{}); else { const x=u.locator('button:has(svg.lucide-x)'); if(await x.count()) await x.first().click({timeout:1500}).catch(()=>{}); else await u.locator('button').last().click({timeout:1500}).catch(()=>{}); } await dorme(350); } };
const roteiro=async(k,f)=>{ if(!quer(k)) return; try{ await f(); }catch(e){ console.log('ROTEIRO FALHOU',k,String(e.message).split('\n')[0].slice(0,160)); } await limpar(); };

// ---------------------------------------------------------- empresa
await roteiro('ajustes',async()=>{ novoTour('ajustes');
  await menu('Tarefas');
  await passo(btExato('Ajustes da empresa'));
  await menu('Ajustes da empresa');
  await passo([btExato('Usuários'),btExato('Saúde do Sistema')],{folga:12});
  await clicar(btExato('Tarefas').last()); await dorme(500);
  await passo(p.locator('main h2').filter({hasText:'Tarefas'}).locator('xpath=ancestor::div[3]'));
  await clicar(btExato('Aparência e Marca')); await dorme(500);
  await passo(tx('Identidade e Logo').locator('xpath=ancestor::div[2]'));
  await passo(bt('Salvar e Aplicar'),{nova:false});
});
await roteiro('time',async()=>{ novoTour('time');
  await passo(btExato('Gestão de Equipe'));
  await menu('Gestão de Equipe');
  await passo(bt('Convidar pessoa'));
  await clicar(bt('Convidar pessoa')); await dorme(500);
  await ph('pessoa@empresa.com.br').fill('nova.pessoa@suaempresa.com.br');
  await p.locator('div.fixed input[type=text]').first().fill('Nova Pessoa').catch(()=>{});
  await passo(tx('Abrir assento').locator('xpath=ancestor::div[2]'));
  const sel=p.locator('select').filter({has:p.locator('option',{hasText:'Não copiar'})});
  await sel.selectOption({index:3}).catch(()=>{}); await dorme(200);
  await passo(sel.locator('xpath=parent::div'));
  await clicar(bt('Liberar e enviar')); await dorme(700);
  await passo(tx('Acesso liberado').locator('xpath=ancestor::div[3]'));
});
await roteiro('permissoes',async()=>{ novoTour('permissoes');
  await menu('Gestão de Equipe');
  await clicar(p.locator('button[title="Editar Usuário"]').nth(2)); await dorme(600);
  const band=tx('Copiar configuração de outro usuário').locator('xpath=parent::div');
  await passo(band);
  await passo(tx('Permissões e Acessos').locator('xpath=parent::div'));
  await passo(tx('Acesso a Módulos e Departamento').locator('xpath=parent::div'));
  await passo(tx('Colunas visíveis por quadro').locator('xpath=ancestor::div[2]'));
  await p.locator('div.fixed.inset-0').last().getByRole('button',{name:/Salvar/}).first().scrollIntoViewIfNeeded();
  await passo(p.locator('div.fixed.inset-0').last().getByRole('button',{name:/Salvar/}).first());
  await fecharCancelar();
});
await roteiro('clientes',async()=>{ novoTour('clientes');
  await menu('Clientes');
  await passo(bt('Novo cliente'));
  await clicar(bt('Novo cliente')); await dorme(600);
  await passo(modal(),{rolar:false});
  await fecharCancelar();
  await p.keyboard.press('Escape'); await dorme(200);
  await seguro(()=>p.locator('div.fixed.inset-0 button:has(svg.lucide-x)').last().click({timeout:1500}));
  await dorme(300);
  await menu('Projetos');
  await passo(bt('Novo Projeto'));
  await clicar(bt('Novo Projeto')); await dorme(600);
  await passo(modal(),{rolar:false});
  await fecharCancelar();
  await seguro(()=>p.locator('div.fixed.inset-0 button:has(svg.lucide-x)').last().click({timeout:1500}));
  await dorme(300);
});
await roteiro('quadro',async()=>{ novoTour('quadro');
  await menu('Tarefas');
  await passo([p.locator('select.font-display'),p.locator('button[title="Novo Quadro"]')],{folga:10});
  await clicar(p.locator('button[title="Novo Quadro"]')); await dorme(500);
  await passo(modal(),{rolar:false});
  await fecharCancelar();
  await seguro(()=>p.locator('div.fixed.inset-0 button:has(svg.lucide-x)').last().click({timeout:1500}));
  await dorme(300);
  const cab=p.locator('.group\\/header').first();
  await passo(p.locator('.group\\/header').nth(0));
  await cab.hover(); await dorme(200);
  await clicar(cab.locator('button').last()); await dorme(500);
  await passo(tx('Conclusão',{exact:true}).locator('xpath=ancestor::div[2]'));
  await p.keyboard.press('Escape'); await p.mouse.click(1200,920); await dorme(400);
});
await roteiro('modelos',async()=>{ novoTour('modelos');
  await menu('Tipos de Tarefa');
  await passo(bt('Novo Tipo'));
  await menu('Modelos de Projeto');
  await passo(btExato('Novo modelo'));
  await clicar(btExato('Novo modelo')); await dorme(500);
  const cria=async(nome,grupo,titulo,subs)=>{ await ph('Ex.: Artigo').fill(nome); await ph('Ex.: Imprensa | RP').fill(grupo); await ph('Ex.: [Artigo] [Tema]').fill(titulo);
    const q=p.locator('select').filter({has:p.locator('option',{hasText:'O quadro aberto na hora'})}); const v=await q.evaluate(s=>[...s.options].map(o=>o.value).filter(Boolean)[0]); await q.selectOption(v); await dorme(200);
    const e=p.locator('select').filter({has:p.locator('option',{hasText:'A primeira do quadro'})}); const es=await e.evaluate(s=>[...s.options].map(o=>o.value).filter(Boolean)); await e.selectOption(es[1]);
    await p.locator('div[contenteditable]').click(); await p.keyboard.type('Objetivo, público e referências do job.');
    for(const [i,t] of subs.entries()){ await bt('Adicionar subtarefa').click(); await ph('O que fazer').last().fill(t); await p.locator('select').filter({has:p.locator('option',{hasText:'Mesma etapa do card'})}).last().selectOption(es[Math.min(i+1,es.length-1)]); }
    return true; };
  await cria('Campanha digital','Marketing','[Campanha] [Cliente] [Mês]',['Fechar briefing','Criar as peças','Aprovar com o cliente']);
  await passo(tx('Nome do modelo').locator('xpath=ancestor::div[3]'));
  await passo(tx(/^Subtarefas ·/).locator('xpath=ancestor::div[2]'));
  await clicar(bt('Criar modelo')); await dorme(700);
  await menu('Tarefas'); await menu('Modelos de Projeto');
  await clicar(btExato('Novo modelo')); await dorme(400);
  await cria('Material de ponto de venda','Trade','[PDV] [Peça]',['Levantar medidas','Criar arte','Enviar à produção']); await clicar(bt('Criar modelo')); await dorme(600);
  await menu('Tarefas'); await menu('Modelos de Projeto');
  await clicar(btExato('Novo modelo')); await dorme(400);
  await cria('Relatório mensal','Rotinas','[Relatório] [Mês]',['Coletar números','Revisar','Enviar']); await clicar(bt('Criar modelo')); await dorme(600);
  await menu('Tarefas'); await menu('Modelos de Projeto');
  await passo(tx('Modelos de tarefa',{exact:true}).locator('xpath=ancestor::div[3]'));
});
await roteiro('fecho',async()=>{ novoTour('fecho');
  await menu('Feriados');
  await passo(bt('Novo feriado'));
  await menu('Integrações');
  await passo(bt('Conectar').first());
});
// ---------------------------------------------------------- dia a dia
await roteiro('criar',async()=>{ novoTour('criar');
  await menu('Tarefas');
  await passo(bt('Nova Tarefa').first());
  await clicar(bt('Nova Tarefa')); await dorme(600);
  await passo(tx('Começar de um modelo').locator('xpath=ancestor::div[2]'));
  await seguro(()=>clicar(p.getByRole('button',{name:/Campanha digital/})),'modelo'); await dorme(300);
  const t=ph(/O que precisa/).first();
  await t.fill('[Campanha] Kompra Supermercados, Dezembro');
  await passo(t);
  await passo(tx('Responsável',{exact:true}).locator('xpath=ancestor::div[2]'));
  await passo(bt(/Criar tarefa/),{nova:false});
  await clicar(bt(/Criar tarefa/)); await dorme(900);
  // mais cards para a pauta da pessoa
  for(const nome of ['Fechar cronograma do cliente','Revisar arte do encarte','Enviar relatório da semana']){ await clicar(bt('Nova Tarefa')); await dorme(450); await ph(/O que precisa/).first().fill(nome); await clicar(bt(/Criar tarefa/)); await dorme(650); }
});
await roteiro('pauta',async()=>{ novoTour('pauta');
  await menu('Meu Portal');
  await passo(p.locator('main h1').first().locator('xpath=ancestor::div[2]'),{folga:14});
  await passo(p.locator('main table').first(),{nova:false});
});
await roteiro('card',async()=>{ novoTour('card');
  await menu('Tarefas');
  await clicar(tx('KOMPRA, Catálogo de Produtos 2025')); await dorme(1200);
  for(const rot of ['Descrição','Checklist','Subtarefas','Comentários','Anexos','Cronograma','Painel de Controle','Registros de Tempo']){
    await seguro(async()=>{ await p.evaluate((r)=>{ const b=[...document.querySelectorAll('div.fixed button')].find(x=>(x.textContent||'').trim().replace(/\s*\d+$/,'')===r); b&&b.click(); },rot); await dorme(650);
      if(rot==='Checklist'){ if(await bt('Novo checklist').count()){ if(!(await ph('Adicionar item...').count())) await bt('Novo checklist').click(); await dorme(200);
        for(const i of ['Validar medidas com o cliente','Enviar arte para aprovação','Conferir prova de cor']){ await ph('Adicionar item...').first().fill(i); await p.keyboard.press('Enter'); await dorme(120);} 
        const rs=p.locator('select[title="Responsável por este item"]'); const k=await rs.count(); for(let j=0;j<Math.min(k,3);j++){ await rs.nth(j).selectOption({index:1+j}); } await dorme(200);} }
      const aba=p.locator('div.fixed button').filter({hasText:new RegExp('^\\s*'+rot)}).first();
      await passo([aba],{folga:10}); },rot);
  }
  await p.evaluate(()=>{ const b=[...document.querySelectorAll('div.fixed button')].find(x=>(x.textContent||'').trim()==='Descrição'); b&&b.click(); }); await dorme(400);
  novoTour('trabalhar');
  await passo(p.locator('div.fixed').getByRole('button',{name:/^\s*Play\s*$/}).first());
  await passo(p.locator('div.fixed').getByRole('button',{name:/^\s*Concluir\s*$/}).first(),{nova:false});
  await passo(tx('Detalhes da Tarefa',{exact:false}).first().locator('xpath=parent::div'),{nova:false});
  await seguro(()=>p.locator('div.fixed button:has(svg.lucide-x)').first().click({timeout:2500})); await dorme(700);
  await seguro(()=>p.keyboard.press('Escape'));
});
await roteiro('visoes',async()=>{ novoTour('visoes');
  await menu('Tarefas');
  for(const rot of ['Kanban','Por responsável','Lista','Linha do tempo','Gantt','Calendário']){ await seguro(async()=>{ await clicar(p.locator('main button').filter({hasText:new RegExp('^\\s*'+rot+'\\s*$')})); await dorme(1000); await passo(p.locator('main button').filter({hasText:new RegExp('^\\s*'+rot+'\\s*$')}),{folga:10}); },rot); }
  await clicar(p.locator('main button').filter({hasText:/^\s*Kanban\s*$/})); await dorme(500);
});
await roteiro('horas',async()=>{ novoTour('horas');
  await menu('Timesheet');
  await passo(bt('Lançar horas'));
  await passo(p.locator('main table, main [class*=divide]').first(),{nova:false});
  await menu('Planner');
  await passo(btExato('Semana'));
});
await roteiro('solic',async()=>{ novoTour('solic');
  await menu('Solicitações');
  await passo(ph(/O que você precisa/));
  await passo(p.getByRole('button',{name:/Reembolso de despesas/}).first(),{nova:false});
  await clicar(p.getByRole('button',{name:/Reembolso de despesas/})); await dorme(700);
  await passo(modal(),{rolar:false});
  await seguro(()=>p.locator('div.fixed.inset-0').last().getByRole('button',{name:/Cancelar/}).first().click({timeout:2500}));
  await seguro(()=>p.locator('div.fixed.inset-0 button:has(svg.lucide-x)').last().click({timeout:1500})); await dorme(400);
  await passo(bt(/Para eu aprovar/));
});
await roteiro('mural',async()=>{ novoTour('mural');
  await menu('Mural & Recados');
  await passo(bt('Novo Post'));
  await clicar(bt('Novo Post')); await dorme(500);
  await passo(p.locator('div').filter({has:ph('Título do comunicado')}).last().locator('xpath=ancestor::div[2]'));
  await seguro(()=>clicar(bt(/Enquete/))); await dorme(350);
  await passo(ph('Opção 1').locator('xpath=ancestor::div[3]'));
  await limpar();
});
// ---------------------------------------------------------- áreas e gestão
await roteiro('areas',async()=>{ novoTour('areas');
  for(const [m,al] of [['Comercial',()=>p.locator('main button').filter({hasText:/CRM|Importar e exportar/}).first()],['Marketing',()=>bt('Nova campanha')],['RH',()=>bt('Nova pessoa').first()],['Impulsionamento',()=>bt('Cadastrar conta')],['Compras',()=>p.locator('main button').filter({hasText:/Demandas/}).first()],['Criação',()=>p.locator('main button').filter({hasText:/Painel/}).first()],['Social Mídia',()=>bt(/Novo post/i).first()],['Estoque',()=>bt('Novo item').first()]]){ await menu(m); await passo(al()); }
});
await roteiro('gestao',async()=>{ novoTour('gestao');
  await menu('Relatórios');
  await tirar(); CAIXAS[tour].push({f:foto,x:232,y:128,w:1296,h:440});
  await menu('Central de Relatórios');
  await passo(p.locator('main button').filter({hasText:/DA EMPRESA|Da empresa/i}).first());
  await menu('Tarefas');
  await clicar(p.locator('main button').filter({hasText:/Automações/})); await dorme(900);
  await passo(p.locator('main button').filter({hasText:/Nova automação|Nova regra|Criar automação/}).first());
  await clicar(p.locator('main button').filter({hasText:/Kanban/})); await dorme(400);
});
const arq=path.join(AQUI,'../assets/caixas.js');
let ant={}; if(so&&fs.existsSync(arq)){ try{ ant=JSON.parse(fs.readFileSync(arq,'utf-8').replace(/^window\.CAIXAS=/,'').replace(/;\s*$/,'')); }catch{} }
fs.writeFileSync(arq,'window.CAIXAS='+JSON.stringify({...ant,...CAIXAS})+';\n');
console.log(Object.entries(CAIXAS).map(([k,v])=>k+':'+v.length).join(' '));
console.log('erros',erros.length,erros.slice(0,3));
await b.close(); srv.close();
