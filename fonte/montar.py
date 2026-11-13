#!/usr/bin/env python3
"""Monta o index.html do tutorial do Ariuno. Rodar: python3 fonte/montar.py"""
import html, json, pathlib, time

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LINK = 'https://projetos.75lab.com.br/ariuno-tutorial/'
PDF = 'ariuno-tutorial-75lab.pdf'
VER = time.strftime('%Y%m%d%H%M%S')
e = html.escape

MAO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11V5a2 2 0 1 1 4 0v6m0-1a2 2 0 1 1 4 0v2m0-1a2 2 0 1 1 4 0v4a7 7 0 0 1-7 7h-2a7 7 0 0 1-6-3l-3-5a2 2 0 0 1 3-2l2 2"/></svg>'
OK = '<svg viewBox="0 0 24 24"><path d="M4 13l5 5L20 7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def cta(t): return f'<span class="cta so-tela">{MAO}{e(t)}</span>'

telas = []
def add(h): telas.append(h)
VJSON = RAIZ/'assets/videos/videos.json'
VID = json.loads(VJSON.read_text(encoding='utf-8')) if VJSON.exists() else []
VID = [v for v in VID if (RAIZ/'assets/videos'/(v['id']+'.mp4')).exists()]
for v in VID: v['telas'] = v['tela'] if isinstance(v.get('tela'), list) else [v.get('tela') or '']
def video_da_tela(tit):
    for v in VID:
        if any(t and (t == tit or tit.endswith(' · ' + t)) for t in v['telas']): return v['id']
    return ''
def attrs(cap, tit, tema='claro'):
    v = video_da_tela(tit)
    return f'data-cap="{e(cap)}" data-titulo="{e(tit)}" data-tema="{tema}"' + (f' data-video="{v}"' if v else '')
def quadro(): return '<div class="quadro" data-cursor="Ampliar"><div class="vista"><img alt="Tela do Ariuno"></div><div class="luz"></div><span class="ampliar so-tela">Ampliar</span></div>'
def cab(eb, h2, c): return f'<div class="cab"><div><div class="eb">{eb}</div><h2>{h2}</h2></div>{cta(c)}</div>'
def lista(p): return '<ol class="passos">' + ''.join(f'<li><button class="passo" data-p data-dd="{e(d)}" data-cursor=""><i>{i+1}</i><div><b data-t>{e(t)}</b><span data-d>{e(d)}</span></div></button></li>' for i,(t,d) in enumerate(p)) + '</ol>'

def tour(nome, cap, tit, eb, h2, layout, p, c='Clique em cada passo', extra=''):
    a = f'data-tour="{nome}" {extra} {attrs(cap, tit)}'
    if layout in ('dir', 'esq'):
        add(f'<section class="tela tour l-{layout}" {a}>{cab(eb,h2,c)}<div class="corpo">{quadro()}{lista(p)}</div></section>')
    elif layout == 'trilho':
        bolas = ''.join(f'<button data-p data-dd="{e(d)}" data-cursor=""><u style="text-decoration:none">{i+1}</u><b data-t hidden>{e(t)}</b><em data-d hidden>{e(d)}</em></button>' for i,(t,d) in enumerate(p))
        add(f'<section class="tela tour l-trilho" {a}><div class="lat"><div class="eb">{eb}</div><h2>{h2}</h2>{cta(c)}<div class="atual"><i>1</i><b></b><span></span></div></div><div class="dir">{quadro()}<div class="bolas">{bolas}</div></div></section>')
    elif layout == 'foco':
        nav = ''.join(f'<button data-p data-tt="{e(t)}" data-dd="{e(d)}" data-cursor="">{i+1}</button>' for i,(t,d) in enumerate(p))
        add(f'<section class="tela tour l-foco" {a}>{quadro()}<div class="cartao"><div class="eb">{eb}</div><h2>{h2}</h2><div class="num"></div><b class="tit"></b><span class="des"></span><nav>{nav}</nav>{cta(c)}</div></section>')

def abas(nome, cap, tit, eb, h2, itens, c, extra=''):
    bts = ''.join(f'<button data-p data-tt="{e(t)}" data-dd="{e(d)}" data-ini="{e(ini)}" data-cursor="">{e(r)}</button>' for r,t,d,ini in itens)
    add(f'<section class="tela tour l-abas" data-tour="{nome}" {extra} {attrs(cap,tit)}>{cab(eb,h2,c)}<div class="abas">{bts}</div><div class="linha">{quadro()}<div class="expl"><b></b><p></p><small></small></div></div></section>')

def capitulo(n, nome, dur, quem, itens):
    li = ''.join(f'<li>{OK}{e(i)}</li>' for i in itens)
    add(f'<section class="tela s-cap" {attrs(f"{n} · {nome}", nome, "iris")}><div><div class="n">{n}</div><h2>{e(nome)}</h2><span class="dur">{e(dur)}</span></div><div><small>{e(quem)}</small><ul>{li}</ul></div></section>')

# ================================================================= abertura
add(f'''<section class="tela s-capa" {attrs("", "Capa", "escuro")}>
<div class="fx"><img src="assets/telas/quadro-1.jpg" alt=""></div>
<div class="tx"><h1>Sua empresa rodando no <em>Ariuno</em> em uma hora.</h1>
<p>Passo a passo para configurar a conta e colocar o time para trabalhar.</p>
<div class="ac so-tela"><button class="botao lime" data-ir="2" data-cursor="Ir">Começar a reunião →</button><button class="botao claro" data-ir="3" data-cursor="Ir">Ver o índice</button><a class="botao claro" href="{PDF}" target="_blank" rel="noopener">Baixar em PDF</a></div></div>
<div class="lab"><span>Uma apresentação</span><img src="assets/75lab-wordmark-paper.png" alt="75 LAB"></div></section>''')

PAR = [(5,'Entender','Como o Ariuno se organiza'),(15,'Configurar','Sete passos do admin'),(20,'Dia a dia','A rotina de quem usa'),(6,'Áreas','Cada departamento'),(6,'Gestão','Relatórios e regras'),(5,'1ª semana','Plano e teste'),(3,'Perguntas','Com a sua realidade')]
blocos = ''.join(f'<div class="par" style="flex:{m+6} 1 0"><u>{m}<small>min</small></u><div><b>{e(n)}</b><p>{e(d)}</p></div></div>' for m,n,d in PAR)
add(f'''<section class="tela" {attrs("Agenda","Agenda da reunião")}><div class="eb">A reunião</div><h2>Sete paradas, sessenta minutos. <em>O relógio está no topo.</em></h2>
<div class="linha60">{blocos}</div>
<div class="quem"><div><b>Quem administra</b>Fica do começo ao fim e sai com a conta configurada.</div><div><b>O time</b>Pode entrar a partir do Dia a dia, aos 20 minutos.</div><div><b>Como acompanhar</b>Cada tela mostra o passo destacado no próprio Ariuno.</div></div></section>''')

# ================================================================= índice (o deck.js monta a lista a partir das telas)
add(f'''<section class="tela s-indice" {attrs("Índice","Índice")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb">Índice</div><h2>Vá direto <em>ao que você precisa</em>.</h2></div>{cta("Clique para ir à tela")}</div>
<div class="ind" id="indice" data-caps="1-6"></div><div class="ind-pe"><p class="ind-dica">O índice também abre a qualquer momento no botão <b>Índice</b>, no topo, ou com a tecla M.</p><button class="botao" data-ir-titulo="Manual avançado" data-cursor="Ir">Manual avançado, capítulos 7 a 14 →</button></div></section>''')

# ================================================================= 1 entender
C1='1 · Entender'
capitulo(1,'Entender','5 minutos','Ao final você sabe',['Como cliente, projeto e card se ligam','Quem pode fazer o quê'])
ELOS=[('Cliente','Para quem o trabalho é feito.','Kompra Supermercados','M3 21V7l9-4 9 4v14M9 21v-6h6v6'),('Projeto','O conjunto de trabalho de um cliente.','Catálogo de Produtos 2026','M3 7h7l2 3h9v10H3z'),('Quadro','O caminho que o trabalho percorre, em etapas.','Briefing, Criação, Aprovação, Entrega','M4 4h5v16H4zM10 4h5v10h-5zM16 4h4v13h-4z'),('Card','Uma entrega: briefing, responsáveis, prazo e conversa.','Encarte de dezembro','M4 5h16v14H4zM8 10h8M8 14h5'),('Horas','O tempo gasto, registrado no próprio card.','6h30 em Criação','M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 7v5l3 2'),('Relatório','A soma de tudo, sem planilha paralela.','Horas por cliente no mês','M4 20V10M10 20V4M16 20v-7M21 20H3')]
elos=''
for i,(n,o,x,ic) in enumerate(ELOS):
    if i: elos+='<span class="seta">→</span>'
    elos+=f'<button class="elo" data-o="{e(o)}" data-ex="{e(x)}" data-t="{e(o)}{e(x)}" data-cursor=""><svg viewBox="0 0 24 24"><path d="{ic}"/></svg>{e(n)}</button>'
add(f'''<section class="tela s-cadeia" data-abas=".elo" {attrs(C1,"Tudo gira em torno do card")}><div class="cab" style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb">Parada 1</div><h2>Tudo no Ariuno gira em torno do <em>card</em>.</h2></div>{cta("Clique em cada peça")}</div>
<div class="cadeia">{elos}</div>
<div class="expl-c"><h3 id="cTit"></h3><div><b>O que é</b><p id="cO"></p></div><div><b>Exemplo</b><p id="cEx"></p></div></div></section>''')
add(f'''<section class="tela" {attrs(C1,"Quem faz o quê")}><div class="eb">Parada 1</div><h2>Quatro papéis. <em>Cada um com o seu limite.</em></h2>
<div class="papeis">
<div class="pap d"><small>Plataforma</small><h3>75 LAB</h3><ul><li>Cria a empresa</li><li>Abre novos assentos</li><li>Envia os convites</li></ul></div>
<div class="pap i"><small>Sua empresa</small><h3>Admin</h3><ul><li>Configura regras, quadros e modelos</li><li>Edita permissões do time</li><li>Preenche vagas livres</li><li class="nao">Não aumenta o número de assentos</li></ul></div>
<div class="pap"><small>Sua empresa</small><h3>Pessoa do time</h3><ul><li>Trabalha nos seus cards</li><li>Registra horas e comenta</li><li>Faz pedidos em Solicitações</li><li class="nao">Só vê as áreas liberadas</li></ul></div>
<div class="pap"><small>Fora da empresa</small><h3>Cliente</h3><ul><li>Acompanha o que é dele</li><li>Responde por link</li><li class="nao">Não ocupa assento pago</li></ul></div>
</div></section>''')

# ================================================================= 2 configurar
C2='2 · Configurar'
capitulo(2,'Configurar','15 minutos','Só para quem administra',['Regras da empresa','Time e permissões','Clientes, quadros e modelos'])
SETE=[('Ajustes','Regras e marca','2 min'),('Time','Convidar pessoas','3 min'),('Permissões','Quem vê o quê','3 min'),('Clientes','E os projetos','2 min'),('Quadro','Etapas do fluxo','2 min'),('Modelos','O que se repete','2 min'),('Fechar','Feriados e contas','1 min')]
pts=''.join(f'<div class="pt"><div class="bola">{i+1}</div><h3>{e(a)}</h3><p>{e(b)}</p><u>{e(c)}</u></div>' for i,(a,b,c) in enumerate(SETE))
add(f'''<section class="tela" {attrs(C2,"Os 7 passos")}><div class="eb">Parada 2</div><h2>A empresa fica pronta em <em>sete passos</em>, nesta ordem.</h2>
<div class="sete">{pts}</div><div class="total">Faça na ordem: cada passo usa o que o anterior deixou pronto.</div></section>''')
tour('ajustes',C2,'Passo 1 · Ajustes da empresa','<b>Passo 1</b> 2 min','Comece pelas <em>regras da casa</em>.','dir',[
 ('Abra os Ajustes','No menu, em Administração, clique em Ajustes da empresa.'),
 ('Escolha o assunto','As regras ficam separadas: usuários, tarefas, comentários, tempo, mural.'),
 ('Ligue o que vale','Cada regra é uma chave. Mudou de ideia, é só desligar.'),
 ('Coloque a sua marca','Em Aparência e Marca entram logo, cores e fontes.'),
 ('Salve','Salvar e Aplicar vale para toda a empresa.')])
tour('time',C2,'Passo 2 · Convidar o time','<b>Passo 2</b> 3 min','Traga o time: <em>o link já entra liberado</em>.','esq',[
 ('Abra Gestão de Equipe','Em Administração. Assentos contratados e vagas livres ficam no topo.'),
 ('Assento novo é com a 75 LAB','Mande a lista de e-mails: a 75 LAB abre os assentos e envia os convites.'),
 ('O convite leva e-mail e nome','O link pessoal chega por e-mail e vale 14 dias.'),
 ('Já com a configuração certa','O convite pode copiar as permissões de um colega da mesma área.'),
 ('A pessoa entra liberada','Quem cria a senha pelo link entra direto. Vaga livre sem convite: o admin aprova em Pendentes.')])
tour('permissoes',C2,'Passo 3 · Permissões','<b>Passo 3</b> 3 min','Cada pessoa vê <em>só o que precisa</em>.','trilho',[
 ('Copie de um colega','Na edição do usuário, puxe a configuração de alguém da mesma empresa.'),
 ('Ajuste as chaves','Gestor, edição de custos e acesso a relatórios.'),
 ('Libere as áreas','Departamento principal e os módulos que a pessoa usa.'),
 ('Limite as colunas','Opcional: o que ela enxerga em cada quadro. Vazio mostra tudo.')],c='Clique nos números')
add(f'''<section class="tela s-perm" {attrs(C2,"Simulador de permissões")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Experimente</b> Passo 3</div><h2>Mude o acesso e veja o <em>menu da pessoa</em> mudar.</h2></div>{cta("Clique nas opções")}</div>
<div class="sim-p"><div><div class="areas"></div><div class="aviso" style="margin-top:12px"><i>Resultado</i><span id="permRes"></span></div></div><div class="menu-m"></div></div></section>''')
tour('clientes',C2,'Passo 4 · Clientes e projetos','<b>Passo 4</b> 2 min','Cliente primeiro, <em>projeto depois</em>.','foco',[
 ('Novo cliente','Em Clientes, no canto superior direito.'),
 ('Preencha o básico','O nome basta para começar. O resto entra depois.'),
 ('Novo Projeto','Em Projetos. Cada projeto pertence a um cliente.'),
 ('Ligue tudo','Escolha cliente, modelo, responsável e prazos.')],c='Clique nos números',extra='data-max="2"')
tour('quadro',C2,'Passo 5 · Quadro e etapas','<b>Passo 5</b> 2 min','O quadro é <em>o caminho</em> do seu trabalho.','esq',[
 ('Crie o quadro','Use o + ao lado do nome. Um por fluxo, não um por cliente.'),
 ('Dê um nome','Exemplos: Campanhas, Comercial, Interno.'),
 ('Edite as etapas','Clique no nome para trocar. Arraste a coluna para mudar a ordem.'),
 ('Configure a etapa','No ícone da coluna: cor, ordenação e quais são Concluído e Perdidos.')])
add(f'''<section class="tela s-etapas" data-abas=".segs button" {attrs(C2,"Sugestão de etapas")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Experimente</b> Passo 5</div><h2>Não sabe quais etapas usar? <em>Comece por uma destas.</em></h2></div>{cta("Clique no seu tipo de empresa")}</div>
<div class="segs"><button data-s="ag" data-cursor="">Agência e criação</button><button data-s="ind" data-cursor="">Indústria e times internos</button><button data-s="serv" data-cursor="">Serviços e consultoria</button></div>
<div class="col-m"></div>
<div class="dicas"><p><b>Poucas etapas.</b> De 4 a 7 resolvem quase tudo.</p><p><b>Uma pergunta por etapa.</b> Com quem está o card agora?</p><p><b>Sempre com fim.</b> Marque qual coluna é Concluído.</p></div></section>''')
tour('modelos',C2,'Passo 6 · Tipos e modelos','<b>Passo 6</b> 2 min','O que se repete <em>vira modelo</em>.','dir',[
 ('Tipos de tarefa','Cadastre o que a empresa entrega, com a cor de cada um.'),
 ('Novo modelo','Em Modelos de Projeto, desça até Modelos de tarefa.'),
 ('Monte o roteiro','Nome, grupo, título, quadro, etapa e briefing.'),
 ('Liste as subtarefas','Cada passo com a sua etapa e o seu prazo.'),
 ('Pronto para usar','Clique no modelo para editar quando precisar.')],extra='data-max="1.9"')
tour('fecho',C2,'Passo 7 · Feriados e integrações','<b>Passo 7</b> 1 min','Feche com <em>calendário e contas</em>.','foco',[
 ('Cadastre os feriados','Assim eles não contam como dias úteis nos prazos.'),
 ('Conecte as contas','Google Analytics, Meta e YouTube: o admin conecta e os números entram sozinhos.')],c='Clique nos números',extra='data-max="1.8"')
ck=''.join(f'<button data-cursor=""><i></i>{e(t)}</button>' for t in ['Regras e marca salvas em Ajustes','Pessoas convidadas','Permissões conferidas','Clientes e projetos criados','Quadro com etapas e coluna de Concluído','Tipos e primeiros modelos prontos','Feriados e contas conectadas','Um card de teste feito de ponta a ponta'])
add(f'''<section class="tela s-chk" {attrs(C2,"Checagem da configuração")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Confira</b> Antes de chamar o time</div><h2>Marque o que já está <em>feito na sua conta</em>.</h2></div>{cta("Clique em cada item")}</div>
<div class="chk">{ck}</div><div class="barra"><i></i><span></span></div></section>''')

# ================================================================= 3 dia a dia
C3='3 · Dia a dia'
capitulo(3,'Dia a dia','20 minutos','Para o time inteiro',['A rotina em cinco movimentos','Tarefa, subtarefa e checklist','Criar, abrir e tocar um card','Horas, pedidos e recados'])
MOV=[('Abra','Sua pauta mostra o que é seu.','M4 5h16v14H4zM4 10h16M9 5V3M15 5V3'),('Dê o Play','O tempo entra no card.','M8 5l12 7-12 7z'),('Registre','Comente, marque e anexe no card.','M4 5h16v11H9l-5 4z'),('Mova','A próxima etapa já vê.','M4 12h15M13 6l6 6-6 6'),('Conclua','Entra nos relatórios.','M4 13l5 5L20 7')]
mv=''.join(f'<div class="mov"><div class="ic"><svg viewBox="0 0 24 24"><path d="{p}"/></svg></div><small>{i+1}</small><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i,(a,b,p) in enumerate(MOV))
add(f'''<section class="tela" {attrs(C3,"A rotina em 5 movimentos")}><div class="eb">Parada 3</div><h2>O dia de trabalho cabe em <em>cinco movimentos</em>.</h2><div class="rot">{mv}</div><div class="total" style="margin-top:50px">Regra de ouro: se aconteceu no job, está dentro do card.</div></section>''')
tour('pauta',C3,'Minha pauta','<b>1</b> Abra','Comece o dia pela <em>sua pauta</em>.','dir',[
 ('Abra Meu Portal','Minha pauta reúne o que é seu, de qualquer quadro.'),
 ('Veja o que vence','Cada linha é um card. Clique para abrir.')],extra='data-max="1.6"')
tour('criar',C3,'Criar uma tarefa','Criar tarefa','Criar um card leva <em>menos de um minuto</em>.','esq',[
 ('Nova Tarefa','Botão no canto superior direito do quadro.'),
 ('Escolha um modelo','Um clique traz briefing e subtarefas.'),
 ('Dê o título','Troque os colchetes pelo caso real.'),
 ('Quem faz','Responsável, etapa e prioridade.'),
 ('Criar tarefa','Em Mais detalhes dá para abrir o card completo.')],extra='data-max="2"')
abas('card',C3,'Dentro do card','Dentro do card','Tudo sobre o job <em>mora no card</em>.',[
 ('Descrição','Briefing','O pedido completo, com texto formatado.','Comece sempre por aqui'),
 ('Checklist','Passos e responsáveis','Cada item com quantidade, responsável, fornecedor e data.','Um dono por item'),
 ('Subtarefas','Divida o trabalho','Cada parte com seu dono, prazo e etapa.','Uma subtarefa, uma pessoa'),
 ('Comentários','A conversa do job','Use @ para chamar alguém. O histórico fica no card.','Nada de decisão no WhatsApp'),
 ('Anexos','Arquivos em um lugar','Tudo o que foi enviado e produzido para o job.','Procure aqui primeiro'),
 ('Cronograma','Etapas e datas','Monte o cronograma do job, linha a linha.','Para jobs longos'),
 ('Painel','Painel de Controle','AF, orçamento aprovado, faturamento e entrega.','Para quem cuida do financeiro do job'),
 ('Tempo','Registros de Tempo','Cada apontamento: de quem, quando e quanto.','Lançou errado? Corrija aqui')],'Clique em cada aba','data-regiao="60,50,1160,725" data-semluz')
# ---- tarefa principal, subtarefa e checklist: um job de verdade, desmontado
NIV=[('principal','Tarefa principal','O job inteiro: o que o cliente vai receber.','Tem cliente, projeto, briefing e o prazo final. O card mostra quantas subtarefas já foram feitas.','O que o cliente vai receber?'),
     ('sub','Subtarefa','Uma parte do job com dono, prazo e etapa próprios.','Anda pelo quadro na sua etapa e pode ir para o Planner de quem faz. Use quando muda a pessoa ou a etapa.','Precisa de outra pessoa ou de outra etapa?'),
     ('chk','Checklist','Itens curtos para não esquecer, dentro de um card.','Não anda pelo quadro: o card mostra o progresso, como 1/3. Cada item pode ter responsável, fornecedor e data.','É um lembrete rápido dentro de um trabalho?')]
niv=''.join(f'<button class="niv" data-n="{k}" data-nome="{e(t)}" data-o="{e(o)}" data-onde="{e(w)}" data-q="{e(q)}" data-t="{e(o)} {e(w)}" data-cursor="">{e(t)}</button>' for k,t,o,w,q in NIV)
SUBS=[('Redação dos textos','Ana','Criação','até 12/12',False),('Diagramação','Bruno','Criação','até 16/12',True),('Aprovação com o cliente','Camila','Aprovação','até 18/12',False)]
CHK=[('Conferir os preços com a tabela','Bruno',True),('Logo na versão nova','Bruno',False),('Exportar o PDF em alta','Diego',False)]
def subtarefa(t,p,et,pr,abre):
    ch=''
    if abre:
        ch='<div class="chkl" data-n="chk"><div class="chk-rot">Checklist da Diagramação <u>1/3</u></div>'+''.join(f'<div class="itm{" ok" if f else ""}"><i>{"✓" if f else ""}</i><span>{e(x)}</span><em>{e(q)}</em></div>' for x,q,f in CHK)+'</div>'
    return f'<div class="ramo"><div class="sb" data-n="sub"><span class="tag">Subtarefa</span><b>{e(t)}</b><small>{e(p)} · {e(et)} · {e(pr)}</small></div>{ch}</div>'
arv=''.join(subtarefa(*x) for x in SUBS)
add(f"""<section class="tela s-hier" data-abas=".niv" {attrs(C3,"Tarefa, subtarefa e checklist")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Exemplo</b> Um job desmontado</div><h2>Um job, <em>três níveis</em>: tarefa, subtarefa e checklist.</h2></div>{cta("Clique em cada nível")}</div>
<div class="hier"><div class="arv"><div class="mae" data-n="principal"><span class="tag">Tarefa principal</span><b>Encarte de dezembro</b><small>Kompra Supermercados · Catálogo 2026 · entrega 20/12 · subtarefas 1 de 3</small></div><div class="filhos">{arv}</div></div>
<div class="pn"><div class="niveis">{niv}</div><h3 id="hNome"></h3><p id="hO"></p><div class="lin"><b>Na prática</b><span id="hOnde"></span></div><div class="pergunta"><b>Pergunta para decidir</b><span id="hQ"></span></div></div></div>
<div class="regra">Regra prática: <b>tem dono e prazo, é subtarefa.</b> <b>É para não esquecer, é checklist.</b></div></section>""")
ONDE=[{"t":"Campanha de Natal da Kompra","c":0,"p":"É o job inteiro, com cliente e prazo final."},
      {"t":"Fotografar os produtos do encarte","c":1,"p":"Outra pessoa, outro prazo: subtarefa."},
      {"t":"Conferir se o logo é o da versão nova","c":2,"p":"Lembrete rápido dentro da diagramação: checklist."},
      {"t":"Aprovação do cliente","c":1,"p":"Depende do cliente e tem etapa própria: subtarefa."},
      {"t":"Revisar a ortografia antes de enviar","c":2,"p":"Item curto para não esquecer: checklist."}]
add(f"""<section class="tela s-onde" {attrs(C3,"Onde isso entra?")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Agora você</b> Cinco casos</div><h2>Onde isso entra: <em>tarefa, subtarefa ou checklist?</em></h2></div>{cta("Clique na resposta")}</div>
<script type="application/json" id="ondeDados">{json.dumps(ONDE,ensure_ascii=False)}</script>
<div class="onde"><div class="caso"><small id="oN"></small><b id="oT"></b></div><div class="tres"><button data-c="0" data-cursor=""><u>1</u>Tarefa principal</button><button data-c="1" data-cursor=""><u>2</u>Subtarefa</button><button data-c="2" data-cursor=""><u>3</u>Checklist</button></div><p class="porque" id="oP"></p><div class="fila" id="oFila"></div></div>
<div class="regra">Regra prática: <b>é o job inteiro, é tarefa principal.</b> <b>Tem dono e prazo, é subtarefa.</b> <b>É para não esquecer, é checklist.</b></div></section>""")
# ---- cards em massa por planilha
tour('importar',C3,'Cards em massa por planilha','<b>Atalho</b> Criar em massa','Muitos cards de uma vez: <em>suba uma planilha</em>.','dir',[
 ('Abra a importação','No quadro, clique no ícone de planilha ao lado do nome.'),
 ('Baixe o modelo','Vem com as etapas, pessoas, clientes e projetos deste quadro.'),
 ('Suba a planilha','Uma linha por card, em Excel ou CSV. Nada é criado ainda.'),
 ('Confira a prévia','Os avisos em amarelo mostram o que não bateu com o quadro.'),
 ('Crie os cards','O botão mostra o total, e todos entram de uma vez.'),
 ('Desfaça se precisar','Desfazer apaga só os cards desta planilha. O resto do quadro fica igual.')],extra='data-novo data-max="2.2"')
PL_COLS=['','Título','Card principal','Etapa','Responsável','Data de entrega','Checklist']
PL=[(2,['Campanha de Natal','','Planejamento','Camila Ferraz','28/11/2026',''],'Vira card principal','Card principal vazio: a linha é uma tarefa principal. Entra em Planejamento, com a Camila, para 28/11.'),
    (3,['Roteiro do vídeo','Campanha de Natal','Criação','Lucas Prado','21/11/2026','Gancho; Legenda; Trilha'],'Vira subtarefa','Card principal preenchido: entra como subtarefa da Campanha de Natal. O checklist chega com três itens, separados por ponto e vírgula.'),
    (4,['Peças para redes sociais','Campanha de Natal','Criação','Lucas Prado','24/11/2026',''],'Segunda subtarefa','A ordem das linhas é a ordem das subtarefas dentro da Campanha de Natal.'),
    (5,['Aprovação com o cliente','Campanha de Natal','Briefng','Camila Ferraz','26/11/2026',''],'Etapa digitada errado','"Briefng" não existe no quadro. A prévia avisa e o card vai para a primeira etapa. Copie os nomes da aba Listas.'),
    (6,['Relatório mensal','','','','30/11/2026',''],'Só o título já basta','Sem etapa, o card entra na primeira. Sem responsável, fica sem dono até alguém assumir.')]
def cel(j,v): return f'<span class="{"v" if j==1 and v else ("x" if v=="Briefng" else "")}">{e(v)}</span>'
pl_cab='<div class="pl-c">'+''.join(f'<span>{e(c)}</span>' for c in PL_COLS)+'</div>'
pl_lin=''.join(f'<button class="pl-l" data-n="{n}" data-tt="{e(tt)}" data-dd="{e(dd)}" data-t="{e(dd)}" data-cursor=""><span>{n}</span>'+''.join(cel(j,v) for j,v in enumerate(cs))+'</button>' for n,cs,tt,dd in PL)
def mc(r,tit,tag,info): return f'<div class="mc" data-r="{r}">'+(f'<em>{e(tag)}</em>' if tag else '')+f'<b>{e(tit)}</b><small>{e(info)}</small></div>'
MQ=[('Briefing',[mc(3,'Aprovação com o cliente','↳ Campanha de Natal','Camila · 26/11'),mc(4,'Relatório mensal','','Sem responsável · 30/11')]),
    ('Planejamento',[mc(0,'Campanha de Natal','Card principal','Camila · 28/11 · subtarefas 0 de 3')]),
    ('Criação',[mc(1,'Roteiro do vídeo','↳ Campanha de Natal','Lucas · 21/11 · checklist 0/3'),mc(2,'Peças para redes sociais','↳ Campanha de Natal','Lucas · 24/11')])]
mq=''.join(f'<div class="c{i+1}"><h4>{e(t)}</h4>{"".join(cs)}</div>' for i,(t,cs) in enumerate(MQ))
add(f"""<section class="tela s-plan" data-novo data-abas=".pl-l" {attrs(C3,"Como preencher a planilha")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Exemplo</b> A planilha</div><h2>Cada linha vira um card. <em>Veja onde ela entra.</em></h2></div>{cta("Clique em cada linha")}</div>
<div class="pl">{pl_cab}{pl_lin}</div>
<div class="baixo"><div class="mq">{mq}</div><div class="pl-ex"><small id="plN"></small><b id="plT"></b><p id="plP"></p></div></div>
<div class="regra">Só o <b>Título</b> é obrigatório. Nomes iguais aos da <b>aba Listas</b>. Datas em <b>dd/mm/aaaa</b>. Itens de checklist separados por <b>ponto e vírgula</b>.</div></section>""")
tour('trabalhar',C3,'Play e Concluir','<b>2</b> Dê o Play','Play quando começa. <em>Concluir quando termina.</em>','trilho',[
 ('Play','Começou a trabalhar? Clique. O tempo vai para o card.'),
 ('Concluir','Terminou? O card sai da sua pauta e entra nos relatórios.'),
 ('Detalhes','À direita: responsáveis, etapa, prioridade, cliente e projeto.')],c='Clique nos números',extra='data-max="2.2"')
add(f'''<section class="tela s-mk" {attrs(C3,"Experimente: arraste o card")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Experimente</b> Dê o Play e mova</div><h2>Faça o caminho do card <em>com o mouse</em>.</h2></div>{cta("Clique em Trabalhar e arraste")}</div>
<div class="mk"><div class="col"><h4>Briefing</h4><div class="mcard" data-cursor="Arraste"><b>Encarte de dezembro</b><p>Kompra Supermercados</p><div class="ln"><button class="play" data-cursor=""><span>▶</span><span>Trabalhar</span></button><time>00:00:00</time></div></div></div><div class="col"><h4>Criação</h4></div><div class="col"><h4>Aprovação</h4></div><div class="col"><h4>Concluído</h4></div></div>
<div class="aviso" id="mkAviso"><i>Passo 1</i><span></span></div></section>''')
abas('visoes',C3,'Seis formas de ver','Visões do quadro','O mesmo trabalho, <em>seis formas de ver</em>.',[
 ('Kanban','Por etapa','Para tocar o dia a dia.','Arraste entre as colunas'),
 ('Por responsável','Por pessoa','Quem está com o quê, e quem está cheio.','Bom para distribuir o trabalho'),
 ('Lista','Em tabela','Para filtrar, ordenar e exportar.','Tem exportação'),
 ('Linha do tempo','Por período','As entregas no mês, por pessoa.','Veja os choques de agenda'),
 ('Gantt','Por duração','Início e fim de cada card.','Para projetos longos'),
 ('Calendário','Por data','O que vence em cada dia.','Reunião de pauta')],'Clique em cada visão','data-regiao="226,0,1374,860" data-semluz')
tour('horas',C3,'Horas e Planner','Tempo','Hora que não foi registrada <em>não existe</em>.','esq',[
 ('Esqueceu o Play?','Em Timesheet, use Lançar horas.'),
 ('Confira os apontamentos','Filtre por pessoa, cliente, projeto e período.'),
 ('Planeje a semana','No Planner, arraste as subtarefas para a agenda.')],extra='data-max="1.8"')
tour('solic',C3,'Solicitações','Pedidos','Pediu? <em>Virou Solicitação.</em>','foco',[
 ('Busque o pedido','Digite o que precisa: reembolso, folga, compra.'),
 ('Escolha o tipo','São 15 tipos, e cada um diz para que serve.'),
 ('Preencha e anexe','Valor, data, nota e comprovantes. Depois envie.'),
 ('Aprove ou recuse','Em Para eu aprovar. Recusar pede motivo, e pagamento pede nota ou comprovante.')],c='Clique nos números',extra='data-max="1.9"')
tour('mural',C3,'Mural e enquetes','Recados','O recado de todos <em>fica no Mural</em>.','dir',[
 ('Novo Post','Em Mural & Recados.'),
 ('Escreva o comunicado','Título, texto e, se quiser, imagem.'),
 ('Pergunte ao time','Em Enquete, monte as opções e cada pessoa vota.')],extra='data-max="2"')

# ================================================================= 4 áreas
C4='4 · Áreas'
capitulo(4,'Áreas','6 minutos','Só aparece o que o admin liberou',['Para que serve cada área','Qual é o primeiro clique em cada uma'])
abas('areas',C4,'Áreas da empresa','Departamentos','Cada área começa em <em>um primeiro clique</em>.',[
 ('Comercial','Propostas e funil','Orçamentos, registros, fornecedores e CRM.','Primeiro clique: Importar e exportar'),
 ('Marketing','Campanhas e verba','Calendário, pedidos, leads e resultados.','Primeiro clique: Nova campanha'),
 ('RH','Pessoas e férias','Organograma, ausências, desempenho e clima.','Primeiro clique: Nova pessoa'),
 ('Impulsionamento','Redes e anúncios','Desempenho das contas, em um painel.','Primeiro clique: Cadastrar conta'),
 ('Compras','Demandas e cotações','Fornecedores e pedidos em um só fluxo.','Primeiro clique: Demandas'),
 ('Criação','Entregas e aprovações','A fila de quem produz, com o que está atrasado.','Primeiro clique: Entregas'),
 ('Social Mídia','Calendário de posts','Planeje, aprove e acompanhe o conteúdo.','Primeiro clique: Novo post'),
 ('Estoque','Materiais por cliente','Saldo, reservas e movimentações.','Primeiro clique: Novo item')],'Clique em cada área','data-max="1.3"')

# ================================================================= 5 gestão
C5='5 · Gestão'
capitulo(5,'Gestão','6 minutos','Para quem lidera',['O que olhar toda semana','Regras que trabalham sozinhas'])
tour('gestao',C5,'Relatórios e automações','<b>Toda semana</b>','Três lugares para <em>liderar sem perguntar</em>.','trilho',[
 ('Relatórios','A foto do dia: quem está trabalhando e o que vence.'),
 ('Central de Relatórios','Horas e entregas por empresa, usuário e cliente.'),
 ('Automações','Na aba Automações do quadro, em Nova automação.')],c='Clique nos números',extra='data-max="1.5"')
def bloco(k,tit,sub,ops): return f'<div class="bl" data-k="{k}"><small>{e(sub)}</small><h3>{e(tit)}</h3>'+''.join(f'<button data-v="{e(o)}" data-cursor="">{e(o)}</button>' for o in ops)+'</div>'
add(f'''<section class="tela s-auto" {attrs(C5,"Monte uma automação")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Experimente</b> Automações</div><h2>Toda regra tem <em>três partes</em>. Monte uma.</h2></div>{cta("Escolha uma opção em cada bloco")}</div>
<div class="auto">{bloco("q","Quando","O gatilho",["um card entrar em uma etapa","um card for criado","o checklist for concluído","um card ficar parado"])}{bloco("c","Só se","Filtro opcional",["for deste quadro","for deste tipo de tarefa","for qualquer card"])}{bloco("a","Então","A ação",["criar as subtarefas de um modelo","notificar o responsável","mover para outra etapa","comentar no card"])}</div>
<div class="frase" id="autoFrase"></div></section>''')

# ================================================================= 6 semana
C6='6 · Primeira semana'
capitulo(6,'Primeira semana','5 minutos e perguntas','Para sair daqui com data marcada',['O plano de cinco dias','Um teste rápido'])
DIAS=[('Segunda','Admin',['Ajustes da empresa','Convites enviados','Permissões conferidas'],'Quem: admin'),('Terça','Base',['Clientes e projetos','Quadro e etapas','Tipos de tarefa'],'Quem: admin'),('Quarta','Modelos',['Três modelos principais','Um card de teste de ponta a ponta'],'Quem: admin e líderes'),('Quinta','Time',['Todo mundo com cards','Play ligado','Parar de usar a planilha'],'Quem: time inteiro'),('Sexta','Leitura',['Abrir os Relatórios','Ver quem não registrou','Ajustar o que travou'],'Quem: líderes')]
ds=''.join(f'<div class="dia"><header><small>{e(a)}</small><b>{e(b)}</b></header><ul>'+''.join(f'<li>{e(x)}</li>' for x in c)+f'</ul><div class="quem2">{e(d)}</div></div>' for a,b,c,d in DIAS)
add(f'''<section class="tela" {attrs(C6,"Plano da primeira semana")}><div class="eb">Parada 6</div><h2>Em <em>cinco dias</em> o time inteiro está dentro.</h2><div class="sem">{ds}</div></section>''')
QUIZ=[
 {"q":"Precisa de mais uma pessoa e não há vaga livre. O que fazer?","a":["Pedir à 75 LAB um novo assento","Criar a pessoa no cadastro de Clientes","Compartilhar o login de um colega"],"c":0,"p":"Assento novo é com a 75 LAB. Vaga livre, o admin preenche."},
 {"q":"Onde o time deve combinar os detalhes de um job?","a":["No grupo do WhatsApp","Nos Comentários do card","Em uma planilha à parte"],"c":1,"p":"No card fica o histórico, e o @ chama quem precisa ver."},
 {"q":"O mesmo tipo de job se repete todo mês. O melhor caminho é:","a":["Copiar e colar o texto","Criar do zero, para não errar","Criar um modelo de tarefa"],"c":2,"p":"O modelo traz briefing e subtarefas em um clique."},
 {"q":"Você pagou um almoço com cliente. Como pede o reembolso?","a":["Em Solicitações, Reembolso de despesas","Por e-mail para o financeiro","Em um comentário no card"],"c":0,"p":"Solicitações registra, encaminha e guarda os comprovantes."}]
add(f'''<section class="tela s-quiz" {attrs(C6,"Teste rápido")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Teste rápido</b> Todo mundo responde</div><h2>Quatro perguntas para <em>fixar o essencial</em>.</h2></div>{cta("Clique na resposta")}</div>
<script type="application/json" id="quizDados">{json.dumps(QUIZ,ensure_ascii=False)}</script>
<div class="qz"><div class="pl"><span id="qN"></span><small>pergunta</small></div><div><h3 id="qT"></h3><div class="ops"></div><div class="porque" id="qP"></div><button class="botao prox so-tela" id="qProx" data-cursor="" style="display:none"><span>Próxima pergunta →</span></button></div></div></section>''')
# ================================================================= manual avançado (fonte/avancado.py)
exec((RAIZ/'fonte/avancado.py').read_text(encoding='utf-8'))

add(f'''<section class="tela s-fim" {attrs("Encerramento","Próximos passos e contato","lime")}>
<div class="e"><h2>Agora é com o seu time.</h2><p>Comece hoje pelo passo 1. Na sexta, o Ariuno já responde quem fez o quê, quando e por quanto tempo.</p>
<div class="so-tela" style="display:flex;gap:12px"><a class="botao" href="https://wa.me/5511986765634" target="_blank" rel="noopener">Fale conosco no WhatsApp →</a><a class="botao claro" href="https://ariuno.com.br" target="_blank" rel="noopener">Abrir o Ariuno</a></div></div>
<div class="d"><img src="assets/75lab-wordmark-lime.png" alt="75 LAB"><h4>Quem te acompanha</h4><p>75 LAB ESTRATÉGIA, DESIGN E PRODUÇÃO LTDA<br>CNPJ 55.470.982/0001-77</p><h4>Onde estamos</h4><p>CENU, Torre Norte, Av. das Nações Unidas, 12.901<br>Brooklin, São Paulo, SP, CEP 04578-910</p><h4>Contato</h4><p>(11) 98676-5634 · contato@75lab.com.br<br>75lab.com.br</p></div></section>''')

LOGO = '<svg viewBox="0 0 100 100" fill="none"><defs><linearGradient id="gl" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6A5CFF"/><stop offset="50%" stop-color="#4285FF"/><stop offset="100%" stop-color="#00C2A8"/></linearGradient></defs><path d="M 80 70 L 35 55 C 5 45, 20 90, 35 55 L 50 20 L 80 70 Z" stroke="url(#gl)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'
pagina = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ariuno · Tutorial para novas empresas</title>
<meta name="description" content="Passo a passo para configurar o Ariuno e colocar o time para trabalhar, em uma reunião de até uma hora.">
<meta name="robots" content="noindex">
<meta name="versao" id="versaoDeck" content="{VER}">
<script>
(function(){{var v=document.getElementById('versaoDeck').content;
fetch('versao.txt?t='+Date.now(),{{cache:'no-store'}}).then(function(r){{return r.ok?r.text():''}}).then(function(n){{n=(n||'').trim();
if(n&&n!==v&&new URLSearchParams(location.search).get('v')!==n){{var q=new URLSearchParams(location.search);q.set('v',n);location.replace(location.pathname+'?'+q.toString()+location.hash);}}}}).catch(function(){{}});}})();
</script>
<link rel="icon" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Sora:wght@700;800&family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/deck.css?v={VER}">
</head>
<body>
<div id="wrap"><div id="stage">
{chr(10).join(telas)}
<header id="topo"><div style="display:flex;align-items:center"><div id="marca">{LOGO}ariuno</div><span id="capTxt"></span></div>
<div id="topoDir"><button class="chip vid" id="btVideo" data-cursor="Assistir" hidden>▶ Vídeo desta tela</button><button class="chip" id="relogio" data-cursor="Pausar">00:00 de 60:00</button><button class="chip" data-sumario data-cursor="Abrir">Índice</button><a class="chip" href="{PDF}" target="_blank" rel="noopener">PDF</a></div></header>
<div id="pe"><span id="cont"></span><div><button id="ant" aria-label="Voltar" data-cursor="">‹</button><button id="prox" aria-label="Avançar" data-cursor="">›</button></div></div>
<div id="prog"><i></i></div>
<div id="wipe">{LOGO}</div>
<nav id="sumario" aria-label="Índice"><button class="botao claro fechar" data-cursor="">Fechar ✕</button><h2>Índice</h2><ol id="sumLista"></ol></nav>
</div></div>
<div id="player" role="dialog" aria-label="Vídeo"><div class="pl-box"><div class="pl-top"><b id="plTit"></b><button class="botao claro fechar" data-cursor="">Fechar ✕</button></div><video id="plVideo" controls playsinline preload="none"></video><p id="plSub"></p></div></div>
<div id="caixa" role="dialog" aria-label="Imagem ampliada"><button class="botao claro fechar" data-cursor="">Fechar ✕</button><img id="cxImg" alt=""></div>
<div id="cursor"></div><div id="anel"><span id="anelTxt"></span></div>
<script>window.VIDEOS={json.dumps({v['id']: {'titulo': v['titulo'], 'sub': v['sub']} for v in VID}, ensure_ascii=False)};</script>
<script src="assets/caixas.js?v={VER}"></script>
<script src="assets/deck.js?v={VER}"></script>
</body></html>
'''
(RAIZ/'index.html').write_text(pagina, encoding='utf-8')
(RAIZ/'versao.txt').write_text(VER+'\n', encoding='utf-8')
exec((RAIZ/'fonte/pagina_videos.py').read_text(encoding='utf-8'))
print('telas', len(telas), 'versão', VER, 'vídeos', len(VID))
