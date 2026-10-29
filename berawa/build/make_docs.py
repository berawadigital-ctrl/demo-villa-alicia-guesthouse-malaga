"""Escribe README.md, INSTALACION.md, LICENSES.md y berawa/V1.0-CAMBIOS.md a partir de content_<slug>.py (META, ART, D). Determinista."""
from _rutas import ROOT
from content_villa_alicia_guesthouse_malaga import META,ART,D
n=META['name'];dom=META['domain'];rd=META['read_at'][:10].split('-');rd='/'.join(reversed(rd))
rat=META['rating'];rf=rat['date'][:10].split('-');rf='/'.join(reversed(rf))
ph=D['phones'][0];ma=D['emails'][0]
(ROOT/'README.md').write_text(f"""# {n} · propuesta de rediseño (demo)

**Propuesta de rediseño independiente, no oficial.** Hecha por Berawa sin encargo del negocio. No es la web de {n} ni está afiliada a ella. Lleva `noindex,nofollow`.

Sitio estático (HTML + CSS + JS, sin servidor ni APIs ni servicios de terceros) en español, catalán, inglés y francés, con un asistente local que responde solo con datos publicados en {dom} (`berawa/knowledge.json`, con la fuente y una cita literal por respuesta).

## Ver en local
```
python3 -m http.server 8000      # y abrir http://localhost:8000
```
También funciona abriendo `index.html` directamente. Detalle de instalación en `INSTALACION.md`.

## Comprobaciones
Ver `berawa/build/README.md` (un solo comando: `python3 berawa/build/run_checks.py --file`).

## Trazabilidad
- `berawa/project.json`: datos del negocio, nota de Maps (con fecha), estado de las auditorías.
- `berawa/sources.json` y `berawa/knowledge.json`: de dónde sale cada dato y cada respuesta del chat (lectura del {rd}).
- `berawa/asset_manifest.json` y `LICENSES.md`: cada imagen y fuente con origen, licencia, hash y evidencia.
- `berawa/V1.0-CAMBIOS.md`: reglas de la V1.0 y cómo se cumplen.
""")
(ROOT/'INSTALACION.md').write_text(f"""# Instalación

## Requisitos
Cualquier hosting estático (Apache, Nginx, Netlify, Cloudflare Pages, GitHub Pages, S3…). No necesita PHP, base de datos, Node ni claves de API. Probado con `python3 -m http.server` y abriendo `index.html` desde disco (`file://`) en Chromium.

## Pasos
1. Descomprime `{META['repo']}.zip`.
2. Sube **el contenido** de la carpeta (no la carpeta) al directorio público del hosting: `index.html`, `styles.css`, `app.js`, `robots.txt`, `img/`, `fonts/` y `berawa/`.
3. Abre la URL y comprueba: la página carga con imágenes y tipografía; el selector ES/CA/EN/FR cambia todo el texto; el menú y el botón de reservar funcionan; el asistente responde a la primera pregunta sugerida y dice «No dispongo de esa información» ante algo que no sabe.

## Mientras sea una propuesta
No quites el aviso «Propuesta de rediseño independiente, no oficial» ni el `noindex` (`<meta name="robots">` y `robots.txt`). No publiques bajo el dominio del negocio sin su autorización.

## Seguridad: lo que el hosting debe añadir
El sitio lleva una Content-Security-Policy y una política de referrer por `<meta>`, que cubren casi todo. Las siguientes protecciones **solo funcionan como cabeceras HTTP** y GitHub Pages no permite configurarlas; si el hosting lo permite, añade:
```
X-Content-Type-Options: nosniff
Content-Security-Policy: <la misma del <meta>> ; frame-ancestors 'none'
Referrer-Policy: no-referrer
Permissions-Policy: camera=(), microphone=(), geolocation=()
```
Si cambias el contenido de `index.html`, mantén los scripts y estilos en `app.js` y `styles.css`: la CSP no admite código en línea.

## Limitaciones
- Datos leídos de {dom} el {rd}; precios y condiciones pueden haber cambiado (el asistente avisa de que se confirmen al reservar).
- Reservas: {META['book'].get('note','solo contacto real (teléfono, correo o WhatsApp) o el motor de reservas del propio negocio')} Teléfono {ph} · {ma}. No hay motor de reservas ni disponibilidad en esta demo.
- No se ha probado en Safari ni Firefox ni con lector de pantalla.
- No se toca DNS ni se publica nada por iniciativa propia.
""")
(ROOT/'LICENSES.md').write_text(f"""# Licencias de los activos

| Activo | Origen | Autor | Licencia |
|---|---|---|---|
"""+''.join(f"| img/{k}.webp (+ {k}-m.webp) | Ilustración generada por código (`berawa/build/make_art.py`, tipo `{v[0]}`, semilla {v[1]}) | Berawa Solutions | Propia (generada por script) |\n" for k,v in ART.items())+f"""| fonts/cormorant.woff2 | https://github.com/CatharsisFonts/Cormorant | Christian Thalmann (Catharsis Fonts) | SIL OFL 1.1 |

Ninguna imagen es una foto ni muestra el establecimiento: son ilustraciones propias y se rotulan «Imagen ilustrativa». Detalle por fichero (hash, parámetros de generación) en `berawa/asset_manifest.json` y `berawa/evidence/assets/`.

Los textos proceden de la web pública del negocio ({dom}, leída el {rd}; ver `berawa/sources.json`); no se han copiado sus fotos, logotipos, vídeos ni testimonios.
""")
(ROOT/'berawa'/'V1.0-CAMBIOS.md').write_text(f"""# Cómo cumple esta demo las reglas de la V1.0 de Juan (28/10/2026)

| # | Regla | Dónde | Cómo se comprueba |
|---|---|---|---|
| V1 | Aviso fijo y visible «Propuesta de rediseño independiente, no oficial» (ES/CA/EN/FR) arriba y en el pie, y `noindex,nofollow` | `index.html`, `robots.txt` | `berawa/build/tests_{META['repo'][5:].replace('-','_')}.py` (textos aplicados en los 4 idiomas) y `sec_scan.py` |
| V2 | Ninguna foto, logotipo, vídeo ni testimonio del negocio | `img/` | `berawa/asset_manifest.json`: todo `origin: generated` (o fuente OFL); `rg` de las URLs del negocio en `img/` y HTML: vacío |
| V3 | Imágenes propias generadas por código, rotuladas «Imagen ilustrativa», con aviso en el texto de las habitaciones | `img/`, `index.html` | manifiesto con sha256, herramienta y hash de parámetros; `regenerar.py` reproduce los mismos bytes |
| V4 | Chatbot solo con `berawa/knowledge.json`: cada respuesta con cita literal y URL; sin coincidencia, «No dispongo de esa información» | `berawa/knowledge.json` | `check_kb.py` (citas, cifras y regla de precios P1–P6: fuente con fecha, «según su web», «confírmalo al reservar» en 4 idiomas) |
| V5 | Solo CTA reales: {'correo' if META['book']['mode']=='mail' else META['book']['mode']}, teléfono (`tel:`) y enlaces del propio negocio; sin sistema de reservas propio | `index.html` | `sec_scan.py` y revisión de enlaces |
| V6 | `berawa/project.json` con nota de Maps (valor {rat['value']}, leída el {rf}, coincidencia: {', '.join(rat['coincide'])}) y auditoría original (LCP > 4 s) | `berawa/project.json` | JSON válido; cada dato con su fuente |

{META.get('first_of_type') or ''}
""")
print('docs escritos')
