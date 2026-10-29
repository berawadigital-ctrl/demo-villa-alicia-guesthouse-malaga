#!/usr/bin/env python3
"""Comprobación de berawa/knowledge.json (chatbot de las demos).
  1) CITAS: cada fuente (URL + cita literal) está en la página guardada; cada cifra de la respuesta aparece en alguna fuente.   [K04]
  2) PRECIOS (regla de Juan 28/10/2026, 10:28): todo precio lleva su fuente con fecha y «confírmalo al reservar» en los 4 idiomas. [P1–P6]
Uso (desde cualquier carpeta; todo se resuelve desde la raíz del repositorio, sin rutas absolutas):
      python3 berawa/build/check_kb.py                      → berawa/knowledge.json + texto fuente guardado en berawa/evidence/source-text.json
                                                              (y comprueba que knowledge.json coincide con knowledge_villa_alicia_guesthouse_malaga.py)
      python3 berawa/build/check_kb.py --kb ruta/knowledge.json [--text ruta/text.txt|ruta/source-text.json] [--solo-precios]
Sale con código 1 si hay cualquier fallo."""
import re,json,sys,unicodedata,datetime,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from _rutas import ROOT,SOURCE_TEXT
LANGS=('es','ca','en','fr')
# Frases canónicas de la regla (comparación sin acentos, sin mayúsculas, espacios normalizados)
CONFIRMA={'es':'confírmalo al reservar','ca':'confirma-ho en reservar','en':'confirm it when you book','fr':'confirmez-le lors de la réservation'}
def norm(x): return re.sub(r'\s+',' ',unicodedata.normalize('NFD',(x or '').lower()).encode('ascii','ignore').decode()).strip()
NUM=r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)'
MON=r'(?:€|eur\b|euros?\b)'
PRICE_RE=[re.compile(NUM+r'\s*(?:(?:a|à|to|-|–)\s*'+NUM+r'\s*)?'+MON,re.I),re.compile(r'(?:€|eur\b)\s*'+NUM+r'(?:\s*(?:to|-|–)\s*'+NUM+r')?',re.I)]
def num(s):
    s=s.strip()
    if re.fullmatch(r'\d{1,3}(?:[.,]\d{3})+',s): return str(int(re.sub(r'\D','',s)))
    v=float(s.replace(',','.')); return str(int(v)) if v==int(v) else str(v)
def precios(texto):
    """Cifras de precio que aparecen en el texto (normalizadas)."""
    out=set()
    for rx in PRICE_RE:
        for m in rx.finditer(texto or ''):
            for g in m.groups():
                if g: out.add(num(g))
    return out
def fecha_iso_a_es(iso):
    try: d=datetime.datetime.fromisoformat(iso.replace('Z','+00:00')); return d.strftime('%d/%m/%Y')
    except Exception: return None
DATE_RE=re.compile(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b')
def fechas_en(texto): return {f'{int(d):02d}/{int(m):02d}/{y}' for d,m,y in DATE_RE.findall(texto or '')}

def check_prices(kb):
    """Devuelve lista de (id_entrada, código, mensaje). Vacía = cumple la regla."""
    err=[]; kb_fecha=fecha_iso_a_es(kb.get('source_read_at',''))
    for e in kb['entries']:
        eid=e['id']; a=e['a']
        por_lang={l:precios(a.get(l,'')) for l in LANGS}
        if not any(por_lang.values()): continue                       # entrada sin precios: la regla no aplica
        # P1 los 4 idiomas presentes y con los mismos precios
        for l in LANGS:
            if not a.get(l): err.append((eid,'P1',f'falta la respuesta en {l}'))
        base=por_lang['es']
        for l in LANGS:
            if por_lang[l]!=base: err.append((eid,'P1',f'los precios de {l} {sorted(por_lang[l],key=float)} no coinciden con es {sorted(base,key=float)}'))
        # P2 fuente con URL y cita literal (no vale una cita de ausencia '!')
        reales=[s for s in e.get('sources',[]) if s.get('url') and s.get('quote') and not s['quote'].startswith('!')]
        if not reales: err.append((eid,'P2','precio sin fuente con URL y cita literal'))
        # P3 cada cifra de precio sale de alguna cita de la entrada
        citas=' '.join(s['quote'] for s in reales)
        en_citas=set(re.findall(r'\d+(?:[.,]\d+)?',citas)); en_citas={num(x) for x in en_citas}
        for n in sorted(base,key=float):
            if n not in en_citas: err.append((eid,'P3',f'el precio {n} no aparece en ninguna cita de sus fuentes'))
        # P4 fecha de la fuente: en la base (source_read_at) o en la fuente (fecha) y visible en la respuesta
        fechas=set()
        for s in reales:
            f=fecha_iso_a_es(s.get('fecha','')) if s.get('fecha') else None
            if f: fechas.add(f)
        if kb_fecha: fechas.add(kb_fecha)
        if not fechas: err.append((eid,'P4','sin fecha de lectura de la fuente (source_read_at o fuente.fecha)'))
        for l in LANGS:
            vis=fechas_en(a.get(l,''))
            if not vis: err.append((eid,'P4',f'la respuesta en {l} no muestra la fecha de la fuente (DD/MM/AAAA)'))
            elif fechas and not (vis&fechas): err.append((eid,'P4',f'la fecha de la respuesta en {l} {sorted(vis)} no coincide con la lectura {sorted(fechas)}'))
        # P5 frase canónica en cada idioma
        for l in LANGS:
            if norm(CONFIRMA[l]) not in norm(a.get(l,'')): err.append((eid,'P5',f'falta «{CONFIRMA[l]}» en {l}'))
        # P6 el precio se presenta como publicado por la web (no como propio): marca «web/site» en cada idioma
        for l,w in (('es','su web'),('ca','seva web'),('en','website'),('fr','leur site')):
            if w not in norm(a.get(l,'')): err.append((eid,'P6',f'la respuesta en {l} no atribuye el precio a la web del negocio («{w}»)'))
    return err

def load_pages(path):
    """Acepta el JSON del repo {url: texto} o un text.txt crudo con bloques «===== URL | titulo»."""
    t=open(path,encoding='utf-8').read(); pages={}
    if str(path).endswith('.json'):
        return {u:' '+re.sub(r'\s+',' ',x) for u,x in json.loads(t).items()}
    for b in re.split(r'\n(?====== https)',t):
        m=re.match(r'===== (\S+) \|',b)
        if m: pages[m.group(1)]=pages.get(m.group(1),'')+' '+re.sub(r'\s+',' ',b)
    return pages
def check_quotes(kb,pages):
    bad=0
    for e in kb['entries']:
        for s in e['sources']:
            p=pages.get(s['url'])
            if p is None: print('SIN PAGINA',e['id'],s['url']);bad+=1;continue
            q=s['quote']
            if q.startswith('!'):
                if q[1:] in p: print('AUSENCIA FALSA',e['id'],s['url'],q);bad+=1
                continue
            if re.sub(r'\s+',' ',s['quote']) not in p: print('CITA NO ENCONTRADA',e['id'],s['url'],'|',s['quote'][:70]);bad+=1
    for e in kb['entries']:
        src=' '.join(pages[s['url']] for s in e['sources'] if s['url'] in pages)
        for l,a in e['a'].items():
            for n in set(re.findall(r'\d+',DATE_RE.sub('',a))):
                if n not in src and n not in ('8',): print('CIFRA SIN FUENTE',e['id'],l,n); bad+=1
    return bad

def main(argv):
    arg=lambda k:(argv[argv.index(k)+1] if k in argv else None)
    kbpath=arg('--kb') or str(ROOT/'berawa'/'knowledge.json')
    kb=json.load(open(kbpath,encoding='utf-8'))
    bad=0
    if '--solo-precios' not in argv:
        pages=load_pages(arg('--text') or SOURCE_TEXT)
        bad+=check_quotes(kb,pages); print('entradas',len(kb['entries']),'fallos de citas/cifras',bad)
    if not arg('--kb') and '--solo-precios' not in argv:   # el entregable debe coincidir con el generador
        from knowledge_villa_alicia_guesthouse_malaga import KB as KBGEN
        if json.loads(json.dumps(KBGEN))!=kb: print('knowledge.json NO coincide con knowledge_villa_alicia_guesthouse_malaga.py'); bad+=1
        else: print('knowledge.json coincide con knowledge_villa_alicia_guesthouse_malaga.py')
    pe=check_prices(kb)
    for eid,c,m in pe: print('PRECIO',eid,c,m)
    print('REGLA DE PRECIOS:','CUMPLE' if not pe else f'{len(pe)} FALLOS en {len({x[0] for x in pe})} entradas')
    return 1 if (bad or pe) else 0
if __name__=='__main__': sys.exit(main(sys.argv[1:]))
