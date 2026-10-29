#!/usr/bin/env python3
"""Ilustraciones propias de Berawa (generadas por codigo, sin fotos ni logos de nadie). Determinista: misma semilla = mismos bytes.
Uso desde el repo: python3 berawa/build/make_art.py [--out DIR]   (lee ART de content_<slug>.py)
Cada imagen: abstracta/geometrica, con una paleta propia del negocio; no representa el establecimiento (se rotula «Imagen ilustrativa»)."""
import sys,math,random,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
W,H=1600,1067
def hx(c): c=c.lstrip('#'); return tuple(int(c[i:i+2],16) for i in (0,2,4))
def mix(a,b,t): return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def vgrad(top,bot):
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H): d.line([(0,y),(W,y)],fill=mix(top,bot,y/(H-1)))
    return im
def ridge(rng,base,amp,k):
    ph=[rng.uniform(0,6.28) for _ in range(3)]; fr=[rng.uniform(0.6,1.2)*k,rng.uniform(1.8,2.6)*k,rng.uniform(3.5,5)*k]
    return [base+amp*(math.sin(x/W*6.283*fr[0]+ph[0])+0.5*math.sin(x/W*6.283*fr[1]+ph[1])+0.25*math.sin(x/W*6.283*fr[2]+ph[2])) for x in range(W+1)]
def hills(rng,pal):
    im=vgrad(hx(pal[0]),hx(pal[1])); d=ImageDraw.Draw(im)
    sx,sy=rng.randint(400,1200),rng.randint(220,420); r=rng.randint(90,150)
    d.ellipse([sx-r,sy-r,sx+r,sy+r],fill=hx(pal[2]))
    for i,c in enumerate(pal[3:]):
        ys=ridge(rng,560+i*130,40+i*10,1+i*0.3); d.polygon([(x,ys[x]) for x in range(W+1)]+[(W,H),(0,H)],fill=hx(c))
    return im
def skyline(rng,pal):
    im=vgrad(hx(pal[0]),hx(pal[1])); d=ImageDraw.Draw(im)
    sx,sy=rng.randint(300,1300),rng.randint(200,380); r=rng.randint(70,110); d.ellipse([sx-r,sy-r,sx+r,sy+r],fill=hx(pal[2]))
    for i,c in enumerate(pal[3:]):
        x=-40
        while x<W:
            w=rng.randint(70,170); h=rng.randint(180,520)-i*60; top=H-h-i*40
            d.rectangle([x,top,x+w,H],fill=hx(c))
            for wx in range(x+14,x+w-18,34):
                for wy in range(top+18,H-30,46):
                    if rng.random()<0.35: d.rectangle([wx,wy,wx+14,wy+22],fill=mix(hx(c),hx(pal[2]),0.55))
            x+=w+rng.randint(0,18)
    return im
def columns(rng,pal):
    im=vgrad(hx(pal[0]),hx(pal[1])); d=ImageDraw.Draw(im)
    n=rng.randint(5,7); gap=W/(n+1)
    d.rectangle([0,150,W,200],fill=hx(pal[3])); d.polygon([(0,150),(W/2,40),(W,150)],fill=hx(pal[2]))
    for i in range(n):
        cx=gap*(i+1); cw=gap*0.34
        d.rectangle([cx-cw/2,200,cx+cw/2,H-120],fill=hx(pal[3]))
        for s in range(-2,3): d.line([(cx+s*cw/6,210),(cx+s*cw/6,H-130)],fill=mix(hx(pal[3]),hx(pal[1]),0.35),width=4)
        d.rectangle([cx-cw*0.7,H-120,cx+cw*0.7,H-90],fill=hx(pal[4] if len(pal)>4 else pal[3]))
    d.rectangle([0,H-90,W,H],fill=hx(pal[4] if len(pal)>4 else pal[3]))
    return im
def waves(rng,pal):
    im=vgrad(hx(pal[0]),hx(pal[1])); d=ImageDraw.Draw(im)
    sx,sy=rng.randint(400,1200),rng.randint(220,380); r=rng.randint(80,130); d.ellipse([sx-r,sy-r,sx+r,sy+r],fill=hx(pal[2]))
    for i,c in enumerate(pal[3:]):
        ys=ridge(rng,520+i*120,26+i*8,1.6+i*0.4); d.polygon([(x,ys[x]) for x in range(W+1)]+[(W,H),(0,H)],fill=hx(c))
    return im
def arches(rng,pal):
    im=vgrad(hx(pal[0]),hx(pal[1])); d=ImageDraw.Draw(im)
    n=rng.randint(3,4); aw=W/n
    for i in range(n):
        x0=i*aw+40; x1=(i+1)*aw-40; top=180+rng.randint(0,40)
        d.rectangle([x0-30,top,x1+30,H],fill=hx(pal[3]))
        d.ellipse([x0,top+10,x1,top+10+(x1-x0)],fill=hx(pal[0]))
        d.rectangle([x0,top+10+(x1-x0)/2,x1,H],fill=hx(pal[0]))
        d.ellipse([x0+60,top+90,x0+60+90,top+180],fill=hx(pal[2]))
    d.rectangle([0,H-70,W,H],fill=hx(pal[4] if len(pal)>4 else pal[3]))
    return im
ALT_KIND={
'hills':dict(es='Ilustración geométrica de colinas bajo un sol',ca='Il·lustració geomètrica de turons sota un sol',en='Geometric illustration of hills under a sun',fr='Illustration géométrique de collines sous un soleil'),
'skyline':dict(es='Ilustración geométrica de edificios al atardecer',ca='Il·lustració geomètrica d\'edificis a la posta de sol',en='Geometric illustration of buildings at dusk',fr='Illustration géométrique d\'immeubles au crépuscule'),
'columns':dict(es='Ilustración geométrica de una fachada con columnas',ca='Il·lustració geomètrica d\'una façana amb columnes',en='Geometric illustration of a facade with columns',fr='Illustration géométrique d\'une façade à colonnes'),
'waves':dict(es='Ilustración geométrica de olas y un sol',ca='Il·lustració geomètrica d\'ones i un sol',en='Geometric illustration of waves and a sun',fr='Illustration géométrique de vagues et d\'un soleil'),
'arches':dict(es='Ilustración geométrica de arcos de una arcada',ca='Il·lustració geomètrica d\'arcs d\'una arcada',en='Geometric illustration of arches in an arcade',fr='Illustration géométrique d\'arcs d\'une arcade')}
def alts_from_art(art,langs=('es','ca','en','fr')):
    return {l:{n:ALT_KIND[v[0]][l] for n,v in art.items()} for l in langs}
KINDS=dict(hills=hills,skyline=skyline,columns=columns,waves=waves,arches=arches)
def render(kind,seed,pal):
    rng=random.Random(seed); im=KINDS[kind](rng,pal)
    return im.filter(ImageFilter.GaussianBlur(0.6))
def save(im,out,name,q=72):
    Path(out,'img').mkdir(parents=True,exist_ok=True)
    im.save(f'{out}/img/{name}.webp','WEBP',quality=q,method=6)
    s=im.resize((800,round(800*im.height/im.width)),Image.LANCZOS); s.save(f'{out}/img/{name}-m.webp','WEBP',quality=q-4,method=6)
def main(out):
    from content_villa_alicia_guesthouse_malaga import ART
    for name,(kind,seed,pal) in ART.items(): save(render(kind,seed,pal),out,name)
    print(len(ART),'ilustraciones ->',out)
if __name__=='__main__':
    a=[x for x in sys.argv[1:] if not x.startswith('--out=')]; o=[x[6:] for x in sys.argv[1:] if x.startswith('--out=')]
    from _rutas import ROOT
    main(o[0] if o else str(ROOT))
