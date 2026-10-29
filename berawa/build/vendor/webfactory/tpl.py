import json,html,os,shutil
CSS=r"""
@font-face{font-family:Cormorant;src:url(fonts/cormorant.woff2) format('woff2');font-weight:300 700;font-display:swap}
:root{--ac:%(ac)s;--ac2:%(ac2)s;--ink:#1f1d1a;--mut:#6b655d;--bg:#fbf8f3;--card:#fff;--line:#e8e1d6}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:16px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg)}
img{max-width:100%%;display:block}a{color:var(--ac)}
h1,h2,h3{font-family:Cormorant,Georgia,serif;font-weight:600;line-height:1.1;margin:0 0 .5em}
h2{font-size:clamp(2rem,4vw,2.8rem)}h3{font-size:1.5rem}
.wrap{max-width:1140px;margin:0 auto;padding:0 20px}
header{position:fixed;inset:36px 0 auto;z-index:20;transition:.3s;color:#fff}
header.s{background:rgba(251,248,243,.96);color:var(--ink);box-shadow:0 1px 0 var(--line);backdrop-filter:blur(8px)}
.nav{display:flex;align-items:center;gap:18px;height:68px}
.brand{font-family:Cormorant,Georgia,serif;font-size:1.45rem;font-weight:600;color:inherit;text-decoration:none;margin-right:auto;white-space:nowrap}
.links{display:flex;gap:20px}.links a{color:inherit;text-decoration:none;font-size:.92rem;opacity:.9}
.langs{display:flex;gap:2px}.langs button{background:none;border:0;color:inherit;font:600 .78rem system-ui;padding:6px 7px;border-radius:6px;cursor:pointer;opacity:.65}
.langs button[aria-pressed=true]{opacity:1;background:rgba(127,127,127,.18)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--ac);color:#fff!important;text-decoration:none;font-weight:600;padding:12px 22px;border-radius:999px;border:0;cursor:pointer;font-size:.95rem;transition:.2s}
.btn:hover{filter:brightness(1.1);transform:translateY(-1px)}.btn.ghost{background:transparent;border:1.5px solid currentColor;color:inherit!important}
.hero{position:relative;min-height:92vh;display:flex;align-items:flex-end;color:#fff;overflow:hidden}
.hero picture,.hero img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45) 0,rgba(0,0,0,.05) 35%%,rgba(0,0,0,.65) 100%%)}
.hero .wrap{position:relative;z-index:2;padding-bottom:9vh;width:100%%}
.kick{text-transform:uppercase;letter-spacing:.18em;font-size:.78rem;opacity:.9}
.hero h1{font-size:clamp(2.6rem,7vw,5.2rem);max-width:15ch;margin:.2em 0 .25em}
.hero p{font-size:1.15rem;max-width:46ch;opacity:.95;margin:0 0 1.4em}
.cta{display:flex;gap:12px;flex-wrap:wrap}
section{padding:88px 0}.alt{background:#f3eee6}
.intro{display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.intro img{border-radius:18px;aspect-ratio:4/5;object-fit:cover;width:100%%}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}.stats span{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 14px;font-size:.88rem}
.sub{color:var(--mut);max-width:60ch;margin:-.2em 0 2em}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px}
.card{background:var(--card);border-radius:16px;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.05),0 8px 24px rgba(0,0,0,.05);display:flex;flex-direction:column}
.card img{aspect-ratio:4/3;object-fit:cover;width:100%%}.card div{padding:18px 20px 22px;display:flex;flex-direction:column;gap:10px;flex:1}
.card p{margin:0;color:var(--mut);font-size:.95rem;flex:1}.card a{font-weight:600;text-decoration:none}
.svc{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;list-style:none;padding:0;margin:0}
.svc li{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px;display:flex;gap:12px;align-items:flex-start}
.svc li:before{content:"";flex:0 0 10px;height:10px;margin-top:8px;border-radius:50%%;background:var(--ac2)}
.gal{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.gal img{width:100%%;height:100%%;object-fit:cover;border-radius:12px;aspect-ratio:1}
.gal img:first-child{grid-column:span 2;grid-row:span 2}
.chips{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0}.chips li{background:#fff;border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-size:.9rem}
.loc{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.box{background:#fff;border-radius:16px;padding:28px;border:1px solid var(--line)}.box p{margin:.3em 0}
footer{background:#1f1d1a;color:#d9d3c9;padding:44px 0 90px;font-size:.92rem}footer a{color:#fff}
.demo{opacity:.6;font-size:.8rem;margin-top:18px}
.sticky{display:none}
.notice{position:fixed;top:0;left:0;right:0;z-index:40;height:36px;display:flex;align-items:center;justify-content:center;background:#111;color:#fff;font:600 13px/1.2 system-ui,sans-serif;text-align:center;padding:0 10px}
.ill{position:absolute;right:14px;bottom:12px;z-index:3;background:rgba(0,0,0,.55);color:#fff;font-size:.72rem;padding:3px 9px;border-radius:999px}
.demo{opacity:1;color:#d9d3c9}
.demo{line-height:1.5}
#chatb{position:fixed;right:18px;bottom:18px;z-index:30;width:58px;height:58px;border-radius:50%%;background:var(--ac2);color:#fff;border:0;box-shadow:0 8px 24px rgba(0,0,0,.25);cursor:pointer;font-size:26px}
#chat{position:fixed;right:18px;bottom:88px;z-index:31;width:min(370px,calc(100vw - 36px));max-height:min(560px,calc(100vh - 120px));background:#fff;border-radius:18px;box-shadow:0 18px 50px rgba(0,0,0,.25);display:none;flex-direction:column;overflow:hidden}
#chat.o{display:flex}#chat header{position:static;background:var(--ac);color:#fff;padding:14px 16px;font-weight:600;display:flex;justify-content:space-between;align-items:center}
#chat header button{background:none;border:0;color:#fff;font-size:20px;cursor:pointer}
#msgs{padding:14px;overflow:auto;flex:1;display:flex;flex-direction:column;gap:8px;font-size:.93rem}
.m{padding:9px 13px;border-radius:14px;max-width:85%%;overflow-wrap:anywhere}.m.b{background:#f2ede5;align-self:flex-start}.m.u{background:var(--ac);color:#fff;align-self:flex-end}
#qs{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 10px}#qs button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 10px;font-size:.8rem;cursor:pointer}
#chat form{display:flex;border-top:1px solid var(--line)}#chat input{flex:1;border:0;padding:13px 14px;font:inherit;outline:none}#chat form button{border:0;background:none;color:var(--ac);font-weight:700;padding:0 16px;cursor:pointer}
@media(max-width:860px){.links{display:none}.brand{font-size:1.15rem;overflow:hidden;text-overflow:ellipsis;min-width:0}.nav{gap:8px}.langs button{padding:5px 5px;font-size:.72rem}.intro,.loc{grid-template-columns:1fr}.gal{grid-template-columns:repeat(2,1fr)}.nav .btn{display:none}
.sticky{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:25;padding:10px 84px 10px 12px;background:rgba(251,248,243,.97);border-top:1px solid var(--line)}.sticky .btn{flex:1}
section{padding:64px 0}.intro img{aspect-ratio:4/3}}
"""
JS=r"""
const D=__DATA__;let L='es';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
function setLang(l){L=D.i18n[l]?l:'es';const t=D.i18n[L];document.documentElement.lang=L;
$$('[data-t]').forEach(e=>{const k=e.dataset.t;if(t[k]!==undefined)e.innerHTML=t[k]});
$$('[data-book]').forEach(e=>{e.href=(e.dataset.book?D.roombook[e.dataset.book]:D.book)[L]||D.book.es});
$$('.langs button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.l===L));
document.title=t.title;$$('[data-alt]').forEach(e=>{e.alt=t.alts[e.dataset.alt]||''});try{localStorage.setItem('lang',L)}catch(e){}
$('#msgs').innerHTML='';say(t.chat_hello,'b');$('#qs').innerHTML='';t.chips.forEach(c=>{const b=document.createElement('button');b.type='button';b.textContent=c;b.onclick=()=>ask(c);$('#qs').appendChild(b)});$('#q').placeholder=t.chat_ph}
const norm=s=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
function say(h,c){const d=document.createElement('div');d.className='m '+c;d.innerHTML=h;$('#msgs').appendChild(d);$('#msgs').scrollTop=1e6}
function ask(q){say(q.replace(/</g,'&lt;'),'u');const n=norm(q),t=D.i18n[L];let best=null,sc=0;
t.faq.forEach(f=>{let s=0;f.k.forEach(k=>{if(n.includes(norm(k)))s+=k.length});if(s>sc){sc=s;best=f}});
setTimeout(()=>say(best?best.a:t.chat_fb,'b'),250)}
addEventListener('scroll',()=>$('header').classList.toggle('s',scrollY>40),{passive:true});
$$('.langs button').forEach(b=>b.onclick=()=>setLang(b.dataset.l));
$('#chatb').onclick=()=>{$('#chat').classList.toggle('o');if($('#chat').classList.contains('o'))$('#q').focus()};
$('#chatx').onclick=()=>$('#chat').classList.remove('o');
$('#chat form').onsubmit=e=>{e.preventDefault();const v=$('#q').value.trim();if(v){ask(v);$('#q').value=''}};
let init=new URLSearchParams(location.search).get('lang');try{init=init||localStorage.getItem('lang')}catch(e){}
init=init||(navigator.language||'es').slice(0,2);setLang(init);
"""
def T(k,tag='span',cls=''):
    return f'<{tag} data-t="{k}"{(" class=%s"%cls) if cls else ""}></{tag}>'
def build(d,out):
    os.makedirs(out+'/fonts',exist_ok=True)
    shutil.copy(os.path.join(os.path.dirname(__file__),'../build/cormorant.woff2'),out+'/fonts/')
    es=d['i18n']['es']
    def img(n,alt,sizes='100vw',eager=False,cls=''):
        return (f'<img src="img/{n}-m.webp" srcset="img/{n}-m.webp 800w, img/{n}.webp 1600w" sizes="{sizes}" alt="{html.escape(alt)}"'
                f'{" fetchpriority=high" if eager else " loading=lazy decoding=async"}{(" class="+cls) if cls else ""}>')
    rooms=''.join(f'<article class="card">{img(r["img"],"",sizes="(max-width:860px) 100vw, 380px")}<div><h3 data-t="room{i}_n"></h3><p data-t="room{i}_d"></p><a data-book="{r.get("book","")}" href="#" target="_blank" rel="noopener" data-t="room_cta"></a></div></article>' for i,r in enumerate(d['rooms']))
    gal=''.join(img(g,'',sizes='(max-width:860px) 50vw, 300px') for g in d['gallery'])
    extra=''
    if d.get('around'):
        extra=f'<section><div class="wrap"><h2 data-t="around_t"></h2><p class="sub" data-t="around_s"></p><ul class="chips">'+''.join(f'<li>{html.escape(x)}</li>' for x in d['around'])+'</ul></div></section>'
    stats=''.join(f'<span data-t="stat{i}"></span>' for i in range(d.get('nstats',0)))
    svc=''.join(f'<li data-t="svc{i}"></li>' for i in range(d['nsvc']))
    phones=' · '.join(f'<a href="tel:{p.replace(" ","")}">{p}</a>' for p in d['phones'])
    data=dict(i18n=d['i18n'],book=d['book'],roombook=d.get('roombook',{}))
    page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(es["title"])}</title><meta name="robots" content="noindex,nofollow"><link rel="icon" href="data:,"><meta name="description" content="{html.escape(es["hero_s"])}">
<link rel="preload" href="fonts/cormorant.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" as="image" href="img/{d["hero"]}-m.webp" imagesrcset="img/{d["hero"]}-m.webp 800w, img/{d["hero"]}.webp 1600w" imagesizes="100vw">
<style>{CSS % dict(ac=d["ac"],ac2=d["ac2"])}</style></head><body>
<header><div class="wrap nav"><a class="brand" href="#top">{html.escape(d["name"])}</a><nav class="links"><a href="#rooms" data-t="nav_rooms"></a><a href="#services" data-t="nav_svc"></a><a href="#gallery" data-t="nav_gal"></a><a href="#contact" data-t="nav_loc"></a></nav>
<div class="langs" role="group" aria-label="Idioma / Language">{"".join(f'<button type="button" data-l="{l}" aria-pressed="false">{l.upper()}</button>' for l in ["es","en","fr","de"])}</div>
<a class="btn" data-book="" href="{d["book"]["es"]}" target="_blank" rel="noopener" data-t="book"></a></div></header>
<main id="top"><section class="hero" style="padding:0">{img(d["hero"],d["name"],eager=True)}<div class="wrap"><div class="kick" data-t="hero_k"></div><h1 data-t="hero_t"></h1><p data-t="hero_s"></p>
<div class="cta"><a class="btn" data-book="" href="{d["book"]["es"]}" target="_blank" rel="noopener" data-t="book_long"></a><a class="btn ghost" href="#rooms" data-t="see_rooms"></a></div></div></section>
<section><div class="wrap intro"><div><div class="kick" style="color:var(--ac)" data-t="intro_k"></div><h2 data-t="intro_t"></h2><p data-t="intro_p1"></p><p data-t="intro_p2"></p><div class="stats">{stats}</div></div>{img(d["intro_img"],"",sizes="(max-width:860px) 100vw, 480px")}</div></section>
<section class="alt" id="rooms"><div class="wrap"><h2 data-t="rooms_t"></h2><p class="sub" data-t="rooms_s"></p><div class="grid">{rooms}</div></div></section>
<section id="services"><div class="wrap"><h2 data-t="svc_t"></h2><ul class="svc">{svc}</ul></div></section>
<section class="alt" id="gallery"><div class="wrap"><h2 data-t="gal_t"></h2><div class="gal">{gal}</div></div></section>
{extra}
<section id="contact"><div class="wrap loc"><div><h2 data-t="loc_t"></h2><p data-t="loc_p"></p><p><a class="btn ghost" style="color:var(--ac)!important" href="https://www.google.com/maps/search/?api=1&query={html.escape(d["maps"])}" target="_blank" rel="noopener" data-t="map"></a></p></div>
<div class="box"><h3 data-t="contact_t"></h3><p>{html.escape(d["address"])}</p><p>{phones}</p><p><a href="mailto:{d["email"]}">{d["email"]}</a></p><p style="margin-top:18px"><a class="btn" data-book="" href="{d["book"]["es"]}" target="_blank" rel="noopener" data-t="book_long"></a></p></div></div></section></main>
<footer><div class="wrap"><strong>{html.escape(d["name"])}</strong><br>{html.escape(d["address"])} · {phones} · <a href="mailto:{d["email"]}">{d["email"]}</a>
<div class="demo">Propuesta de rediseño · demo</div></div></footer>
<div class="sticky"><a class="btn" data-book="" href="{d["book"]["es"]}" target="_blank" rel="noopener" data-t="book_long"></a></div>
<button id="chatb" aria-label="Chat">💬</button><div id="chat" role="dialog" aria-label="Chat"><header><span data-t="chat_t"></span><button id="chatx" aria-label="Cerrar">×</button></header><div id="msgs"></div><div id="qs"></div><form><input id="q" autocomplete="off"><button data-t="send"></button></form></div>
<script>{JS.replace("__DATA__",json.dumps(data,ensure_ascii=False))}</script></body></html>'''
    open(out+'/index.html','w').write(page)
    open(out+'/robots.txt','w').write('User-agent: *\nDisallow: /\n')
    for k in d['i18n']['es']:
        for l in 'en fr de'.split():
            assert k in d['i18n'][l],(d['name'],l,k)
