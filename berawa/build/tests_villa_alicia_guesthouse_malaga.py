"""Pruebas funcionales de la demo: i18n 4 idiomas + chatbot (sin red externa). Uso: tests_villa_alicia_guesthouse_malaga.py URL salida.json [--kb]"""
import sys,json,re
from _rutas import lanzar_navegador
from playwright.sync_api import sync_playwright
url,outf=sys.argv[1],sys.argv[2];KB='--kb' in sys.argv
from knowledge_villa_alicia_guesthouse_malaga import KB as K
ENT={e['id']:e for e in K['entries']}
from content_villa_alicia_guesthouse_malaga import QS as Q   # (pregunta, id esperado o None=desconocida) por idioma
res=dict(url=url,langs={},fail=[])
def chk(c,msg):
    if not c: res['fail'].append(msg)
with sync_playwright() as p:
    b=lanzar_navegador(p)
    pg=b.new_page(viewport=dict(width=1280,height=900))
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
    reqs=[];pg.on('request',lambda r:reqs.append(r.url))
    for l in ['es','ca','en','fr']:
        pg.goto(url+('?lang='+l),wait_until='load');pg.wait_for_timeout(400)
        D=pg.evaluate("D")['i18n'] if pg.evaluate("typeof D!=='undefined'") else None
        lang=pg.evaluate("document.documentElement.lang");chk(lang==l,f'{l}: html lang={lang}')
        bad=pg.evaluate("[...document.querySelectorAll('[data-t]')].filter(e=>{const t=D.i18n[document.documentElement.lang][e.dataset.t];return t!==undefined&&e.textContent!==t}).map(e=>e.dataset.t)") if D else []
        chk(not bad,f'{l}: data-t sin aplicar {bad}')
        body=pg.inner_text('body')
        for w in ['Deutsch','Sprache','Unterkunft','Buchen','Ausstattung']: chk(w not in body,f'{l}: texto alemán "{w}"')
        btns=pg.evaluate("[...document.querySelectorAll('.langs button')].map(b=>b.dataset.l)");chk(btns==['es','ca','en','fr'],f'{l}: botones idioma {btns}')
        same=[]
        if D:
            for k,v in D[l].items():
                if l!='es' and isinstance(v,str) and v==D['es'].get(k): same.append(k)
        pg.click('#chatb');pg.wait_for_timeout(200)
        chat=[]
        for q,eid in Q[l]:
            pg.fill('#q',q);pg.press('#q','Enter');pg.wait_for_timeout(450)
            last=pg.evaluate("[...document.querySelectorAll('#msgs .m.b')].pop().textContent")
            if not KB:
                ok=(last==D[l]['chat_fb']) if not eid else True
                if eid=='K10': ok='Adentro' in last
                elif eid=='K04' or eid=='K08': ok='WhatsApp' in last or 'wa.me' in last
                elif eid: ok=True
            elif eid:
                exp=ENT[eid]['a'][l];ok=last.startswith(exp)
            else:
                fb=D[l]['chat_fb'];ok=last==fb
            chat.append(dict(q=q,esperado=eid or 'DESCONOCIDA',ok=ok,respuesta=last[:140]))
            chk(ok,f'{l}: chat "{q}" esperado {eid or "desconocida"} -> {last[:80]}')
        chips=pg.evaluate("[...document.querySelectorAll('#qs button')].map(b=>b.textContent)")
        for c in chips:
            if not KB and False: continue
            pg.fill('#q',c);pg.press('#q','Enter');pg.wait_for_timeout(350)
            last=pg.evaluate("[...document.querySelectorAll('#msgs .m.b')].pop().textContent");chk(last!=D[l]['chat_fb'],f'{l}: chip "{c}" sin respuesta')
        res['langs'][l]=dict(textos_iguales_al_es=same,chat=chat,chips=chips)
    ext=[u for u in reqs if not u.startswith(url.split('/',3)[0]+'//'+url.split('/')[2]) and not u.startswith('data:')]
    chk(not ext,f'peticiones externas {ext}');chk(not errs,f'errores consola {errs}')
    b.close()
res['ok']=not res['fail']
json.dump(res,open(outf,'w'),ensure_ascii=False,indent=1)
print('OK' if res['ok'] else 'FALLOS',res['fail'][:12])
