"""Generador v2 (27 oct 2026): alojamientos de cualquier tipo + plantilla sobria de abogados.
Uso: from gen2 import build_aloj, build_law, prep_imgs"""
import json,html,os,shutil,urllib.parse as up
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
FONT=os.path.join(HERE,'..','..','..','..','fonts','cormorant.woff2')   # la fuente ya esta en la raiz del repo (copia de webfactory sin duplicar el binario)
LN={'es':'ES','ca':'CA','en':'EN','fr':'FR'}
LANGS=['es','ca','en','fr']
NOTICE={'es':'Propuesta de rediseño independiente, no oficial','ca':'Proposta de redisseny independent, no oficial','en':'Independent redesign proposal, not official','fr':'Proposition de refonte indépendante, non officielle'}
ILL={'es':'Imagen ilustrativa','ca':'Imatge il·lustrativa','en':'Illustrative image','fr':'Image illustrative'}
FOOT={'es':'Esta página es una propuesta de diseño hecha por Berawa sin encargo del establecimiento. Textos basados en su web pública; fotos ilustrativas de bancos libres, no muestran el establecimiento.','ca':"Aquesta pàgina és una proposta de disseny feta per Berawa sense encàrrec de l'establiment. Textos basats en la seva web pública; fotos il·lustratives de bancs lliures, no mostren l'establiment.",'en':'This page is a design proposal made by Berawa without any commission from the business. Text based on its public website; photos are illustrative stock images and do not show the business.','fr':"Cette page est une proposition de design réalisée par Berawa sans commande de l'établissement. Textes issus de son site public ; photos illustratives de banques libres, elles ne montrent pas l'établissement."}

def prep_imgs(out,items,big=1600,small=800,q=72):
    """items: {name: (src_path, crop_box_or_None)}"""
    os.makedirs(out+'/img',exist_ok=True)
    for n,v in items.items():
        src,crop=(v if isinstance(v,tuple) else (v,None))
        im=Image.open(src).convert('RGB')
        if crop: im=im.crop(crop)
        w,h=im.size
        b=im if w<=big else im.resize((big,round(h*big/w)),Image.LANCZOS)
        b.save(f'{out}/img/{n}.webp','WEBP',quality=q,method=6)
        sw=min(small,w); s=im.resize((sw,round(h*sw/w)),Image.LANCZOS)
        s.save(f'{out}/img/{n}-m.webp','WEBP',quality=q-4,method=6)

# ---------- textos comunes ----------
UI={
'es':dict(nav_rooms='Alojamiento',nav_svc='Servicios',nav_gal='Galería',nav_loc='Ubicación',see_rooms='Ver alojamiento',svc_t='Servicios',gal_t='Galería',loc_t='Dónde estamos',map='Abrir en Google Maps',contact_t='Contacto',
  around_t='Qué hacer cerca',chat_t='Asistente',chat_ph='Escribe tu pregunta…',send='Enviar',
  hello='¡Hola! Soy el asistente de {n}. Pregúntame por el alojamiento, los servicios, la zona o cómo reservar.',
  fb='No dispongo de esa información. Escríbenos o llámanos: {c}.',book='Reservar',
  modes=dict(engine=('Ver disponibilidad y precios','Ver disponibilidad →','Consulta disponibilidad y tarifas al momento en nuestro {a}motor de reservas</a>.'),
   form=('Solicitar reserva','Solicitar reserva →','Puedes pedir tu reserva en nuestro {a}formulario de reservas</a>; también por teléfono o correo: {c}.'),
   wa=('Reservar por WhatsApp','Consultar por WhatsApp →','Escríbenos por {a}WhatsApp</a> con tus fechas y te confirmamos la disponibilidad. También: {c}.'),
   mail=('Pedir reserva por correo','Pedir reserva →','Escríbenos a {a}nuestro correo</a> con tus fechas y número de personas. También por teléfono: {c}.'),
   ota=('Reservar online','Reservar online →','Puedes reservar online {a}aquí</a>, o contactarnos directamente: {c}.')),
  wa_txt='Hola, quería consultar disponibilidad en {n}.',mail_subj='Reserva · {n}',
  chip_where='¿Dónde estáis?',chip_book='Reservar',
  kw=dict(where=['donde','direccion','ubicacion','llegar','mapa','situad'],book=['reserv','precio','tarifa','disponib','cuesta','cuanto','libre','fecha'],contact=['telefono','llamar','email','correo','contacto','whatsapp'])),
'ca':dict(nav_rooms='Allotjament',nav_svc='Serveis',nav_gal='Galeria',nav_loc='Ubicació',see_rooms="Veure l'allotjament",svc_t='Serveis',gal_t='Galeria',loc_t='On som',map='Obrir a Google Maps',contact_t='Contacte',
  around_t='Què fer a prop',chat_t='Assistent',chat_ph='Escriu la teva pregunta…',send='Enviar',
  hello="Hola! Sóc l'assistent de {n}. Pregunta'm per l'allotjament, els serveis, l'entorn o com reservar.",
  fb='No disposo d\'aquesta informació. Escriu-nos o truca\'ns: {c}.',book='Reservar',
  modes=dict(engine=('Disponibilitat i preus','Veure disponibilitat →','Consulta disponibilitat i tarifes al moment al nostre {a}motor de reserves</a>.'),
   form=('Sol·licitar reserva','Sol·licitar reserva →','Pots demanar la reserva al nostre {a}formulari</a>; també per telèfon o correu: {c}.'),
   wa=('Reservar per WhatsApp','Consultar per WhatsApp →','Escriu-nos per {a}WhatsApp</a> amb les dates i et confirmem la disponibilitat. També: {c}.'),
   mail=('Demanar reserva per correu','Demanar reserva →','Escriu-nos al {a}nostre correu</a> amb les dates i el nombre de persones. També per telèfon: {c}.'),
   ota=('Reservar en línia','Reservar en línia →','Pots reservar en línia {a}aquí</a>, o contactar-nos directament: {c}.')),
  wa_txt='Hola, voldria consultar disponibilitat a {n}.',mail_subj='Reserva · {n}',
  chip_where='On sou?',chip_book='Reservar',
  kw=dict(where=['on ','adreca','ubicacio','arribar','mapa','situa'],book=['reserv','preu','tarifa','disponib','costa','quant','dates'],contact=['telefon','trucar','email','correu','contacte','whatsapp'])),
'en':dict(nav_rooms='Accommodation',nav_svc='Amenities',nav_gal='Gallery',nav_loc='Location',see_rooms='See accommodation',svc_t='Amenities',gal_t='Gallery',loc_t='Where we are',map='Open in Google Maps',contact_t='Contact',
  around_t='Things to do nearby',chat_t='Assistant',chat_ph='Type your question…',send='Send',
  hello="Hi! I'm the {n} assistant. Ask me about the accommodation, amenities, the area or how to book.",
  fb="I don't have that information. Please contact us: {c}.",book='Book',
  modes=dict(engine=('Check availability & rates','Check availability →','Check live availability and rates in our {a}booking engine</a>.'),
   form=('Request a booking','Request a booking →','You can request your booking through our {a}booking form</a>, or by phone or email: {c}.'),
   wa=('Book via WhatsApp','Ask on WhatsApp →','Send us your dates on {a}WhatsApp</a> and we will confirm availability. Also: {c}.'),
   mail=('Request by email','Request a booking →','Email {a}us</a> with your dates and number of guests. Or call: {c}.'),
   ota=('Book online','Book online →','You can book online {a}here</a>, or contact us directly: {c}.')),
  wa_txt="Hello, I'd like to check availability at {n}.",mail_subj='Booking request · {n}',
  chip_where='Where are you?',chip_book='Book',
  kw=dict(where=['where','address','location','get there','map','located'],book=['book','price','rate','availab','cost','how much','dates','reserv'],contact=['phone','call','email','mail','contact','whatsapp'])),
'fr':dict(nav_rooms='Hébergement',nav_svc='Services',nav_gal='Galerie',nav_loc='Accès',see_rooms="Voir l'hébergement",svc_t='Services',gal_t='Galerie',loc_t='Où nous trouver',map='Ouvrir dans Google Maps',contact_t='Contact',
  around_t='À faire aux alentours',chat_t='Assistant',chat_ph='Votre question…',send='Envoyer',
  hello="Bonjour ! Je suis l'assistant de {n}. Posez-moi vos questions sur l'hébergement, les services, la région ou la réservation.",
  fb="Je ne dispose pas de cette information. Contactez-nous : {c}.",book='Réserver',
  modes=dict(engine=('Disponibilités et tarifs','Voir les disponibilités →','Consultez disponibilités et tarifs en temps réel sur notre {a}moteur de réservation</a>.'),
   form=('Demander une réservation','Demander une réservation →','Vous pouvez demander votre réservation via notre {a}formulaire</a>, ou par téléphone ou e-mail : {c}.'),
   wa=('Réserver par WhatsApp','Écrire sur WhatsApp →','Envoyez-nous vos dates sur {a}WhatsApp</a> et nous confirmons la disponibilité. Aussi : {c}.'),
   mail=('Réserver par e-mail','Demander une réservation →',"Écrivez-{a}nous</a> avec vos dates et le nombre de personnes. Ou appelez : {c}."),
   ota=('Réserver en ligne','Réserver en ligne →','Vous pouvez réserver en ligne {a}ici</a>, ou nous contacter directement : {c}.')),
  wa_txt='Bonjour, je souhaite connaître les disponibilités à {n}.',mail_subj='Demande de réservation · {n}',
  chip_where='Où êtes-vous ?',chip_book='Réserver',
  kw=dict(where=['ou ','adresse','situ','acces','venir','carte'],book=['reserv','prix','tarif','disponib','combien','dates'],contact=['telephone','appeler','email','mail','contact','whatsapp'])),
'de':dict(nav_rooms='Unterkunft',nav_svc='Ausstattung',nav_gal='Galerie',nav_loc='Lage',see_rooms='Unterkunft ansehen',svc_t='Ausstattung',gal_t='Galerie',loc_t='So finden Sie uns',map='In Google Maps öffnen',contact_t='Kontakt',
  around_t='Ausflüge in der Umgebung',chat_t='Assistent',chat_ph='Ihre Frage…',send='Senden',
  hello='Hallo! Ich bin der Assistent von {n}. Fragen Sie mich zur Unterkunft, Ausstattung, Umgebung oder Buchung.',
  fb='Dazu habe ich keine Information. Kontaktieren Sie uns: {c}.',book='Buchen',
  modes=dict(engine=('Verfügbarkeit & Preise','Verfügbarkeit prüfen →','Aktuelle Verfügbarkeit und Preise finden Sie in unserer {a}Buchungsmaschine</a>.'),
   form=('Buchung anfragen','Buchung anfragen →','Sie können Ihre Buchung über unser {a}Formular</a> anfragen, oder per Telefon/E-Mail: {c}.'),
   wa=('Per WhatsApp buchen','Per WhatsApp fragen →','Schicken Sie uns Ihre Daten per {a}WhatsApp</a>, wir bestätigen die Verfügbarkeit. Oder: {c}.'),
   mail=('Per E-Mail anfragen','Buchung anfragen →','Schreiben Sie {a}uns</a> mit Reisedaten und Personenzahl. Oder rufen Sie an: {c}.'),
   ota=('Online buchen','Online buchen →','Sie können {a}hier</a> online buchen oder uns direkt kontaktieren: {c}.')),
  wa_txt='Hallo, ich möchte die Verfügbarkeit bei {n} anfragen.',mail_subj='Buchungsanfrage · {n}',
  chip_where='Wo liegt es?',chip_book='Buchen',
  kw=dict(where=['wo ','adresse','lage','anfahrt','karte','liegt'],book=['buch','preis','verfugbar','kosten','wie viel','termin','reserv'],contact=['telefon','anruf','email','mail','kontakt','whatsapp']))}


EXTRA={
'es':dict(skip='Saltar al contenido',menu='Menú',menu_open='Abrir menú',menu_close='Cerrar menú',chat_open='Abrir asistente',chat_close='Cerrar asistente',langs_label='Idioma',lang_names=dict(es='Español',ca='Català',en='English',fr='Français'),chat_label='Tu pregunta',nav_label='Navegación principal',price_note='Precios publicados en su web; confirma al reservar.'),
'ca':dict(skip='Salta al contingut',menu='Menú',menu_open='Obre el menú',menu_close='Tanca el menú',chat_open="Obre l'assistent",chat_close="Tanca l'assistent",langs_label='Idioma',lang_names=dict(es='Español',ca='Català',en='English',fr='Français'),chat_label='La teva pregunta',nav_label='Navegació principal',price_note='Preus publicats a la seva web; confirma en reservar.'),
'en':dict(skip='Skip to content',menu='Menu',menu_open='Open menu',menu_close='Close menu',chat_open='Open assistant',chat_close='Close assistant',langs_label='Language',lang_names=dict(es='Español',ca='Català',en='English',fr='Français'),chat_label='Your question',nav_label='Main navigation',price_note='Prices published on their website; confirm when booking.'),
'fr':dict(skip='Aller au contenu',menu='Menu',menu_open='Ouvrir le menu',menu_close='Fermer le menu',chat_open="Ouvrir l'assistant",chat_close="Fermer l'assistant",langs_label='Langue',lang_names=dict(es='Español',ca='Català',en='English',fr='Français'),chat_label='Votre question',nav_label='Navigation principale',price_note='Prix publiés sur leur site ; à confirmer lors de la réservation.')}

CSS=open(os.path.join(HERE,'tpl.py')).read().split('CSS=r"""')[1].split('"""')[0]
JS=open(os.path.join(HERE,'tpl.py')).read().split('JS=r"""')[1].split('"""')[0]

def book_urls(d,langs):
    b=d['book'];m=b['mode'];n=d['name'];out={}
    for l in langs:
        u=UI[l]
        if m=='wa': out[l]=f"https://wa.me/{b['num']}?text="+up.quote(u['wa_txt'].format(n=n))
        elif m=='mail': out[l]=f"mailto:{b['email']}?subject="+up.quote(u['mail_subj'].format(n=n))
        else: out[l]=b['url'] if isinstance(b['url'],str) else b['url'][l]
    return out

def build_aloj(d,out):
    langs=LANGS
    os.makedirs(out+'/fonts',exist_ok=True); shutil.copy(FONT,out+'/fonts/')
    mode=d['book']['mode']; urls=book_urls(d,langs)
    contact=' · '.join(d['phones']+d['emails'])
    i18n={}
    for l in langs:
        u=UI[l]; t=d['t'][l]; bl,rc,ba=u['modes'][mode]
        A=f'<a href="{html.escape(urls[l])}" target="_blank" rel="noopener">'
        x=dict(title=t['title'],nav_rooms=t.get('nav_rooms',u['nav_rooms']),nav_svc=u['nav_svc'],nav_gal=u['nav_gal'],nav_loc=u['nav_loc'],book=u['book'],book_long=t.get('book_long',bl),see_rooms=t.get('see_rooms',u['see_rooms']),
          hero_k=t['hero_k'],hero_t=t['hero_t'],hero_s=t['hero_s'],intro_k=t.get('intro_k',d['name']),intro_t=t['intro_t'],intro_p1=t['intro_p1'],intro_p2=t.get('intro_p2',''),
          rooms_t=t.get('rooms_t',t.get('nav_rooms',u['nav_rooms'])),rooms_s=t.get('rooms_s',''),room_cta=t.get('room_cta',rc),svc_t=t.get('svc_t',u['svc_t']),gal_t=t.get('gal_t',u['gal_t']),
          around_t=t.get('around_t',u['around_t']),around_s=t.get('around_s',''),loc_t=u['loc_t'],loc_p=t['loc_p'],map=u['map'],contact_t=u['contact_t'],
          chat_t=t.get('chat_t',u['chat_t']),chat_ph=u['chat_ph'],send=u['send'],chat_hello=u['hello'].format(n=d['name']),
          chat_fb=u['fb'].format(c=contact),notice=NOTICE[l],ill=ILL[l],foot=FOOT[l],alts=t['alts'])
        if not d.get('around'): x.pop('around_t',None);x.pop('around_s',None)
        for i,s in enumerate(t.get('stats',[])): x[f'stat{i}']=s
        for i,s in enumerate(t['svcs']): x[f'svc{i}']=s
        for i,(rn,rd) in enumerate(t['rooms']): x[f'room{i}_n']=rn; x[f'room{i}_d']=rd
        kw=u['kw']
        faq=[dict(k=kw['where'],a=t.get('where_a',d['address'])),dict(k=kw['book'],a=ba.format(a=A,c=contact)),dict(k=kw['contact'],a=contact)]
        for k,a in t['faq']: faq.append(dict(k=k,a=a))
        x['faq']=faq
        x['chips']=t.get('chips',[u['chip_where']])+[u['chip_book']]
        i18n[l]=x
    dd=dict(name=d['name'],ac=d['ac'],ac2=d['ac2'],book=urls,hero=d['hero'],intro_img=d['intro_img'],nstats=len(d['t']['es'].get('stats',[])),nsvc=len(d['t']['es']['svcs']),
            rooms=[dict(img=r) for r in d['rooms']],gallery=d['gallery'],around=d.get('around'),address=d['address'],phones=d['phones'],email=d['emails'][0],emails=d['emails'],maps=d['maps'],i18n=i18n,langs=langs)
    render(dd,out)

def render(d,out):
    es=d['i18n']['es'];langs=d['langs']
    def img(n,alt,sizes='100vw',eager=False):
        return (f'<img src="img/{n}-m.webp" srcset="img/{n}-m.webp 800w, img/{n}.webp 1600w" sizes="{sizes}" alt="{html.escape(es["alts"].get(n,""))}" data-alt="{n}"'
                f'{" fetchpriority=high" if eager else " loading=lazy decoding=async"}>')
    rooms=''.join(f'<article class="card">{img(r["img"],"",sizes="(max-width:860px) 100vw, 380px")}<div><h3 data-t="room{i}_n"></h3><p data-t="room{i}_d"></p><a data-book="" href="{html.escape(d["book"]["es"])}" target="_blank" rel="noopener" data-t="room_cta"></a></div></article>' for i,r in enumerate(d['rooms']))
    gal=''.join(img(g,'',sizes='(max-width:860px) 50vw, 300px') for g in d['gallery'])
    extra=''
    if d.get('around'):
        extra='<section><div class="wrap"><h2 data-t="around_t"></h2><p class="sub" data-t="around_s"></p><ul class="chips">'+''.join(f'<li>{html.escape(x)}</li>' for x in d['around'])+'</ul></div></section>'
    stats=''.join(f'<span data-t="stat{i}"></span>' for i in range(d['nstats']))
    svc=''.join(f'<li data-t="svc{i}"></li>' for i in range(d['nsvc']))
    phones=' · '.join(f'<a href="tel:{(p if p.startswith("+") else "+34"+p).replace(" ","")}">{p}</a>' for p in d['phones'])
    mails=' · '.join(f'<a href="mailto:{e}">{e}</a>' for e in d['emails'])
    B=html.escape(d['book']['es'])
    data=dict(i18n=d['i18n'],book=d['book'],roombook={})
    page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(es["title"])}</title><meta name="robots" content="noindex,nofollow"><link rel="icon" href="data:,"><meta name="description" content="{html.escape(es["hero_s"])}">
<link rel="preload" href="fonts/cormorant.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" as="image" href="img/{d["hero"]}-m.webp" imagesrcset="img/{d["hero"]}-m.webp 800w, img/{d["hero"]}.webp 1600w" imagesizes="100vw">
<style>{CSS % dict(ac=d["ac"],ac2=d["ac2"])}</style></head><body>
<div class="notice" role="note" data-t="notice"></div>
<header><div class="wrap nav"><a class="brand" href="#top">{html.escape(d["name"])}</a><nav class="links"><a href="#rooms" data-t="nav_rooms"></a><a href="#services" data-t="nav_svc"></a><a href="#gallery" data-t="nav_gal"></a><a href="#contact" data-t="nav_loc"></a></nav>
<div class="langs" role="group" aria-label="Idioma / Language">{"".join(f'<button type="button" data-l="{l}" aria-pressed="false">{LN[l]}</button>' for l in langs)}</div>
<a class="btn" data-book="" href="{B}" target="_blank" rel="noopener" data-t="book"></a></div></header>
<main id="top"><section class="hero" style="padding:0">{img(d["hero"],d["name"],eager=True)}<div class="wrap"><div class="kick" data-t="hero_k"></div><h1 data-t="hero_t"></h1><p data-t="hero_s"></p>
<div class="cta"><a class="btn" data-book="" href="{B}" target="_blank" rel="noopener" data-t="book_long"></a><a class="btn ghost" href="#rooms" data-t="see_rooms"></a></div></div><span class="ill" data-t="ill"></span></section>
<section><div class="wrap intro"><div><div class="kick" style="color:var(--ac)" data-t="intro_k"></div><h2 data-t="intro_t"></h2><p data-t="intro_p1"></p><p data-t="intro_p2"></p><div class="stats">{stats}</div></div>{img(d["intro_img"],"",sizes="(max-width:860px) 100vw, 480px")}</div></section>
<section class="alt" id="rooms"><div class="wrap"><h2 data-t="rooms_t"></h2><p class="sub" data-t="rooms_s"></p><div class="grid">{rooms}</div></div></section>
<section id="services"><div class="wrap"><h2 data-t="svc_t"></h2><ul class="svc">{svc}</ul></div></section>
<section class="alt" id="gallery"><div class="wrap"><h2 data-t="gal_t"></h2><div class="gal">{gal}</div></div></section>
{extra}
<section id="contact"><div class="wrap loc"><div><h2 data-t="loc_t"></h2><p data-t="loc_p"></p><p><a class="btn ghost" style="color:var(--ac)!important" href="https://www.google.com/maps/search/?api=1&amp;query={up.quote(d["maps"])}" target="_blank" rel="noopener" data-t="map"></a></p></div>
<div class="box"><h3 data-t="contact_t"></h3><p>{html.escape(d["address"])}</p><p>{phones}</p><p>{mails}</p><p style="margin-top:18px"><a class="btn" data-book="" href="{B}" target="_blank" rel="noopener" data-t="book_long"></a></p></div></div></section></main>
<footer><div class="wrap"><strong>{html.escape(d["name"])}</strong><br>{html.escape(d["address"])} · {phones} · {mails}
<div class="demo"><strong data-t="notice"></strong> · <span data-t="foot"></span></div></div></footer>
<div class="sticky"><a class="btn" data-book="" href="{B}" target="_blank" rel="noopener" data-t="book_long"></a></div>
<button id="chatb" aria-label="Chat">💬</button><div id="chat" role="dialog" aria-label="Chat"><header><span data-t="chat_t"></span><button id="chatx" aria-label="Cerrar">×</button></header><div id="msgs"></div><div id="qs"></div><form><input id="q" autocomplete="off" aria-label="Pregunta"><button data-t="send"></button></form></div>
<script>{JS.replace("__DATA__",json.dumps(data,ensure_ascii=False))}</script></body></html>'''
    import re as _re
    page=_re.sub(r'(<(\w+)[^>]*data-t="(\w+)"[^>]*>)</\2>',lambda m:m.group(1)+str(es.get(m.group(3),''))+'</'+m.group(2)+'>',page)
    open(out+'/index.html','w').write(page)
    open(out+'/robots.txt','w').write('User-agent: *\nDisallow: /\n')
    keys=set(d['i18n']['es'])
    for l in langs: assert set(d['i18n'][l])==keys,(l,keys^set(d['i18n'][l]))
