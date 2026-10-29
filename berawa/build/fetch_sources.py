#!/usr/bin/env python3
"""Primera lectura de la web publica del negocio (SOLO para generar la evidencia; no hace falta para verificar la demo).
Rastrea el mismo dominio (max N paginas), guarda el texto visible normalizado de cada una en berawa/evidence/source-text.json
({url: texto}). Requiere red. Uso: python3 berawa/build/fetch_sources.py URL_INICIAL [--max 25]"""
import sys,re,json,urllib.request,urllib.parse,html as H
from pathlib import Path
from _rutas import ROOT,SOURCE_TEXT
start=sys.argv[1]; mx=int(sys.argv[sys.argv.index('--max')+1]) if '--max' in sys.argv else 25
host=urllib.parse.urlparse(start).netloc.replace('www.','')
UA={'User-Agent':'Mozilla/5.0 (compatible; BerawaReader/1.0)'}
def get(u):
    r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30); b=r.read()
    return r.geturl(),b.decode(r.headers.get_content_charset() or 'utf-8','ignore')
def text(h):
    h=re.sub(r'<(script|style|noscript|svg)\b.*?</\1>','',h,flags=re.S|re.I); h=re.sub(r'<!--.*?-->','',h,flags=re.S)
    h=re.sub(r'<(br|/p|/div|/li|/h\d|/tr|/section)\b[^>]*>',' ',h,flags=re.I)
    # el texto de los enlaces mailto:/tel: tambien cuenta (el correo suele estar solo en el href)
    h=re.sub(r'<a\b[^>]*href="(?:mailto|tel):([^"?]+)[^"]*"[^>]*>',lambda m:' '+m.group(1)+' ',h,flags=re.I)
    return re.sub(r'\s+',' ',H.unescape(re.sub(r'<[^>]+>',' ',h))).strip()
seen={};queue=[start]
while queue and len(seen)<mx:
    u=queue.pop(0)
    try: fu,h=get(u)
    except Exception as e: print('ERR',u,e); continue
    fu=fu.split('#')[0]
    if fu in seen: continue
    seen[fu]=text(h)
    for l in re.findall(r'href="([^"#]+)"',h):
        a=urllib.parse.urljoin(fu,H.unescape(l)).split('#')[0]
        p=urllib.parse.urlparse(a)
        if p.netloc.replace('www.','')==host and p.scheme in('http','https') and not re.search(r'\.(jpg|jpeg|png|webp|pdf|zip|svg|css|js|ico|xml)(\?|$)',a,re.I) and a not in seen and a not in queue and not re.search(r'(wp-json|feed|xmlrpc|/tag/|/category/|\?replytocom)',a): queue.append(a)
SOURCE_TEXT.parent.mkdir(parents=True,exist_ok=True)
json.dump(seen,open(SOURCE_TEXT,'w'),ensure_ascii=False,indent=1)
print(len(seen),'paginas guardadas en',SOURCE_TEXT)
for u,t in seen.items(): print(len(t),u)
