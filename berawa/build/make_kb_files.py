"""Escribe berawa/knowledge.json y berawa/sources.json a partir de knowledge_<slug>.py y del texto fuente guardado en el repo
(berawa/evidence/source-text.json, creado por fetch_sources.py en la primera lectura)."""
import json,hashlib
from _rutas import ROOT,SOURCE_TEXT
from knowledge_villa_alicia_guesthouse_malaga import KB
from content_villa_alicia_guesthouse_malaga import META
pages=json.load(open(SOURCE_TEXT,encoding='utf-8'))
used=sorted({s['url'] for e in KB['entries'] for s in e['sources']})
R=str(ROOT/'berawa')
json.dump(KB,open(R+'/knowledge.json','w'),ensure_ascii=False,indent=1)
src=dict(schema='berawa-sources/1',site=META['url'],read_at=META['read_at'],
 method='Texto visible de cada pagina leido de la web publica del negocio en la fecha indicada (fetch_sources.py) y guardado en berawa/evidence/source-text.json; las citas del chatbot se comprueban contra ese texto con check_kb.py.',
 pages=[dict(url=u,sha256=hashlib.sha256(pages[u].encode()).hexdigest(),chars=len(pages[u])) for u in used],
 other_pages_read=sorted(set(pages)-set(used)))
json.dump(src,open(R+'/sources.json','w'),ensure_ascii=False,indent=1)
print(len(used),'paginas fuente usadas de',len(pages))
