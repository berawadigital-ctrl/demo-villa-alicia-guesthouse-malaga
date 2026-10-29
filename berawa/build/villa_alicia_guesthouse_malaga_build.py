"""Generador de la demo villa_alicia_guesthouse_malaga (adaptado del modelo aprobado: mismo generador, contenido propio). Etapas acumulativas: kb, a11y, sec, v1."""
import sys,json,html,os,re,shutil,urllib.parse as up
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'vendor','webfactory'))   # copia de la plantilla base (webfactory) incluida en el repo
import build as B
LANGS=['es','ca','en','fr']
DEMO={'es':'Propuesta de rediseño · demo','ca':'Proposta de redisseny · demo','en':'Redesign proposal · demo','fr':'Proposition de refonte · démo'}
CHATCTA={l:B.UI[l]['modes']['wa'][1] for l in LANGS}
CSS_BASE=B.CSS
CSS_NONOTICE='header{inset:0 0 auto}\n'
CSS_A11Y=r"""
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.skip{position:absolute;left:8px;top:-80px;z-index:100;background:#fff;color:#111;padding:10px 14px;border-radius:8px;font-weight:600}
.skip:focus{top:44px}
:focus-visible{outline:3px solid #1f1d1a;outline-offset:2px;box-shadow:0 0 0 2px #fff}
main:focus{outline:none;box-shadow:none}
.langs button,.links a{opacity:1}
.langs button{min-width:36px;min-height:36px}
.langs button[aria-pressed=true]{background:rgba(127,127,127,.35);text-decoration:underline}
#menub{display:none;background:none;border:1.5px solid currentColor;color:inherit;border-radius:8px;width:40px;height:40px;font-size:20px;cursor:pointer}
#chatb,#chat header button,#qs button,#chat form button{min-width:36px;min-height:36px}
.card h3 a{color:inherit}
.hero:after{background:linear-gradient(180deg,rgba(0,0,0,.62) 0,rgba(0,0,0,.5) 35%,rgba(0,0,0,.8) 100%)}
header:not(.s){background:linear-gradient(180deg,rgba(0,0,0,.7),rgba(0,0,0,0))}
.hero h1,.hero p,.hero .kick,.brand,.links a,.langs button{text-shadow:0 1px 3px rgba(0,0,0,.55)}
.hero .btn.ghost{background:#1f1d1a}
header.s{backdrop-filter:none;-webkit-backdrop-filter:none}
header.s .brand,header.s .links a,header.s .langs button{text-shadow:none}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important;animation:none!important}}
@media(max-width:860px){#menub{display:inline-flex;align-items:center;justify-content:center}
.brand{white-space:normal;line-height:1.05;font-size:1rem;overflow:visible}
.links.o{display:flex;flex-direction:column;position:absolute;top:100%;left:0;right:0;background:var(--bg);color:var(--ink);padding:10px 20px 16px;gap:4px;box-shadow:0 8px 20px rgba(0,0,0,.15)}
.links.o a{padding:12px 4px;font-size:1rem}}
"""
CSS_SEC=r""".mt0{padding:0}.ac-t{color:var(--ac)}.btn.ghost.ac-t{color:var(--ac)!important}.mt18{margin-top:18px}
"""
JS_HEAD=r"""const D=__DATA__;let L='es';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const cl=s=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9 ]+/g,' ').replace(/\s+/g,' ');
const norm=s=>' '+cl(s).trim()+' ';const nk=k=>(k[0]===' '?' ':'')+cl(k).trim()+(k.slice(-1)===' '?' ':'');
"""
JS_TXT_OLD="$$('[data-t]').forEach(e=>{const k=e.dataset.t;if(t[k]!==undefined)e.innerHTML=t[k]});"
JS_TXT_SAFE="$$('[data-t]').forEach(e=>{const k=e.dataset.t;if(t[k]!==undefined)e.textContent=t[k]});"
JS_SAY_OLD=r"""function say(h,c,cta){const d=document.createElement('div');d.className='m '+c;d.innerHTML=h+(cta?' <a href="'+D.book[L]+'" target="_blank" rel="noopener">'+D.i18n[L].chat_cta+'</a>':'');$('#msgs').appendChild(d);$('#msgs').scrollTop=1e6}
function ask(q){say(q.replace(/</g,'&lt;'),'u');"""
JS_SAY_SAFE=r"""function say(h,c,cta){const d=document.createElement('div');d.className='m '+c;d.appendChild(document.createTextNode(h));
if(cta){d.appendChild(document.createTextNode(' '));const a=document.createElement('a');a.href=D.book[L];a.target='_blank';a.rel='noopener noreferrer';a.textContent=D.i18n[L].chat_cta;d.appendChild(a)}
$('#msgs').appendChild(d);$('#msgs').scrollTop=$('#msgs').scrollHeight}
function ask(q){say(q,'u');"""
JS_BODY=r"""
function setLang(l){L=D.i18n[l]?l:'es';const t=D.i18n[L];document.documentElement.lang=L;
__TXT__
$$('[data-book]').forEach(e=>{e.href=D.book[L]||D.book.es});
$$('.langs button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.l===L));
__A11Y_SET__
document.title=t.title;$$('[data-alt]').forEach(e=>{e.alt=(t.alts&&t.alts[e.dataset.alt])||''});try{localStorage.setItem('lang',L)}catch(e){}
$('#msgs').textContent='';say(t.chat_hello,'b');$('#qs').textContent='';t.chips.forEach(c=>{const b=document.createElement('button');b.type='button';b.textContent=c;b.onclick=()=>ask(c);$('#qs').appendChild(b)});$('#q').placeholder=t.chat_ph}
__SAY__
const n=norm(q),t=D.i18n[L];let best=null,sc=0;
t.faq.forEach(f=>{let s=0;f.k.forEach(k=>{if(n.includes(nk(k)))s+=k.trim().length});if(s>sc){sc=s;best=f}});
setTimeout(()=>say(best?best.a:t.chat_fb,'b',best&&best.cta),250)}
addEventListener('scroll',()=>$('header').classList.toggle('s',scrollY>40),{passive:true});
$$('.langs button').forEach(b=>b.onclick=()=>setLang(b.dataset.l));
__CHATUI__
$('#chat form').onsubmit=e=>{e.preventDefault();const v=$('#q').value.trim();if(v){ask(v);$('#q').value=''}};
let init=new URLSearchParams(location.search).get('lang');try{init=init||localStorage.getItem('lang')}catch(e){}
init=(init||(navigator.language||'es')).slice(0,2);setLang(D.i18n[init]?init:'es');
"""
CHATUI_OLD="""$('#chatb').onclick=()=>{$('#chat').classList.toggle('o');if($('#chat').classList.contains('o'))$('#q').focus()};
$('#chatx').onclick=()=>$('#chat').classList.remove('o');"""
CHATUI_A11Y="""const chat=$('#chat'),cb=$('#chatb'),mb=$('#menub'),nav=$('#nav');
function chatSet(o){chat.classList.toggle('o',o);cb.setAttribute('aria-expanded',o);if(o)$('#q').focus();else cb.focus()}
cb.onclick=()=>chatSet(!chat.classList.contains('o'));$('#chatx').onclick=()=>chatSet(false);
function menuSet(o){nav.classList.toggle('o',o);mb.setAttribute('aria-expanded',o)}
mb.onclick=()=>menuSet(!nav.classList.contains('o'));
nav.addEventListener('click',e=>{if(e.target.closest('a'))menuSet(false)});
addEventListener('keydown',e=>{if(e.key==='Escape'){if(chat.classList.contains('o'))chatSet(false);else if(nav.classList.contains('o')){menuSet(false);mb.focus()}}});"""
A11Y_SET="""$$('[data-aria]').forEach(e=>e.setAttribute('aria-label',t[e.dataset.aria]));$$('.langs button').forEach(b=>b.setAttribute('aria-label',b.dataset.l.toUpperCase()+' · '+t.lang_names[b.dataset.l]));$$('[data-rn]').forEach(e=>e.setAttribute('aria-label',t.room_cta.replace(/ →$/,'')+' · '+t['room'+e.dataset.rn+'_n']));"""

CSP="default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; media-src 'none'; frame-src 'none'; manifest-src 'none'"

def build(d,kb,out,imgs,alts,stage):
    """stage: set de {'kb','a11y','sec','v1'}"""
    kbF,a11y,sec,v1='kb' in stage,'a11y' in stage,'sec' in stage,'v1' in stage
    for l in LANGS:   # textos de interfaz propios del tipo de negocio (p. ej. «Pedir cita» en vez de «Reservar»)
        for k,v in d.get('ui',{}).get(l,{}).items():
            if isinstance(v,dict): B.UI[l][k].update(v)
            else: B.UI[l][k]=v
    for l,v in d.get('foot',{}).items(): B.FOOT[l]=v
    os.makedirs(out+'/fonts',exist_ok=True);shutil.copy(B.FONT,out+'/fonts/')
    mode=d['book']['mode'];urls=B.book_urls(d,LANGS);contact=' · '.join(d['phones']+d['emails'])
    rel='noopener noreferrer' if sec else 'noopener'
    i18n={}
    for l in LANGS:
        u=B.UI[l];t=d['t'][l];bl,rc,ba=u['modes'][mode];X=B.EXTRA[l]
        A=f'<a href="{html.escape(urls[l])}" target="_blank" rel="noopener">'
        x=dict(title=t['title'],nav_rooms=t['nav_rooms'],nav_svc=u['nav_svc'],nav_gal=u['nav_gal'],nav_loc=u['nav_loc'],book=u['book'],book_long=bl,see_rooms=t['see_rooms'],
         hero_k=t['hero_k'],hero_t=t['hero_t'],hero_s=t['hero_s'],intro_k=d['name'],intro_t=t['intro_t'],intro_p1=t['intro_p1'],intro_p2=t['intro_p2'],
         rooms_t=t['rooms_t'],rooms_s=t['rooms_s'],room_cta=rc,svc_t=u['svc_t'],gal_t=u['gal_t'],around_t=u['around_t'],around_s=t.get('around_s',''),loc_t=u['loc_t'],loc_p=t['loc_p'],map=u['map'],contact_t=u['contact_t'],
         chat_t=u['chat_t'],chat_ph=u['chat_ph'],send=u['send'],chat_hello=u['hello'].format(n=d['name']),chat_fb=u['fb'].format(c=contact),chat_cta=CHATCTA[l],
         notice=B.NOTICE[l] if v1 else DEMO[l],ill=B.ILL[l],foot=B.FOOT[l] if v1 else DEMO[l],alts=alts[l] if a11y else {})
        if not v1: x.pop('ill')
        if not d['around']: x.pop('around_t');x.pop('around_s')
        for i,s in enumerate(t['stats']): x[f'stat{i}']=s
        for i,s in enumerate(t['svcs']): x[f'svc{i}']=s
        for i,(rn,rd) in enumerate(t['rooms']): x[f'room{i}_n']=rn;x[f'room{i}_d']=rd
        if a11y:
            x.update(skip=X['skip'],menu=X['menu'],chat_open=X['chat_open'],chat_close=X['chat_close'],langs_label=X['langs_label'],lang_names=X['lang_names'],chat_label=X['chat_label'],nav_label=X['nav_label'])
        if kbF:
            x['faq']=[dict(k=e['keys'][l],a=e['a'][l],cta=e['cta']) for e in kb['entries']]
            x['chips']=t['chips']
        else:
            k=u['kw'];x['faq']=[dict(k=k['where'],a=d['address']),dict(k=k['book'],a=ba.format(a=A,c=contact)),dict(k=k['contact'],a=contact)]
            x['chips']=[u['chip_where'],u['chip_book']]
        i18n[l]=x
    keys=set(i18n['es'])
    for l in LANGS: assert set(i18n[l])==keys,(l,keys^set(i18n[l]))
    data=dict(i18n=i18n,book=urls)
    # ---- HTML
    es=i18n['es']
    def img(n,sizes='100vw',eager=False):
        a=html.escape(es['alts'].get(n,'')) if a11y else (d['name'] if eager else '')
        return (f'<img src="img/{n}-m.webp" srcset="img/{n}-m.webp 800w, img/{n}.webp 1600w" sizes="{sizes}" alt="{a}"'+(f' data-alt="{n}"' if a11y else '')+
                (' fetchpriority=high' if eager else ' loading=lazy decoding=async')+'>')
    def tt(k,tag='span',cls='',extra=''):
        return f'<{tag}{(" class="+cls) if cls else ""}{extra} data-t="{k}">{html.escape(str(es.get(k,"")))}</{tag}>'
    B0=html.escape(urls['es'])
    def blink(k,cls='btn',extra=''):
        return f'<a class="{cls}" data-book="" href="{B0}" target="_blank" rel="{rel}"{extra} data-t="{k}">{html.escape(es[k])}</a>'
    rooms=''.join(f'<article class="card">{img(r,"(max-width:860px) 100vw, 380px")}<div><h3 data-t="room{i}_n">{html.escape(es[f"room{i}_n"])}</h3><p data-t="room{i}_d">{html.escape(es[f"room{i}_d"])}</p>'
                  +f'<a data-book="" href="{B0}" target="_blank" rel="{rel}"'+(f' data-rn="{i}"' if a11y else '')+f' data-t="room_cta">{html.escape(es["room_cta"])}</a></div></article>' for i,r in enumerate(imgs['rooms']))
    gal=''.join(img(g,'(max-width:860px) 50vw, 300px') for g in imgs['gallery'])
    around=''.join(f'<li>{html.escape(x)}</li>' for x in d['around'])
    around_sec=(f'<section><div class="wrap"><h2 data-t="around_t">{html.escape(es["around_t"])}</h2><p class="sub" data-t="around_s">{html.escape(es["around_s"])}</p><ul class="chips">{around}</ul></div></section>' if d['around'] else '')
    stats=''.join(tt(f'stat{i}') for i in range(len(d['t']['es']['stats'])))
    svc=''.join(f'<li data-t="svc{i}">{html.escape(es[f"svc{i}"])}</li>' for i in range(len(d['t']['es']['svcs'])))
    phones=' · '.join(f'<a href="tel:{(p if p.startswith("+") else "+34"+p).replace(" ","")}">{p}</a>' for p in d['phones'])
    mails=' · '.join(f'<a href="mailto:{e}">{e}</a>' for e in d['emails'])
    cls_ac='' if sec else ' style="color:var(--ac)"'
    langb=''.join(f'<button type="button" data-l="{l}" aria-pressed="false"'+(f' lang="{l}"' if a11y else '')+f'>{l.upper()}</button>' for l in LANGS)
    notice=f'<div class="notice" role="note" data-t="notice">{html.escape(es["notice"])}</div>' if v1 else ''
    skip=f'<a class="skip" href="#top" data-t="skip">{html.escape(es["skip"])}</a>' if a11y else ''
    menub='<button type="button" id="menub" aria-expanded="false" aria-controls="nav" data-aria="menu" aria-label="Menú">☰</button>' if a11y else ''
    navattr=' id="nav"'+(' data-aria="nav_label" aria-label="Navegación principal"' if a11y else '')
    chatb=('<button type="button" id="chatb" aria-expanded="false" aria-controls="chat" data-aria="chat_open" aria-label="Abrir asistente">💬</button>' if a11y else '<button id="chatb" aria-label="Chat">💬</button>')
    chatd=(f'<div id="chat" role="dialog" aria-labelledby="chat_h"><div class="chh"><span id="chat_h" data-t="chat_t">{html.escape(es["chat_t"])}</span><button type="button" id="chatx" data-aria="chat_close" aria-label="Cerrar asistente">×</button></div><div id="msgs" role="log" aria-live="polite" tabindex="0"></div><div id="qs"></div><form><label class="sr" for="q" data-t="chat_label">{html.escape(es["chat_label"])}</label><input id="q" autocomplete="off"><button type="submit" data-t="send">{html.escape(es["send"])}</button></form></div>' if a11y else
        f'<div id="chat" role="dialog" aria-label="Chat"><header><span data-t="chat_t">{html.escape(es["chat_t"])}</span><button id="chatx" aria-label="Cerrar">×</button></header><div id="msgs"></div><div id="qs"></div><form><input id="q" autocomplete="off"><button data-t="send">{html.escape(es["send"])}</button></form></div>')
    langgrp=f'<div class="langs" role="group"'+(' data-aria="langs_label" aria-label="Idioma"' if a11y else ' aria-label="Idioma / Language"')+f'>{langb}</div>'
    sticky=f'<div class="sticky">{blink("book_long")}</div>'
    aside_o='<aside data-aria="chat_t" aria-label="Asistente">' if a11y else '';aside_c='</aside>' if a11y else ''
    illspan=f'<span class="ill" data-t="ill">{html.escape(es["ill"])}</span>' if v1 else ''
    sty_pad='' if sec else ' style="padding:0"'
    maps=f'https://www.google.com/maps/search/?api=1&amp;query={up.quote(d["maps"])}'
    head_extra=(f'<meta http-equiv="Content-Security-Policy" content="{CSP}"><meta name="referrer" content="no-referrer">' if sec else '')
    css=CSS_BASE%dict(ac=d['ac'],ac2=d['ac2_a11y'] if a11y else d['ac2'])
    if not v1: css+=CSS_NONOTICE
    if a11y: css=css.replace('#chat header','#chat .chh')+CSS_A11Y
    if sec: css+=CSS_SEC.replace('.btn.ghost.ac-t','.btn.ghost.ac-t')
    css_tag='<link rel="stylesheet" href="styles.css">' if sec else f'<style>{css}</style>'
    # ---- JS
    js=JS_HEAD+JS_BODY
    js=js.replace('__TXT__',JS_TXT_SAFE if sec else JS_TXT_OLD).replace('__SAY__',JS_SAY_SAFE if sec else JS_SAY_OLD)
    js=js.replace('__CHATUI__',CHATUI_A11Y if a11y else CHATUI_OLD).replace('__A11Y_SET__',A11Y_SET if a11y else '')
    js=js.replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')))
    js_tag='<script src="app.js"></script>' if sec else f'<script>{js}</script>'
    ghost=f'<a class="btn ghost{" ac-t" if sec else ""}"'+cls_ac+f' href="{maps}" target="_blank" rel="{rel}" data-t="map">{html.escape(es["map"])}</a>'
    page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{head_extra}<title>{html.escape(es["title"])}</title><meta name="robots" content="noindex,nofollow"><link rel="icon" href="data:,"><meta name="description" content="{html.escape(es["hero_s"])}">
<link rel="preload" as="image" href="img/{imgs["hero"]}-m.webp" imagesrcset="img/{imgs["hero"]}-m.webp 800w, img/{imgs["hero"]}.webp 1600w" imagesizes="100vw">
{css_tag}</head><body>
{skip}{notice if not a11y else ''}
<header>{notice if a11y else ''}<div class="wrap nav"><a class="brand" href="#top">{html.escape(d["name"])}</a><nav class="links"{navattr}><a href="#rooms" data-t="nav_rooms">{html.escape(es["nav_rooms"])}</a><a href="#services" data-t="nav_svc">{html.escape(es["nav_svc"])}</a><a href="#gallery" data-t="nav_gal">{html.escape(es["nav_gal"])}</a><a href="#contact" data-t="nav_loc">{html.escape(es["nav_loc"])}</a></nav>
{langgrp}{menub}{blink("book")}</div></header>
<main id="top"{' tabindex="-1"' if a11y else ''}><section class="hero{" mt0" if sec else ""}"{sty_pad}>{img(imgs["hero"],eager=True)}<div class="wrap">{tt("hero_k","div","kick")}<h1 data-t="hero_t">{html.escape(es["hero_t"])}</h1><p data-t="hero_s">{html.escape(es["hero_s"])}</p>
<div class="cta">{blink("book_long")}<a class="btn ghost" href="#rooms" data-t="see_rooms">{html.escape(es["see_rooms"])}</a></div></div>{illspan}</section>
<section><div class="wrap intro"><div><div class="kick{" ac-t" if sec else ""}"{cls_ac} data-t="intro_k">{html.escape(es["intro_k"])}</div><h2 data-t="intro_t">{html.escape(es["intro_t"])}</h2><p data-t="intro_p1">{html.escape(es["intro_p1"])}</p><p data-t="intro_p2">{html.escape(es["intro_p2"])}</p><div class="stats">{stats}</div></div>{img(imgs["intro"],"(max-width:860px) 100vw, 480px")}</div></section>
<section class="alt" id="rooms"><div class="wrap"><h2 data-t="rooms_t">{html.escape(es["rooms_t"])}</h2><p class="sub" data-t="rooms_s">{html.escape(es["rooms_s"])}</p><div class="grid">{rooms}</div></div></section>
<section id="services"><div class="wrap"><h2 data-t="svc_t">{html.escape(es["svc_t"])}</h2><ul class="svc">{svc}</ul></div></section>
<section class="alt" id="gallery"><div class="wrap"><h2 data-t="gal_t">{html.escape(es["gal_t"])}</h2><div class="gal">{gal}</div></div></section>
{around_sec}
<section id="contact"><div class="wrap loc"><div><h2 data-t="loc_t">{html.escape(es["loc_t"])}</h2><p data-t="loc_p">{html.escape(es["loc_p"])}</p><p>{ghost}</p></div>
<div class="box"><h3 data-t="contact_t">{html.escape(es["contact_t"])}</h3><p>{html.escape(d["address"])}</p><p>{phones}</p><p>{mails}</p><p class="{"mt18" if sec else ""}"{"" if sec else ' style="margin-top:18px"'}>{blink("book_long")}</p></div></div></section>{sticky if a11y else ''}</main>
<footer><div class="wrap"><strong>{html.escape(d["name"])}</strong><br>{html.escape(d["address"])} · {phones} · {mails}
<div class="demo"><strong data-t="notice">{html.escape(es["notice"])}</strong> · <span data-t="foot">{html.escape(es["foot"])}</span></div></div></footer>
{'' if a11y else sticky}{aside_o}{chatb}{chatd}{aside_c}
{js_tag}</body></html>'''
    open(out+'/index.html','w').write(page)
    open(out+'/robots.txt','w').write('User-agent: *\nDisallow: /\n')
    if sec:
        open(out+'/styles.css','w').write(css);open(out+'/app.js','w').write(js)
    elif os.path.exists(out+'/styles.css'): os.remove(out+'/styles.css');os.remove(out+'/app.js')
    return i18n
