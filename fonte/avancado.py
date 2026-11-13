# Manual avançado: capítulos 7 em diante, para consulta depois da reunião.
# Roda dentro do montar.py (usa add, tour, abas, capitulo, attrs, cta, e, VID, telas, json).

# ---------------------------------------------------------------- abertura e índice do manual
add(f'''<section class="tela s-avanc" {attrs("Manual avançado", "Manual avançado", "claro")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Manual avançado</b> Para consultar depois</div><h2>Tudo o que o Ariuno faz, <em>tela por tela</em>.</h2></div>{cta("Clique no assunto")}</div>
<p class="lead">A reunião termina no teste rápido. Daqui em diante é consulta: cada assunto tem o passo a passo na tela real e, quando houver, um vídeo curto no botão verde do topo.</p>
<div class="ind" data-caps="7-99" data-cols="4"></div></section>''')

exec((RAIZ/'fonte/capitulos.py').read_text(encoding='utf-8')) if (RAIZ/'fonte/capitulos.py').exists() else None

# ---------------------------------------------------------------- vídeos e GIFs
if VID:
    NCAP = len([1 for t in telas if 'class="tela s-cap"' in t]) + 1
    C_V = f'{NCAP} · Vídeos e GIFs'
    capitulo(NCAP, 'Vídeos e GIFs', f'{len(VID)} vídeos curtos', 'Para assistir e compartilhar', ['Cada assunto em menos de um minuto', 'GIFs para mandar no grupo do time'])
    grupos = {}
    for v in VID: grupos.setdefault((v.get('num') or 'Manual').split('·')[-1].strip().capitalize(), []).append(v)
    blocos = ''.join(f'<div class="vg"><h4>{e(g)}</h4>' + ''.join(f'<button data-abre-video="{v["id"]}" data-cursor="Assistir"><i>▶</i><span>{e(v["titulo"])}</span><u>{int(v["fim"]) // 60}:{int(v["fim"]) % 60:02d}</u></button>' for v in vs) + '</div>' for g, vs in grupos.items())
    add(f'''<section class="tela" {attrs(C_V, "Vídeos do manual")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Assista</b> {len(VID)} vídeos curtos</div><h2>Cada assunto <em>em menos de um minuto</em>.</h2></div><a class="botao lime so-tela" href="videos.html" target="_blank" rel="noopener" data-cursor="Abrir">Página dos vídeos →</a></div>
<div class="vlist">{blocos}</div></section>''')
    GIFS = [v for v in VID if v.get('gif') and (RAIZ/'assets/gifs'/(v['id'] + '.gif')).exists()]
    if GIFS:
        esc = [v for v in GIFS if v['id'].split('-')[0] in ('m10', 'm07', 'm09', 'm11', 'm13', 'm16', 'm23')] or GIFS[:7]
        bts = ''.join(f'<button data-gif="assets/gifs/{v["id"]}.gif" data-t="{e(v["sub"])}" data-cursor="">{e(v["titulo"])}</button>' for v in esc)
        add(f'''<section class="tela s-gifs" data-abas=".gl button" {attrs(C_V, "GIFs para compartilhar")}><div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb"><b>Compartilhe</b> {len(GIFS)} GIFs</div><h2>Mande no grupo: <em>o GIF ensina sozinho</em>.</h2></div><a class="botao lime so-tela" href="videos.html#gifs" target="_blank" rel="noopener" data-cursor="Abrir">Baixar os GIFs →</a></div>
<div class="gifs2"><div class="gl">{bts}</div><div class="gv"><img id="gifAtual" alt="GIF do Ariuno"></div></div></section>''')
