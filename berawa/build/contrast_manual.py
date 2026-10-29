"""Contraste de los nodos que axe marca como 'incompletos' (texto sobre imagen): se muestrea el fondo real con el texto oculto."""
import sys,json,io
from _rutas import axe_js,lanzar_navegador
from playwright.sync_api import sync_playwright
from PIL import Image
url,outf=sys.argv[1],sys.argv[2]
AXE=axe_js()
def lum(c):
    f=lambda v:(v/255/12.92) if v/255<=0.03928 else (((v/255+0.055)/1.055)**2.4)
    return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])
def cr(a,b):
    la,lb=lum(a),lum(b);return (max(la,lb)+0.05)/(min(la,lb)+0.05)
res=[];fails=[]
with sync_playwright() as p:
    b=lanzar_navegador(p)
    for vp,(w,h) in dict(desktop=(1280,900),movil=(375,800)).items():
      for l in ['es','ca','en','fr']:
        pg=b.new_context(viewport=dict(width=w,height=h),bypass_csp=True).new_page();pg.goto(f'{url}?lang={l}',wait_until='load');pg.wait_for_timeout(300)
        pg.add_script_tag(content=AXE)
        r=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'rule',values:['color-contrast']}});return r.incomplete.flatMap(x=>x.nodes.map(n=>n.target[0]))}")
        for sel in sorted(set(r)):
            els=pg.query_selector_all(sel)
            for el in els[:3]:
                el.scroll_into_view_if_needed();pg.wait_for_timeout(120)
                info=pg.evaluate("""e=>{const cs=getComputedStyle(e);return {color:cs.color,size:parseFloat(cs.fontSize),weight:cs.fontWeight,op:cs.opacity,bg:cs.backgroundColor}}""",el)
                box=el.bounding_box()
                if not box or box['width']<2: continue
                pg.evaluate("e=>{e.dataset.oc=e.style.color;e.style.setProperty('color','transparent','important');e.querySelectorAll('*').forEach(c=>c.style.setProperty('color','transparent','important'))}",el)
                png=pg.screenshot(clip=dict(x=max(box['x'],0),y=max(box['y'],0),width=min(box['width'],w),height=min(box['height'],h)))
                pg.evaluate("e=>{e.style.removeProperty('color');e.querySelectorAll('*').forEach(c=>c.style.removeProperty('color'))}",el)
                im=Image.open(io.BytesIO(png)).convert('RGB');px=list(im.getdata())
                import re
                m=[int(x) for x in re.findall(r'[\d.]+',info['color'])[:3]]
                # peor caso: el 5% de píxeles de fondo con menor contraste
                bgm=re.findall(r'[\d.]+',info['bg']);ownbg=len(bgm)==3 or (len(bgm)==4 and float(bgm[3])>0.95)
                cs=[cr(m,[int(float(x)) for x in bgm[:3]])] if ownbg else sorted(cr(m,q) for q in px[::max(1,len(px)//600)]);worst=cs[0] if ownbg else cs[int(len(cs)*0.08)]
                large=info['size']>=24 or (info['size']>=18.66 and int(info['weight'])>=700)
                need=3 if large else 4.5
                ok=worst>=need
                res.append(dict(vp=vp,l=l,sel=sel,color=info['color'],size=info['size'],peor_contraste=round(worst,2),minimo=need,ok=ok))
                if not ok: fails.append(res[-1])
        pg.close()
    b.close()
json.dump(dict(total=len(res),fallos=fails,detalle=res),open(outf,'w'),ensure_ascii=False,indent=1)
print(len(res),'nodos medidos;',len(fails),'por debajo del mínimo')
for f in fails[:15]: print(f)
