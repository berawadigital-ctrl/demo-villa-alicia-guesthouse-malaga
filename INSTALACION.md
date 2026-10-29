# Instalación

## Requisitos
Cualquier hosting estático (Apache, Nginx, Netlify, Cloudflare Pages, GitHub Pages, S3…). No necesita PHP, base de datos, Node ni claves de API. Probado con `python3 -m http.server` y abriendo `index.html` desde disco (`file://`) en Chromium.

## Pasos
1. Descomprime `demo-villa-alicia-guesthouse-malaga.zip`.
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
- Datos leídos de guesthousealicia.com el 29/10/2026; precios y condiciones pueden haber cambiado (el asistente avisa de que se confirmen al reservar).
- Reservas: Las reservas van al motor de reservas real del establecimiento (Cloudbeds, /reservation/YMJZTS, el enlace de su boton «Reservar»); la demo no construye ningun motor. Teléfono +34 622 32 24 76 · hola@guesthousealicia.com. No hay motor de reservas ni disponibilidad en esta demo.
- No se ha probado en Safari ni Firefox ni con lector de pantalla.
- No se toca DNS ni se publica nada por iniciativa propia.
