#!/usr/bin/env python3
"""Traz os vídeos curtos e GIFs gravados em ariuno-videos/saida/manual para o manual.
Rodar: python3 fonte/trazer_videos.py   (depois: python3 fonte/montar.py)"""
import json, pathlib, shutil, subprocess

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ORIGEM = RAIZ.parent / 'ariuno-videos' / 'saida' / 'manual'
VIDEOS, GIFS = RAIZ / 'assets' / 'videos', RAIZ / 'assets' / 'gifs'
VIDEOS.mkdir(parents=True, exist_ok=True); GIFS.mkdir(parents=True, exist_ok=True)

# a lista sai dos roteiros, para a ordem e os títulos baterem com o que foi gravado
js = subprocess.run(['node', '-e', "import('./tools/roteiros-manual.mjs').then(m=>console.log(JSON.stringify(m.ROTEIROS_MANUAL.map(r=>({id:r.id,num:r.num,titulo:r.titulo,sub:r.sub,fim:r.fim,gif:!!r.gif,tela:r.tela||''})))))"],
                    cwd=RAIZ.parent / 'ariuno-videos', capture_output=True, text=True, check=True).stdout
lista = json.loads(js)
ok = []
for v in lista:
    mp4 = ORIGEM / f"{v['id']}.mp4"
    if not mp4.exists(): print('sem vídeo:', v['id']); continue
    shutil.copy2(mp4, VIDEOS / mp4.name)
    shutil.copy2(ORIGEM / f"{v['id']}.jpg", VIDEOS / f"{v['id']}.jpg")
    gif = ORIGEM / f"{v['id']}.gif"
    if v['gif'] and gif.exists(): shutil.copy2(gif, GIFS / gif.name)
    ok.append(v)
(VIDEOS / 'videos.json').write_text(json.dumps(ok, ensure_ascii=False, indent=1), encoding='utf-8')
tam = sum(f.stat().st_size for f in list(VIDEOS.glob('*')) + list(GIFS.glob('*'))) / 1e6
print(f'{len(ok)} vídeos trazidos, {tam:.1f} MB em vídeos e GIFs')
