"""Escribe berawa/asset_manifest.json, berawa/evidence/assets/*.txt, berawa/project.json y LICENSES.md a partir de content_<slug>.py.
Las imagenes son ilustraciones propias generadas por make_art.py (sin material del negocio): todo es reproducible desde el repo."""
import json,hashlib,datetime
from _rutas import ROOT
from content_villa_alicia_guesthouse_malaga import META,ART,D
R=ROOT
NOW=META['built_at']
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
(R/'berawa/evidence/assets').mkdir(parents=True,exist_ok=True)
LIC='Ilustracion propia de Berawa Solutions, generada por berawa/build/make_art.py (Pillow): sin fotos, logos ni textos de terceros; uso libre para esta propuesta.'
assets=[]
for k,(kind,seed,pal) in ART.items():
    ev=f'berawa/evidence/assets/{k}.txt'
    ph=hashlib.sha256(json.dumps([kind,seed,pal]).encode()).hexdigest()
    (R/ev).write_text(f"Ilustracion generada por codigo (make_art.py), tipo '{kind}', semilla {seed}, paleta {pal}.\nSin fotografias ni logotipos: no muestra el establecimiento.\nHash de los parametros: {ph}\nLicencia: {LIC}\n")
    for suf in ('','-m'):
        p=f'img/{k}{suf}.webp'
        assets.append(dict(path=p,sha256=sha(R/p),origin='generated',source_url=None,title=f'Ilustracion {kind} ({k})',author='Berawa Solutions',license='Propia (generada por script)',license_url=None,attribution_required=False,attribution_text=None,modified=False,depicts_real_business=False,shown_label='Imagen ilustrativa',tool='berawa/build/make_art.py (Pillow)',prompt_sha256=ph,retrieved_at=NOW,evidence=ev))
(R/'berawa/evidence/assets/font.txt').write_text('Cormorant (Christian Thalmann, Catharsis Fonts), SIL OFL 1.1: uso comercial y redistribucion permitidos. Fichero fonts/cormorant.woff2. Licencia: https://openfontlicense.org/\n')
assets.append(dict(path='fonts/cormorant.woff2',sha256=sha(R/'fonts/cormorant.woff2'),origin='font',source_url='https://github.com/CatharsisFonts/Cormorant',author='Christian Thalmann (Catharsis Fonts)',license='SIL OFL 1.1',license_url='https://openfontlicense.org/',attribution_required=False,attribution_text=None,modified=False,depicts_real_business=False,retrieved_at=NOW,evidence='berawa/evidence/assets/font.txt'))
json.dump(dict(schema='berawa-asset-manifest/1',project=META['repo'],generated_at=NOW,note='Ninguna foto, logo, video ni testimonio del negocio. Las imagenes son ilustraciones propias generadas por codigo y se rotulan como ilustrativas.',assets=assets),open(R/'berawa/asset_manifest.json','w'),ensure_ascii=False,indent=1)
P=dict(schema='berawa-project/1',slug=META['repo'],template_version='webfactory-2026.10.28+modelo-cazorla-6cfa67d',created_at=META['created_at'],updated_at=NOW,
 business=dict(name=META['name'],legal_name=META.get('legal_name'),registry_ids=META.get('registry_ids',[]),url=META['url'],domain=META['domain'],municipality=META['municipality'],province=META['province'],address=D['address'],phones=D['phones'],emails=D['emails'],sector=META['sector']),
 rating=dict(value=META['rating']['value'],source='Google Maps (maps_rating.py, ficha comprobada por '+', '.join(META['rating']['coincide'])+')',url=META['rating']['url'],date=META['rating']['date'],threshold=4.0),
 languages=['es','ca','en','fr'],noindex=True,notice_es='Propuesta de rediseño independiente, no oficial',
 chatbot=dict(api=False,kind='base local de respuestas verificadas',knowledge='berawa/knowledge.json',fallback_es='No dispongo de esa información'),
 book=META['book'],audit_original=dict(url=META['url'],date=META['audit_date'],veredicto='LCP > 4 s',tool='filtro_mala_web.py (Lighthouse movil, mediana de 3 pasadas)'),
 first_of_type=META.get('first_of_type'),codex=dict(audits=[]),changes_log='ver CORRECCIONES.md (si existe) y berawa/V1.0-CAMBIOS.md')
json.dump(P,open(R/'berawa/project.json','w'),ensure_ascii=False,indent=1)
print(len(assets),'activos')
