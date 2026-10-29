import sys,json
from _rutas import lanzar_navegador
from playwright.sync_api import sync_playwright
from knowledge_villa_alicia_guesthouse_malaga import KB
JS="""([l,q])=>{L=l;const n=norm(q),t=D.i18n[l];let best=null,sc=0;t.faq.forEach((f,i)=>{let s=0;f.k.forEach(k=>{if(n.includes(nk(k)))s+=k.trim().length});if(s>sc){sc=s;best=i}});return best}"""
bad=[];tot=0
with sync_playwright() as p:
    b=lanzar_navegador(p);pg=b.new_page()
    pg.goto(sys.argv[1]);pg.wait_for_timeout(300)
    for i,e in enumerate(KB['entries']):
        for l,ks in e['keys'].items():
            for k in ks:
                q=k.strip()
                r=pg.evaluate(JS,[l,'¿'+q+'?']);tot+=1
                if r!=i: bad.append((e['id'],l,k,None if r is None else KB['entries'][r]['id']))
    b.close()
print(tot,'claves;',len(bad),'ambiguas/fallidas');
for x in bad: print(x)
