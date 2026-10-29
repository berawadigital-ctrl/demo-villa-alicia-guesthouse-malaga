"""Revisión estática + prueba de que la CSP por meta se aplica. Uso: sec_scan.py DIR URL salida.json"""
import sys,re,json,os
from _rutas import lanzar_navegador
from playwright.sync_api import sync_playwright
d,url,outf=sys.argv[1:4]
H=open(d+'/index.html').read();JS=open(d+'/app.js').read() if os.path.exists(d+'/app.js') else ''
res=dict(checks={},fail=[])
def c(name,ok,detail=''):
    res['checks'][name]=dict(ok=bool(ok),detalle=detail)
    if not ok: res['fail'].append(name)
c('S01 sin <script> inline',not re.findall(r'<script(?![^>]*\ssrc=)[^>]*>',H))
c('S02 sin <style> ni style="" inline',not re.search(r'<style|\sstyle=',H))
c('S03 sin manejadores on*=',not re.search(r'\son[a-z]+=',H))
c('S04 sin innerHTML/outerHTML/insertAdjacentHTML/document.write/eval/new Function',not re.search(r'innerHTML|outerHTML|insertAdjacentHTML|document\.write|eval\(|new Function',JS+H),'revisado app.js + index.html')
bl=re.findall(r'<a [^>]*target="_blank"[^>]*>',H);bad=[a for a in bl if not ('noopener' in a and 'noreferrer' in a)]
c('S05 todo target=_blank con rel="noopener noreferrer" (HTML)',bl and not bad,f'{len(bl)} enlaces')
c('S05b target=_blank creados por JS con rel noopener noreferrer',"a.rel='noopener noreferrer'" in JS and "a.target='_blank'" in JS)
ext=set(re.findall(r'(?:src|href)="(https?://[^"/]+)',H))|set(re.findall(r'https?://[^/\'"]+',JS))
c('S06 sin scripts, CSS, fuentes ni imágenes de terceros',not re.search(r'<script[^>]+src="https?:|<link[^>]+href="https?:|<img[^>]+src="https?:',H),f'dominios enlazados (solo enlaces de salida): {sorted(ext)}')
m=re.search(r'Content-Security-Policy" content="([^"]+)"',H);csp=m.group(1) if m else ''
c('S07 CSP por meta presente',bool(csp))
c("S08 CSP sin 'unsafe-inline', 'unsafe-eval' ni comodines",csp and not re.search(r"unsafe-|\*|http:",csp),csp)
c('S09 referrer no-referrer','name="referrer" content="no-referrer"' in H)
c('S10 sin secretos/claves/tokens en el código',not re.search(r'(?i)api[_-]?key|secret|token|password|sk_live|AIza[0-9A-Za-z_-]{20}',H+JS))
res['url_externas_en_js']=sorted(set(re.findall(r'https?://[^/\'"]+',JS)))
# CSP efectiva en el navegador
with sync_playwright() as p:
    b=lanzar_navegador(p);pg=b.new_page()
    pg.add_init_script("window.__v=[];document.addEventListener('securitypolicyviolation',e=>window.__v.push(e.violatedDirective))")
    pg.goto(url,wait_until='load');pg.wait_for_timeout(300)
    pg.evaluate("()=>{const s=document.createElement('script');s.textContent='window.__x=1';document.body.appendChild(s);const i=document.createElement('img');i.src='https://example.invalid/x.png';document.body.appendChild(i);const e=document.createElement('div');e.setAttribute('style','color:red');document.body.appendChild(e);try{fetch('https://example.invalid/')}catch(e){}}")
    pg.wait_for_timeout(500)
    v=pg.evaluate("window.__v");x=pg.evaluate("window.__x===1")
    c('S11 la CSP bloquea script inline inyectado',not x,f'violaciones registradas: {sorted(set(v))}')
    c('S12 la CSP bloquea imagen/fetch externos',any(s.startswith('img-src') for s in v) and any(s.startswith('connect-src') for s in v))
    # inyección en el chat: lo que escribe el usuario se muestra como texto
    pg.click('#chatb');pg.fill('#q','<img src=x onerror=window.__x=1><b>hola</b>');pg.press('#q','Enter');pg.wait_for_timeout(500)
    u=pg.evaluate("[...document.querySelectorAll('#msgs .m.u')].pop().innerHTML")
    c('S13 el texto escrito en el chat no se interpreta como HTML',('&lt;img' in u) and not pg.evaluate("!!document.querySelector('#msgs img,#msgs b')"),u[:90])
    b.close()
res['ok']=not res['fail']
json.dump(res,open(outf,'w'),ensure_ascii=False,indent=1)
print('OK' if res['ok'] else 'FALLOS',res['fail'])
