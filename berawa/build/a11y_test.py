"""axe-core + teclado. Uso: a11y_test.py URL salida.json"""
import sys,json
from _rutas import axe_js,axe_version,lanzar_navegador
from playwright.sync_api import sync_playwright
url,outf=sys.argv[1],sys.argv[2]
from knowledge_villa_alicia_guesthouse_malaga import KB
_e=[e for e in KB['entries'] if e['topic']=='mascotas'] or KB['entries'][:1]
PREG=_e[0]['keys']['es'][0].strip();RESP=_e[0]['a']['es'][:40]   # pregunta y respuesta esperada para la prueba de teclado (de la base de conocimiento)
AXE=axe_js()
ver=axe_version()
TAGS=['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']
res=dict(axe_version=ver,tags=TAGS,url=url,runs=[],keyboard=[],fail=[])
def axe(pg,label):
    pg.evaluate("axe_src=1") if False else None
    pg.add_script_tag(content=AXE) if not pg.evaluate("typeof axe!=='undefined'") else None
    r=pg.evaluate("async tags=>await axe.run(document,{runOnly:{type:'tag',values:tags}})",TAGS)
    v=[dict(id=x['id'],impact=x['impact'],n=len(x['nodes']),sel=[n['target'] for n in x['nodes'][:3]],help=x['help']) for x in r['violations']]
    inc=[dict(id=x['id'],n=len(x['nodes'])) for x in r['incomplete']]
    res['runs'].append(dict(estado=label,violaciones=v,incompletas=inc,pasan=len(r['passes'])))
    for x in v: res['fail'].append(f"{label}: {x['id']} ({x['impact']}) x{x['n']}")
with sync_playwright() as p:
    b=lanzar_navegador(p)
    for vp,(w,h) in dict(desktop=(1280,900),movil=(375,800)).items():
        for l in ['es','ca','en','fr']:
            ctx=b.new_context(viewport=dict(width=w,height=h),locale=l,bypass_csp=True);pg=ctx.new_page()
            pg.goto(f'{url}?lang={l}',wait_until='load');pg.wait_for_timeout(300)
            pg.evaluate("window.scrollTo(0,document.body.scrollHeight)");pg.wait_for_timeout(200);pg.evaluate("window.scrollTo(0,0)")
            axe(pg,f'{vp}/{l}/inicio')
            if vp=='movil' and pg.query_selector('#menub') and pg.is_visible('#menub'):
                pg.click('#menub');pg.wait_for_timeout(200);axe(pg,f'{vp}/{l}/menu-abierto');pg.keyboard.press('Escape')
            pg.click('#chatb');pg.fill('#q','¿Cuánto cuesta?');pg.press('#q','Enter');pg.wait_for_timeout(500)
            axe(pg,f'{vp}/{l}/chat-abierto')
            ctx.close()
    # teclado
    for vp,(w,h) in dict(desktop=(1280,900),movil=(375,800)).items():
        ctx=b.new_context(viewport=dict(width=w,height=h),bypass_csp=True);pg=ctx.new_page();pg.goto(url+'?lang=es',wait_until='load');pg.wait_for_timeout(300)
        stops=[]
        for i in range(60):
            pg.keyboard.press('Tab')
            s=pg.evaluate("""()=>{const e=document.activeElement;if(!e||e===document.body)return null;const cs=getComputedStyle(e);
              const nm=e.getAttribute('aria-label')||e.textContent.trim()||e.alt||e.placeholder||'';
              const r=e.getBoundingClientRect();
              return {tag:e.tagName.toLowerCase(),id:e.id,name:nm.slice(0,40),outline:cs.outlineStyle+' '+cs.outlineWidth,shadow:cs.boxShadow!=='none',vis:r.width>0&&r.height>0&&cs.visibility!=='hidden'}}""")
            if s is None: break
            stops.append(s)
            if len(stops)>3 and stops[-1]==stops[0] : break
        sin_nombre=[s for s in stops if not s['name']]
        sin_foco=[s for s in stops if s['vis'] and s['outline'].startswith('none') and not s['shadow']]
        ocultos=[s for s in stops if not s['vis']]
        k=dict(viewport=vp,paradas=len(stops),sin_nombre=sin_nombre,sin_foco_visible=sin_foco,enfocables_ocultos=ocultos,primeras=[(s['tag'],s['name']) for s in stops[:8]])
        # teclado en chat
        pg.focus('#chatb');pg.keyboard.press('Enter');pg.wait_for_timeout(200)
        k['chat_abre_con_enter']=pg.evaluate("document.querySelector('#chat').classList.contains('o')")
        k['foco_en_input']=pg.evaluate("document.activeElement.id")=='q'
        pg.keyboard.type(PREG);pg.keyboard.press('Enter');pg.wait_for_timeout(400)
        k['chat_responde_con_teclado']=pg.evaluate("[...document.querySelectorAll('#msgs .m.b')].pop().textContent").startswith(RESP)
        pg.keyboard.press('Escape');pg.wait_for_timeout(150)
        k['esc_cierra_chat']=not pg.evaluate("document.querySelector('#chat').classList.contains('o')");k['foco_vuelve_a_boton']=pg.evaluate("document.activeElement.id")=='chatb'
        # selector de idioma con teclado
        pg.focus('.langs button[data-l=fr]');pg.keyboard.press('Enter');pg.wait_for_timeout(200)
        k['idioma_con_teclado']=pg.evaluate("document.documentElement.lang")=='fr'
        if vp=='movil':
            pg.focus('#menub') if pg.query_selector('#menub') else None
            if pg.query_selector('#menub'):
                pg.keyboard.press('Enter');pg.wait_for_timeout(150);k['menu_abre']=pg.evaluate("document.querySelector('#nav').classList.contains('o')");pg.keyboard.press('Escape');pg.wait_for_timeout(100)
                k['menu_esc_cierra']=not pg.evaluate("document.querySelector('#nav').classList.contains('o')")
        res['keyboard'].append(k)
        for key in ['sin_nombre','sin_foco_visible','enfocables_ocultos']:
            if k[key]: res['fail'].append(f"teclado {vp}: {key} {[(x['tag'],x['name']) for x in k[key]][:4]}")
        for key in ['chat_abre_con_enter','foco_en_input','chat_responde_con_teclado','esc_cierra_chat','foco_vuelve_a_boton','idioma_con_teclado','menu_abre','menu_esc_cierra']:
            if key in k and not k[key]: res['fail'].append(f'teclado {vp}: {key}=False')
        ctx.close()
    b.close()
res['ok']=not res['fail']
json.dump(res,open(outf,'w'),ensure_ascii=False,indent=1)
print('OK' if res['ok'] else 'FALLOS');print('\n'.join(res['fail'][:25]))
