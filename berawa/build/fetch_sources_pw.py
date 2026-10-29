#!/usr/bin/env python3
"""Primera lectura de una web publica que se pinta con JavaScript (SOLO para generar la evidencia). Igual que fetch_sources.py pero con el navegador de Playwright.
Guarda el texto visible normalizado de cada pagina en berawa/evidence/source-text.json ({url: texto}). Requiere red.
Uso: python3 berawa/build/fetch_sources_pw.py URL_INICIAL [--max 25] [--lang es]   (solo sigue enlaces del mismo dominio y de la misma ruta de idioma)"""
import sys,re,json,urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright
from _rutas import ROOT,SOURCE_TEXT
start=sys.argv[1]; mx=int(sys.argv[sys.argv.index('--max')+1]) if '--max' in sys.argv else 25
lang=sys.argv[sys.argv.index('--lang')+1] if '--lang' in sys.argv else ''
host=urllib.parse.urlparse(start).netloc.replace('www.','')
seen={};queue=[start]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']); pg=b.new_page(user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36')
    while queue and len(seen)<mx:
        u=queue.pop(0)
        try: pg.goto(u,wait_until='networkidle',timeout=45000); pg.wait_for_timeout(1200)
        except Exception as e: print('ERR',u,e); continue
        fu=pg.url.split('#')[0].rstrip('/')
        if fu in seen: continue
        seen[fu]=re.sub(r'\s+',' ',pg.inner_text('body')).strip()
        for h in pg.eval_on_selector_all('a[href]','els=>els.map(e=>e.href)'):
            a=h.split('#')[0].rstrip('/'); pu=urllib.parse.urlparse(a)
            if pu.scheme in('http','https') and pu.netloc.replace('www.','')==host and a not in seen and a not in queue and not re.search(r'\.(pdf|jpg|png|webp|zip)$',a,re.I) and (not lang or ('/'+lang) in pu.path): queue.append(a)
    b.close()
SOURCE_TEXT.parent.mkdir(parents=True,exist_ok=True)
SOURCE_TEXT.write_text(json.dumps(seen,ensure_ascii=False,indent=1),encoding='utf-8')
print(len(seen),'paginas guardadas en',SOURCE_TEXT)
for u,t in seen.items(): print(len(t),u)
