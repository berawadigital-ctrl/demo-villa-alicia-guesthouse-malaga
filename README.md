# Villa Alicia Guest House · propuesta de rediseño (demo)

**Propuesta de rediseño independiente, no oficial.** Hecha por Berawa sin encargo del negocio. No es la web de Villa Alicia Guest House ni está afiliada a ella. Lleva `noindex,nofollow`.

Sitio estático (HTML + CSS + JS, sin servidor ni APIs ni servicios de terceros) en español, catalán, inglés y francés, con un asistente local que responde solo con datos publicados en guesthousealicia.com (`berawa/knowledge.json`, con la fuente y una cita literal por respuesta).

## Ver en local
```
python3 -m http.server 8000      # y abrir http://localhost:8000
```
También funciona abriendo `index.html` directamente. Detalle de instalación en `INSTALACION.md`.

## Comprobaciones
Ver `berawa/build/README.md` (un solo comando: `python3 berawa/build/run_checks.py --file`).

## Trazabilidad
- `berawa/project.json`: datos del negocio, nota de Maps (con fecha), estado de las auditorías.
- `berawa/sources.json` y `berawa/knowledge.json`: de dónde sale cada dato y cada respuesta del chat (lectura del 29/10/2026).
- `berawa/asset_manifest.json` y `LICENSES.md`: cada imagen y fuente con origen, licencia, hash y evidencia.
- `berawa/V1.0-CAMBIOS.md`: reglas de la V1.0 y cómo se cumplen.
