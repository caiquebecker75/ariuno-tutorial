# Página videos.html: todos os vídeos curtos e GIFs do manual, para assistir e compartilhar.
# Roda dentro do montar.py (usa RAIZ, VID, telas, e, VER, LINK).
import re as _re

def _tela_do_video(vid):
    for i, h in enumerate(telas):
        if f'data-video="{vid}"' in h: return i + 1
    return 0

def _dur(s):
    s = int(round(s)); return f'{s // 60}:{s % 60:02d}'

def _grupo(v):
    n = (v.get('num') or '').split('·')[-1].strip().title() or 'Manual'
    return n.replace('Dia A Dia', 'Dia a dia')

_grupos = {}
for v in VID: _grupos.setdefault(_grupo(v), []).append(v)

_cards = ''
for g, vs in _grupos.items():
    itens = ''
    for v in vs:
        n = _tela_do_video(v['id'])
        ir = f'<a href="./#{n}">Abrir a tela {n:02d} do manual</a>' if n else ''
        itens += (f'<article class="v"><video controls playsinline preload="none" poster="assets/videos/{v["id"]}.jpg" src="assets/videos/{v["id"]}.mp4"></video>'
                  f'<div class="vt"><h3>{e(v["titulo"])}</h3><p>{e(v.get("sub", ""))}</p><div class="meta"><span>{_dur(v.get("fim", 0))}</span>{ir}</div></div></article>')
    _cards += f'<section class="grupo"><h2>{e(g)}</h2><div class="grade">{itens}</div></section>'

_gifs = ''.join(
    f'<figure><img loading="lazy" src="assets/gifs/{v["id"]}.gif" alt="{e(v["titulo"])}" width="880" height="495"><figcaption><b>{e(v["titulo"])}</b><a href="assets/gifs/{v["id"]}.gif" download>Baixar GIF</a></figcaption></figure>'
    for v in VID if v.get('gif') and (RAIZ/'assets/gifs'/(v['id'] + '.gif')).exists())

_pagina = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vídeos do Ariuno</title>
<meta name="description" content="Vídeos curtos e GIFs do manual do Ariuno: configurar a empresa, usuários, quadros, rotina e cada departamento.">
<meta name="robots" content="noindex">
<link rel="icon" href="assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=Space+Grotesk:wght@400;500;600&family=Space+Mono:wght@700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#F7F8FD;--card:#fff;--ink:#0B0D1E;--txt2:#5A6180;--line:#E1E5F3;--iris:#6A5CFF;--iris-ink:#4B3BE0;--lime:#C0EE4E;color-scheme:light}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0B0D1E;--card:#151934;--ink:#EEF0FA;--txt2:#B3B8D3;--line:#262B4D;--iris:#8A7FFF;--iris-ink:#B3ABFF;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0B0D1E;--card:#151934;--ink:#EEF0FA;--txt2:#B3B8D3;--line:#262B4D;--iris:#8A7FFF;--iris-ink:#B3ABFF;color-scheme:dark}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font:400 16px/1.55 'Space Grotesk',system-ui,sans-serif}}
.wrap{{max-width:1200px;margin:0 auto;padding:40px 16px 80px}}
header .eb{{font:700 12px/1 'Space Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--iris-ink)}}
h1{{font:800 clamp(34px,6vw,56px)/1.04 'Archivo',sans-serif;letter-spacing:-.02em;margin:12px 0 12px}}
h1 em{{font-style:normal;color:var(--iris)}}
.lead{{font-size:18px;color:var(--txt2);max-width:720px}}
.topo{{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}}
.topo a{{font:700 13px/1 'Space Mono',monospace;text-decoration:none;color:var(--ink);background:var(--card);border:1px solid var(--line);padding:11px 14px;border-radius:9px}}
.topo a.principal{{background:var(--lime);border-color:var(--lime);color:#0B0D1E}}
.grupo{{margin-top:48px}}
.grupo h2,.gifs h2{{font:800 26px/1.1 'Archivo',sans-serif;margin-bottom:16px}}
.grade{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:18px}}
.v{{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.v video{{display:block;width:100%;aspect-ratio:16/9;background:#000}}
.vt{{padding:14px 16px 16px}}
.vt h3{{font:700 18px/1.2 'Archivo',sans-serif}}
.vt p{{color:var(--txt2);font-size:15px;margin-top:4px}}
.meta{{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:10px;font-size:14px}}
.meta span{{font:700 12px/1 'Space Mono',monospace;color:var(--txt2)}}
.meta a{{color:var(--iris-ink);font-weight:600}}
.gifs{{margin-top:60px;padding-top:40px;border-top:1px solid var(--line)}}
.gifs .lead{{margin-bottom:18px}}
.ggrade{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:18px}}
figure{{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
figure img{{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;background:var(--line)}}
figcaption{{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:12px 14px}}
figcaption a{{font:700 12px/1 'Space Mono',monospace;color:var(--iris-ink);white-space:nowrap}}
footer{{margin-top:60px;font-size:14px;color:var(--txt2)}}
</style>
</head>
<body><main class="wrap">
<header><p class="eb">Manual do Ariuno</p><h1>Vídeos <em>curtos</em> e GIFs</h1>
<p class="lead">Cada vídeo mostra um assunto do manual na demonstração do Ariuno, com dados fictícios. Assista na ordem ou vá direto ao que precisa.</p>
<div class="topo"><a class="principal" href="./">Abrir o manual completo</a><a href="#gifs">Ir para os GIFs</a></div></header>
{_cards}
<section class="gifs" id="gifs"><h2>GIFs para mandar no grupo</h2><p class="lead">Os mesmos assuntos em poucos segundos, sem som, para colar no WhatsApp ou no e-mail.</p><div class="ggrade">{_gifs}</div></section>
<footer>Ariuno · uma plataforma da 75 LAB · {len(VID)} vídeos</footer>
</main></body></html>
'''
(RAIZ/'videos.html').write_text(_pagina, encoding='utf-8')
