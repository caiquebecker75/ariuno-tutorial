# Capítulos 7 a 13 do manual avançado. Roda dentro do avancado.py (montar.py).
# Textos conferidos no código do Ariuno em 13/11/2026: só entra o que funciona para a empresa cliente.
REG = 'data-regiao="232,0,1368,855"'
def tourA(*a, **k):
    k.setdefault('extra', 'data-max="1.6"')
    tour(*a, **k)

# ================================================================= 7 empresa
C7 = '7 · Empresa a fundo'
capitulo(7, 'Empresa a fundo', 'Consulta', 'Para quem administra', ['Cada regra dos Ajustes', 'Marca, feriados, tipos e formulários', 'Integrações com as redes'])
abas('ajustes2', C7, 'As regras da empresa', '<b>Ajustes</b> Administração', 'Cada assunto dos Ajustes, <em>o que muda de verdade</em>.', [
 ('Usuários', 'Usuários', 'A chave que vale: esconder de quem não é gestor os números individuais dos colegas, como horas, ranking e atrasos.', 'Ligada, só admin e gestor veem por pessoa'),
 ('Tarefas', 'Tarefas', 'Toda tarefa criada na mão entra na primeira coluna do quadro, ou na coluna de entrada que você escrever.', 'Exemplo: escreva Briefing'),
 ('Comentários', 'Comentários e anexos', 'Bloqueie anexos para todos, ou dê um prazo para editar e apagar comentários.', 'Depois do prazo, só o admin edita'),
 ('Cliente > Projeto', 'Cliente e projeto', 'Liga a ligação entre cliente e projeto e, se quiser, os grupos de projetos.', 'Grupo aparece no cadastro do projeto'),
 ('Mural', 'Mural', 'Liga ou desliga o Mural & Recados para a empresa inteira.', 'Desligado, some do menu'),
 ('Tempo', 'Gestão de tempo', 'Escolha como o tempo conta e se o Ariuno lembra de registrar horas na entrega.', 'Padrão: contabilização normal'),
 ('Aparência', 'Aparência e Marca', 'Logo, cor, fonte, fundo, tema escuro e menu com a cara da empresa.', 'Tem botão para voltar ao padrão'),
 ('Etiquetas', 'Etiquetas globais', 'Etiquetas com cor que valem em todos os quadros.', 'Ex.: Urgente, Reunião, Aprovação')],
 'Clique em cada assunto', REG + ' data-semluz')
tourA('aparencia', C7, 'Aparência e marca', '<b>Marca</b> Ajustes', 'O Ariuno com <em>a cara da sua empresa</em>.', 'foco', [
 ('Comece por um modelo', 'São doze aparências prontas, do claro ao escuro.'),
 ('Nome e logo', 'O nome da plataforma e a sua logo, por link ou enviando o arquivo.'),
 ('Cor e fonte', 'A cor da marca e a fonte do Google Fonts.'),
 ('Fundo', 'Liso, sólido, gradiente ou imagem.'),
 ('Tema escuro', 'Personalize as cores do modo escuro, com o contraste medido.'),
 ('Salvar e Aplicar', 'Vale na hora para todo o time. Não gostou? Restaurar padrão de fábrica.')], c='Clique nos números')
tourA('cadastros', C7, 'Feriados, tipos e backups', '<b>Cadastros</b> Administração', 'O que o admin cadastra <em>uma vez só</em>.', 'trilho', [
 ('Novo feriado', 'Em Feriados. Assim o dia não conta como útil nos prazos.'),
 ('Se repete todo ano', 'Nome, data e a marcação de anual. Natal se cadastra uma vez.'),
 ('Novo Tipo de tarefa', 'Nome, cor e a estimativa padrão em minutos.'),
 ('Ative ou desative', 'Clique no Ativo para esconder um tipo sem apagar o histórico. Os backups saem sozinhos todo dia às 20h.')], c='Clique nos números')
tourA('formularios', C7, 'Formulários', '<b>Formulários</b> Principal', 'O cliente pede, <em>o card nasce sozinho</em>.', 'dir', [
 ('Novo Formulário', 'Em Formulários, no menu principal.'),
 ('Quadro de destino', 'Escolha o quadro e a coluna onde as respostas viram card.'),
 ('Perguntas e respostas', 'Texto, múltipla escolha, data ou anexo. Compartilhe o link público: cada resposta vira card com Criar Tarefa.')])
tourA('integracoes', C7, 'Integrações', '<b>Integrações</b> Administração', 'Os números das redes <em>entram sozinhos</em>.', 'esq', [
 ('Escolha a conta', 'Google Analytics 4, Meta, YouTube e Postiz.'),
 ('Conectar', 'O admin conecta uma vez e testa na hora.'),
 ('Passo a passo', 'Cada integração explica onde pegar a credencial.'),
 ('O que vem depois', 'TikTok, LinkedIn, X e Pinterest aguardam aprovação das plataformas. A leitura roda todo dia às 3h30.')])

# ================================================================= 8 usuários
C8 = '8 · Usuários e permissões'
capitulo(8, 'Usuários e permissões', 'Consulta', 'Para quem administra', ['Aprovar, bloquear e excluir', 'Cada campo do usuário', 'Quem pode o quê'])
tourA('equipe2', C8, 'Gestão de Equipe', '<b>Equipe</b> Administração', 'O time inteiro, <em>com os assentos à vista</em>.', 'trilho', [
 ('Usuários e Equipes', 'Duas abas: as pessoas e os times com líder.'),
 ('Assentos', 'Quantos a empresa contratou e quantos estão livres.'),
 ('Busca e filtros', 'Por nome, e-mail, tipo e status. Pendentes ficam em cima: Aprovar usa uma vaga livre.'),
 ('Editar, bloquear, excluir', 'Bloquear libera o assento e encerra a sessão. Excluir pede para quem passar os cards.'),
 ('Equipes', 'Nova Equipe com nome e líder.')], c='Clique nos números')
tourA('usuario2', C8, 'Editar usuário a fundo', '<b>Usuário</b> Editar', 'Cada campo do usuário, <em>de cima para baixo</em>.', 'dir', [
 ('Informações básicas', 'Nome, e-mail, tipo Funcionário ou Cliente e a jornada semanal.'),
 ('Permissões e acessos', 'É Gestor, Edição de Custos e Acessa Relatórios. Administrador só a 75 LAB promove.'),
 ('Áreas liberadas', 'Marque cada área. Em cada uma, escolha edita ou só vê.'),
 ('Colunas visíveis', 'Limite as colunas por quadro. Liberar todas desfaz.'),
 ('Senha e salvar', 'Resetar senha manda o link por e-mail. Salvar grava só o que mudou.')])
PAPEIS = ['75 LAB', 'Admin', 'Gestor', 'Pessoa do time', 'Cliente']
PAPEL_TXT = ['Dona da plataforma: abre assentos, envia convites e promove administradores.',
             'Configura a empresa, aprova quem chega e decide o que cada pessoa vê.',
             'Lidera um time: vê os números de cada pessoa nos relatórios. Não abre a Administração.',
             'Trabalha nos cards e nas áreas que o admin liberou.',
             'Acompanha o que é dele e responde por link. Não ocupa assento pago.']
LINHAS = [('Abrir assento e enviar convite', 'S....'), ('Aprovar quem se cadastrou, com vaga livre', 'SS...'), ('Tornar alguém administrador', 'S....'),
          ('Mudar os Ajustes da empresa', 'SS...'), ('Editar áreas, permissões e colunas', 'SS...'), ('Criar, arquivar e excluir quadros', 'SS...'),
          ('Ver os números de cada pessoa', 'SSS..'), ('Ver custos e margem', 'SSCC.'), ('Abrir os departamentos', 'SSAA.'),
          ('Trabalhar nos cards, dar Play e comentar', 'SSSS.'), ('Acompanhar o próprio job por link', '....S')]
SIM = {'S': '<i class="mx s" title="Pode">●</i>', 'C': '<i class="mx c" title="Com a chave Edição de Custos">◐</i>', 'A': '<i class="mx c" title="Se a área estiver liberada">◐</i>', '.': '<i class="mx n"></i>'}
cab_m = '<div class="mz-l mz-cab"><span></span>' + ''.join(f'<button class="mz-p" data-k="{i}" data-t="{e(PAPEL_TXT[i])}" data-cursor="">{e(p)}</button>' for i, p in enumerate(PAPEIS)) + '</div>'
lin_m = ''.join(f'<div class="mz-l"><span>{e(t)}</span>' + ''.join(f'<b data-k="{i}">{SIM[c]}</b>' for i, c in enumerate(v)) + '</div>' for t, v in LINHAS)
add(f'''<section class="tela s-matriz" data-abas=".mz-p" {attrs(C8, "Quem pode o quê")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Matriz</b> Papéis</div><h2>Quem pode o quê, <em>papel por papel</em>.</h2></div>{cta("Clique em cada papel")}</div>
<div class="mz">{cab_m}{lin_m}</div>
<div class="mz-pe"><p id="mzTxt"></p><span><i class="mx s">●</i> pode <i class="mx c">◐</i> com a chave de custos ou a área liberada</span></div></section>''')
tourA('perfil', C8, 'Equipes, perfil e avisos', '<b>Cada um</b> Perfil', 'O que cada pessoa <em>ajusta para si</em>.', 'foco', [
 ('Equipes', 'Nome e líder. A equipe vira filtro nos quadros e relatórios.'),
 ('Meu perfil', 'Foto, modo ausente, tema escuro e trocar a senha. Abre no seu nome, no pé do menu.'),
 ('Notificações', 'No sininho: escolha o que aparece e ligue o aviso no navegador.')], c='Clique nos números')

# ================================================================= 9 clientes
C9 = '9 · Clientes e projetos'
capitulo(9, 'Clientes e projetos', 'Consulta', 'Para quem atende cliente', ['Cadastro completo e contrato', 'Relatório e repositório por link', 'Entrega com aprovação do cliente'])
tourA('cliente2', C9, 'Cadastro completo do cliente', '<b>Cliente</b> Cadastro', 'O cliente completo, <em>com contrato e horas</em>.', 'esq', [
 ('O básico', 'Nome, segmento, e-mail e telefone. A logo entra aqui.'),
 ('Outros contatos', 'Quantos contatos precisar, cada um com o seu papel.'),
 ('Dados de faturamento', 'Razão social, CNPJ e endereço completo.'),
 ('Quem aprova', 'Os e-mails que aprovam já vêm preenchidos ao enviar uma entrega.'),
 ('Contrato', 'Horas contratadas por mês, prazo e regras de pagamento.')])
tourA('clienterel', C9, 'Relatório e repositório', '<b>Cliente</b> Links', 'O cliente vê o trabalho <em>sem precisar de login</em>.', 'trilho', [
 ('Clique no nome do cliente', 'Dados do cliente, Relatório ou Repositório.'),
 ('Relatório por link', 'Escolha o que entra (financeiro fica desligado) e gere o link. O retrato fica congelado.'),
 ('Modo cliente', 'Troca o nome de cada pessoa pela área dela. Também baixa em PDF.'),
 ('Repositório', 'Os arquivos do cliente num link só. Adicione do Drive e esconda o que for interno.')], c='Clique nos números')
tourA('projetos2', C9, 'Projetos a fundo', '<b>Projeto</b> Cadastro', 'Projeto com <em>orçamento, horas e prazos</em>.', 'dir', [
 ('Status do projeto', 'Abertos, concluídos, arquivados e cancelados. Favoritos no topo.'),
 ('Modelo de projeto', 'Comece de um modelo e as etapas viram as colunas do quadro.'),
 ('Orçamento e horas', 'O valor e as horas previstas. O saldo aparece para quem vê custos.'),
 ('Três prazos', 'Início, prazo estimado e o prazo que o cliente pediu.')])
tourA('entrega', C9, 'Entrega e aprovação', '<b>Cliente</b> Aprovação', 'O cliente aprova <em>pelo link, sem login</em>.', 'foco', [
 ('Enviar ao cliente', 'Na aba Anexos do card.'),
 ('Arquivos, links e recado', 'Gere o link de aprovação e mande por e-mail ou pelo Ariuno. O cliente aprova ou reprova com comentário.'),
 ('Link de acompanhamento', 'O cliente acompanha as etapas do job a qualquer hora.')], c='Clique nos números')

# ================================================================= 10 quadros
C10 = '10 · Quadros e cards'
capitulo(10, 'Quadros e cards', 'Consulta', 'Para quem organiza o fluxo', ['Quem vê cada quadro', 'Filtros, colunas e ações em massa', 'Automações e o card por inteiro'])
tourA('quadro2', C10, 'Ferramentas do quadro', '<b>Quadro</b> Topo', 'Os ícones do topo, <em>um por um</em>.', 'trilho', [
 ('Os ícones', 'Planilha, novo quadro, renomear, quem pode ver, arquivar e excluir.'),
 ('Quem pode ver', 'Marque as pessoas. Ninguém marcado: a empresa toda vê.'),
 ('Arquivar', 'O quadro sai da frente sem apagar nenhum card. Desarquivar traz de volta.')], c='Clique nos números')
tourA('filtros', C10, 'Filtros e busca', '<b>Quadro</b> Filtros', 'Ache qualquer card <em>em segundos</em>.', 'esq', [
 ('Busca', 'Por título, número ou etiqueta.'),
 ('Filtros', 'Situação, etapa, responsável, prioridade e cliente.'),
 ('Avançado', 'Período, equipes, projetos e situações especiais, como atrasadas ou aguardando o cliente. Salve o filtro com um nome.'),
 ('O que ver', 'Todas ou Minhas. Tudo, só Principais ou só Subtarefas.')])
tourA('coluna2', C10, 'Opções da coluna', '<b>Coluna</b> Opções', 'Cada coluna <em>com a sua regra</em>.', 'foco', [
 ('Ordenar cartões', 'Arrastar à mão, por nome, prazo, prioridade ou data.'),
 ('Filtrar por período', 'Mostra só o que vence ou foi criado no período.'),
 ('Conclusão', 'Marque qual é o Concluído e qual é o Perdidos. Soltar ali fecha o card.'),
 ('Departamento', 'Liga a coluna a um departamento: o card aparece no módulo da área.'),
 ('Zona de perigo', 'Excluir só funciona com a coluna vazia.')], c='Clique nos números')
tourA('lista2', C10, 'Lista e ações em massa', '<b>Lista</b> Em massa', 'Mude dezenas de cards <em>de uma vez</em>.', 'dir', [
 ('Colunas e exportar', 'Escolha as colunas da lista e exporte em CSV.'),
 ('Selecione e mude', 'Marque os cards: mover, responsável, prazo, prioridade, etiqueta ou concluir.')])
tourA('auto2', C10, 'Automações a fundo', '<b>Automações</b> Quadro', 'Regras que <em>trabalham sozinhas</em>.', 'esq', [
 ('Comece por uma pronta', 'Seis regras prontas, como card parado há 3 dias.'),
 ('Quando', 'Entrou ou saiu de etapa, foi criado, mudou um campo, venceu, ficou parado, o cliente respondeu ou no relógio.'),
 ('Só se', 'Filtre por quadro, tipo, cliente, projeto, prioridade ou título.'),
 ('Então', 'Criar card ou subtarefas de um modelo, mover, trocar responsável, avisar, comentar ou concluir.'),
 ('Salvar automação', 'Ligue, desligue e teste com Executar agora.')])
tourA('card2', C10, 'Mais do card', '<b>Card</b> Ações', 'O que o card faz <em>além do básico</em>.', 'trilho', [
 ('Mais ações', 'Copiar o link, duplicar com subtarefas e imprimir em PDF.'),
 ('Salvar como modelo', 'O card bom vira modelo para os próximos.'),
 ('Lembretes', 'Data, hora, para quem e com confirmação de leitura.'),
 ('Atividade', 'Quem fez o quê e quando, no card inteiro.')], c='Clique nos números')

# ================================================================= 11 tempo
C11 = '11 · Tempo e rotina'
capitulo(11, 'Tempo e rotina', 'Consulta', 'Para o time inteiro', ['Timesheet e Planner a fundo', 'Reuniões, avisos e notificações', 'Os 15 pedidos das Solicitações'])
tourA('timesheet2', C11, 'Timesheet a fundo', '<b>Horas</b> Timesheet', 'Todas as horas, <em>de quatro jeitos</em>.', 'dir', [
 ('Quatro abas', 'Apontamentos, Grade, Produtividade e Custos.'),
 ('Grade', 'Pessoa por dia: onde faltou registro salta aos olhos.'),
 ('Produtividade', 'Horas por pessoa, cliente e projeto, com retrabalho separado.'),
 ('Lançar e exportar', 'Lançar horas de qualquer dia e exportar em CSV.')])
tourA('planner2', C11, 'Planner a fundo', '<b>Agenda</b> Planner', 'Planeje a semana <em>arrastando</em>.', 'foco', [
 ('De quem é a agenda', 'A sua, a de um colega ou todos os calendários.'),
 ('Dia, semana ou mês', 'Hoje volta para o dia atual.'),
 ('Arraste a subtarefa', 'Busque a subtarefa e solte no horário. Ajuste duração e dias.')], c='Clique nos números')
tourA('rotina2', C11, 'Reunião, IA e avisos', '<b>Rotina</b> Barra lateral', 'A barra da direita <em>e o sininho</em>.', 'esq', [
 ('Barra da direita', 'Ariuno IA, Registrar reunião e Conversas.'),
 ('Registrar reunião', 'Reunião, prospecção, visita ou evento, com cliente ou interno. O tempo entra sozinho.'),
 ('Notificações', 'Do time ou do agente. Escolha o que aparece e marque como lidas.')])
GR = [('Dinheiro e pagamentos', 'Financeiro', ['Reembolso de despesas', 'Adiantamento', 'Pagar uma nota fiscal', 'Pagar um fornecedor'], 'Aprovar pagamento pede a nota fiscal ou o comprovante.'),
      ('Compras e viagens', 'Compras', ['Comprar material ou equipamento', 'Contratar freelancer ou terceiro', 'Viagem a trabalho'], 'Quem é de Compras recebe e responde.'),
      ('Pessoas e RH', 'RH', ['Férias', 'Folga ou day off', 'Home office', 'Enviar atestado médico', 'Atualizar meus dados', 'Pedir um documento ao RH'], 'Atestado pede foto ou PDF. Aprovado vira ausência no RH.'),
      ('Acessos e outros', 'Administração', ['Acesso, equipamento ou TI', 'Outro pedido'], 'Em Outro pedido, você escolhe a área.')]
gr = ''.join(f'<button class="sq" data-t="{e(r)}" data-para="{e(pa)}" data-r="{e(r)}" data-cursor=""><small>Vai para {e(pa)}</small><b>{e(n)}</b><ul>' + ''.join(f'<li>{e(x)}</li>' for x in it) + '</ul></button>' for n, pa, it, r in GR)
add(f'''<section class="tela s-solic" data-abas=".sq" {attrs(C11, "Os 15 pedidos")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Solicitações</b> 15 tipos</div><h2>Quinze pedidos, <em>quatro caminhos</em>.</h2></div>{cta("Clique em cada grupo")}</div>
<div class="sqs">{gr}</div>
<div class="sq-pe"><div><small>Regra do grupo</small><p id="sqR"></p></div><div><small>Para todos</small><p>Recusar sempre pede motivo. Quem pediu edita ou cancela enquanto ninguém respondeu. Admin e diretoria recebem todas as áreas.</p></div></div></section>''')

# ================================================================= 12 departamentos
C12 = '12 · Departamentos'
capitulo(12, 'Departamentos', 'Consulta', 'Só aparece o que o admin liberou', ['Como liberar cada área', 'Dez departamentos, aba por aba', 'O que entra e sai por planilha'])
DEP = [('Comercial', 'Funil de vendas, atividades, contatos, orçamentos e faturamento.', 'Negócios'),
       ('Marketing', 'Campanhas, calendário, pedidos, verba, leads e marca.', 'Nova campanha'),
       ('RH', 'Fichas, organograma, ausências, férias, vagas, desempenho e clima.', 'Importar equipe'),
       ('Impulsionamento', 'Anúncios e redes sociais num painel, com relatório para o cliente.', 'Importar'),
       ('Compras', 'Catálogo de itens, fornecedores e cotações lado a lado.', 'Novo item'),
       ('Tráfego', 'Gestão Operacional: jobs, capacidade, gargalos e entregas.', 'Visão Executiva'),
       ('Criação', 'Entregáveis, aprovações e o acervo de peças.', 'Acervo'),
       ('Social Mídia', 'Calendário de posts, do roteiro ao publicado.', 'Novo post'),
       ('Estoque', 'Materiais por cliente: itens, reservas e movimentos.', 'Novo item'),
       ('RP', 'Pautas, imprensa e comprovação das matérias.', 'Nova pauta')]
dep = ''.join(f'<button class="dp" data-t="{e(d)}" data-o="{e(d)}" data-p="{e(pc)}" data-cursor="">{e(n)}</button>' for n, d, pc in DEP)
add(f'''<section class="tela s-deptos" data-abas=".dp" {attrs(C12, "Quem vê cada departamento")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Departamentos</b> Acesso</div><h2>Dez áreas. <em>Cada pessoa vê as suas.</em></h2></div>{cta("Clique em cada área")}</div>
<div class="dps"><div class="dp-grade">{dep}</div><div class="dp-pn"><h3 id="dpN"></h3><p id="dpO"></p><div class="lin"><b>Primeiro clique</b><span id="dpP"></span></div></div></div>
<div class="regra">Para liberar: <b>Equipe, Editar Usuário, Áreas liberadas</b>. Em cada área, <b>edita</b> ou <b>só vê</b>. Admin vê todas.</div></section>''')
tourA('comercial1', C12, 'Comercial: o funil', '<b>Comercial</b> Funil', 'Do primeiro contato <em>ao negócio ganho</em>.', 'dir', [
 ('Visão Geral', 'Metas de receita, funil em números e ranking dos executivos.'),
 ('Negócios', 'O funil em colunas: Lead, Prospecção, Reunião, Proposta e Negociação.'),
 ('Novo negócio', 'Pessoa, empresa, título, valor, previsão de fechamento e origem.'),
 ('Ganho ou Perdido', 'Arraste entre as etapas. Ganho pede o pedido de compra e vai para o Faturamento. Perdido pede o motivo.'),
 ('Atividades', 'Ligações, reuniões e tarefas com data. Atrasadas e de hoje em destaque.')])
tourA('comercial2', C12, 'Comercial: orçamento e faturamento', '<b>Comercial</b> Fechamento', 'Do orçamento <em>à nota fiscal</em>.', 'trilho', [
 ('Montar orçamento', 'Itens do catálogo de Compras, quantidade, desconto e impostos.'),
 ('Ganho ou Perdido', 'Baixe o PDF só com a venda. Ganho manda para o Faturamento.'),
 ('Faturamento', 'A fila do que foi ganho. Registrar NF com número, datas, valor e arquivo.'),
 ('Relatórios', 'Conversão, previsão de receita, tempo por etapa e motivos de perda.'),
 ('Importar e exportar', 'Negócios, pessoas, empresas e atividades por planilha. A exportação do Pipedrive entra como está.')], c='Clique nos números')
tourA('marketing1', C12, 'Marketing: campanhas', '<b>Marketing</b> Campanhas', 'A campanha da ideia <em>ao relatório final</em>.', 'esq', [
 ('Painel', 'Campanhas no ar, entregas atrasadas, aprovações e leads sem resposta.'),
 ('Nova campanha', 'Nome, tipo, dono, datas, verba prevista, canais e metas.'),
 ('Campanhas', 'Lista, quadro ou linha do tempo. A ficha tem briefing, entregas, verba e resultados.'),
 ('Calendário', 'Campanhas, posts, pautas, eventos e datas comerciais no mesmo mês.')])
abas('marketing2', C12, 'Marketing: pedidos, verba e leads', '<b>Marketing</b> Rotina', 'Pedidos, verba, leads <em>e a marca</em>.', [
 ('Pedidos', 'Pedidos para o marketing', 'Qualquer área pede. O time analisa e aceita como campanha, post ou tarefa no quadro.', 'Pedir informação devolve a quem pediu'),
 ('Verba', 'Verba', 'Planejado, usado e disponível por categoria, no ano.', 'Lançar despesa desconta na hora'),
 ('Leads', 'Leads e resultados', 'Registre ou importe leads, qualifique e envie ao Comercial.', 'Enviar ao Comercial cria o negócio'),
 ('Marca', 'Marca e conteúdo', 'Guia de marca, tom de voz, pilares, personas e datas comerciais.', 'Só gestores mudam a marca')],
 'Clique em cada aba', REG)
tourA('rh1', C12, 'RH: pessoas e organograma', '<b>RH</b> Pessoas', 'O time com ficha <em>e organograma</em>.', 'foco', [
 ('Importar equipe', 'Cada usuário do Ariuno vira uma ficha de pessoa.'),
 ('A ficha', 'Cargo, área, gestor, admissão, salário e documentos. Dados pessoais só o RH vê.'),
 ('Organograma', 'Montado pelo gestor de cada um. Dá para arrastar, imprimir e baixar a imagem.')], c='Clique nos números')
abas('rh2', C12, 'RH: ausências, férias e clima', '<b>RH</b> Rotina', 'Do pedido de folga <em>à pesquisa de clima</em>.', [
 ('Ausências', 'Ausências', 'Férias, atestado, folga, licença, banco de horas e home office, com aprovação.', 'A pessoa recebe a resposta'),
 ('Férias', 'Férias', 'Saldo, vencimento e programação pela regra da CLT.', 'Relatório em CSV'),
 ('Recrutamento', 'Recrutamento', 'Vaga, funil de candidatos e contratação.', 'Contratar, reprovar ou desistiu'),
 ('Desempenho', 'Desempenho', 'Ciclos de avaliação, 360, PDI e histórico por pessoa.', 'Exporta em PDF'),
 ('Entrada e saída', 'Entrada e saída', 'Modelos de jornada para quem chega e para quem sai.', 'Cada passo com responsável'),
 ('Clima', 'Clima', 'Humor do dia e pesquisas de eNPS, clima e pulso.', 'Abrir para o time mostra a todos')],
 'Clique em cada aba', REG)
tourA('impuls', C12, 'Impulsionamento', '<b>Impulsionamento</b> Mídia', 'Anúncios e redes <em>num painel só</em>.', 'dir', [
 ('Painel', 'Investimento, resultados, custo por resultado, ROAS, alcance e engajamento.'),
 ('Anúncios', 'Cada campanha com plataforma, objetivo, verba e resultados.'),
 ('Redes sociais', 'Os números de cada perfil, mês a mês.'),
 ('Importar', 'Relatório do Meta, Google, TikTok ou LinkedIn em CSV, com prévia.'),
 ('Relatório', 'Pronto para o cliente: anotações, resumo para copiar e PDF.')])
tourA('compras', C12, 'Compras', '<b>Compras</b> Cotações', 'Catálogo, fornecedores <em>e cotações</em>.', 'trilho', [
 ('Painel', 'O resumo e as próximas demandas.'),
 ('Itens', 'O catálogo: especificação, variações, unidade e prazo. Vira item do orçamento do Comercial.'),
 ('Fornecedores', 'Contato, telefone, e-mail, CNPJ e categoria.'),
 ('Cotações', 'Vários fornecedores lado a lado: preço, frete, mínimo e prazo. Escolha o melhor.')], c='Clique nos números')
abas('trafego', C12, 'Tráfego: gestão operacional', '<b>Tráfego</b> Operação', 'A operação inteira <em>em números</em>.', [
 ('Executiva', 'Visão Executiva', 'O resumo da operação e quem está trabalhando agora.', 'Filtre por quadro e pessoa'),
 ('Jobs', 'Jobs e projetos', 'Cada job com etapa, prazo e horas.', 'Tarefas-mãe ou subtarefas'),
 ('Gargalos', 'Áreas e gargalos', 'Onde o trabalho está parado.', 'Olhe toda segunda'),
 ('Capacidade', 'Capacidade do time', 'Quem está cheio e quem tem espaço.', 'Bom para distribuir'),
 ('Aprovações', 'Aprovações e qualidade', 'O que foi para o cliente e o que voltou.', 'Reprovação vira ajuste'),
 ('Por pessoa', 'Entregas por usuário', 'O que cada um entregou no período.', 'Para o feedback'),
 ('Concluídas', 'Entregas concluídas', 'O que fechou. Ciente dá baixa.', 'Dar baixa em todas')],
 'Clique em cada aba', REG)
tourA('criacao', C12, 'Criação', '<b>Criação</b> Produção', 'A fila de quem <em>produz</em>.', 'esq', [
 ('Painel', 'Entregáveis, atrasos e aprovações da área.'),
 ('Aprovações e revisões', 'O que foi ao cliente e o que voltou para ajuste.'),
 ('Acervo', 'Novo ativo com versão, autor, link do arquivo e direito de uso.')])
tourA('social', C12, 'Social Mídia', '<b>Social</b> Posts', 'Do roteiro <em>ao post publicado</em>.', 'dir', [
 ('Calendário', 'Todas as redes, campanhas e clientes, mês a mês.'),
 ('Quadro', 'Ideia, roteiro, produção, edição, aprovação, agendado e publicado.'),
 ('Novo post', 'Redes, data, responsável, legenda, hashtags e quem aprova.')])
tourA('estoquerp', C12, 'Estoque e RP', '<b>Estoque e RP</b> Áreas', 'Materiais por cliente, <em>pautas e imprensa</em>.', 'foco', [
 ('Estoque', 'Novo item com cliente dono, unidade, mínimo e custo. Dar entrada, dar saída e reservar.'),
 ('RP', 'Nova pauta, do rascunho à matéria publicada. Imprensa e comprovação em abas.')], c='Clique nos números')

# ================================================================= 13 gestão
C13 = '13 · Gestão a fundo'
capitulo(13, 'Gestão a fundo', 'Consulta', 'Para quem lidera', ['Relatórios e extrator', 'Meta contra realizado', 'Arena Ariuno'])
tourA('relat2', C13, 'Relatórios a fundo', '<b>Relatórios</b> Gestão', 'Os números da empresa, <em>sem planilha</em>.', 'dir', [
 ('Relatórios', 'Meu desempenho, contagem regressiva das entregas e o termômetro. Exporta em PDF.'),
 ('Central de Relatórios', 'Da empresa, por usuário ou por cliente.'),
 ('Meta x realizado', 'Clique no valor para definir a meta do mês. O realizado vem do Comercial.'),
 ('Extrator detalhado', 'Copie para o Excel, exporte em PDF ou baixe o CSV com os registros de tempo.')])
abas('arena', C13, 'Arena Ariuno', '<b>Arena</b> Gamificação', 'Missões, ranking <em>e prêmios</em>.', [
 ('Evolução', 'Minha evolução', 'Os pontos e o nível de cada pessoa.', 'Cada entrega conta'),
 ('Ranking', 'Ranking geral', 'Quem mais entregou no período.', 'O admin pode zerar o placar'),
 ('Conquistas', 'Minhas conquistas', 'As medalhas de cada missão cumprida.', 'O admin cria as missões'),
 ('Loja', 'Loja de prêmios', 'Os pontos viram prêmios definidos pela empresa.', 'Catálogo no botão do admin')],
 'Clique em cada aba', REG)
