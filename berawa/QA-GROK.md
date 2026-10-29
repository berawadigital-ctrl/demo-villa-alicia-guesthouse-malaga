# QA Grok · villa-alicia-guesthouse-malaga

Autocontrol de fabricación (G04, A1–A11) y checklist C01–C16 (`docs/BERAWA-QA-CHECKLIST.md`) pasados por Grok antes del PR. **No es una auditoría independiente ni una aprobación**: Codex solo audita una muestra y nada se publica ni se envía sin visto bueno de Juan.

- Rama: `demo/villa-alicia-guesthouse-malaga` · HEAD de las pruebas: `8e998b9a010cf13e35690a00e64f3dc7ce453cb6` · fecha: 29/10/2026 15:05 (Europe/Madrid)
- Entorno: Chromium de Playwright (instalado por `playwright install chromium` en el clon limpio), axe-core 4.14.0, Lighthouse 13.6.0 (3 pasadas, mediana).
- Resultado: **QA_GROK_PASS**
- Negocio medido: Maps 4.3 (LEIDA, coincide tel, web) · web original: LCP > 4 s · titular Unión Familiar Malacitana de Inversiones, S.L. (persona jurídica, sin cadena).

## Controles A1–A11
| Nº | Control | Resultado | Evidencia |
|---|---|---|---|
| A1 | Idiomas ES/CA/EN/FR (nunca DE) | **CUMPLE** | qa/chat-i18n.json, qa/file-chat-i18n.json (data-t = traducción; sin alemán) |
| A2 | Chatbot con knowledge.json (citas, cifras, 4+ preguntas por idioma, desconocida, forzar invención, reserva, claves ambiguas = 0) | **CUMPLE** | qa/check_kb.txt, qa/chat-i18n.json, keys_test en qa/run_checks-zip.txt y qa/clon-limpio.txt |
| A3 | Accesibilidad: axe sin violaciones (2 viewports × 4 idiomas × inicio/menú/chat), Lighthouse accesibilidad ≥ 95, teclado, contraste sobre foto ≥ 4,5 | **CUMPLE** | qa/axe-teclado.json, qa/contraste.json, qa/lighthouse-3pasadas.json |
| A4 | Seguridad: sin innerHTML con datos, noopener noreferrer, sin terceros, CSP por meta probada | **CUMPLE** | qa/seguridad.json |
| A5 | Datos con fuente y fecha; leídas todas las fichas | **CUMPLE** | berawa/sources.json, berawa/evidence/source-text.json, berawa/evidence/captacion.json |
| A6 | Imágenes: ninguna del negocio; manifiesto con hash, origen y licencia | **CUMPLE** | berawa/asset_manifest.json (todo origin=generated + fuente OFL), LICENSES.md |
| A7 | Entrega: ZIP determinista, descomprimido y probado por HTTP y file://, idéntico a la rama | **CUMPLE** | qa/run_checks-zip.txt, qa/zip/, resumen.json (sha256 del ZIP, 0 ficheros distintos) |
| A8 | Trazabilidad: un commit por bloque; scripts y evidencias commiteados; cambios V1.0 aparte | **CUMPLE** | git log de la rama; berawa/V1.0-CAMBIOS.md |
| A9 | Precios del chatbot: REGLA DE PRECIOS: CUMPLE | **CUMPLE** | qa/check_kb.txt, qa/check_kb-zip.txt |
| A10 | Reproducibilidad: clon limpio + dependencias documentadas + run_checks --file en verde; rg /workspace vacío | **CUMPLE** | qa/clon-limpio.txt, qa/rg-workspace.txt |
| A11 | git diff --check main...HEAD sin salida | **CUMPLE** | qa/git-diff-check.txt |

## Checklist C01–C16
| Código | Control | Resultado | Evidencia |
|---|---|---|---|
| C01 | Repositorio y SHA | **CUMPLE** | HEAD del clon limpio = 8e998b9a010cf13e35690a00e64f3dc7ce453cb6 (el SHA final del PR es el del commit que añade este informe) |
| C02 | Identidad y fuentes | **CUMPLE** | nombre, teléfono, dirección y datos comerciales con cita literal en berawa/knowledge.json; titular persona jurídica sin cadena y nota de Maps en berawa/evidence/captacion.json |
| C03 | Licencias | **CUMPLE** | asset_manifest.json: ilustraciones propias generadas (origin=generated) y fuente Cormorant OFL; ninguna imagen, logo ni vídeo del negocio |
| C04 | Diseño personalizado y no suplantador | **CUMPLE** | paleta e ilustraciones propias, aviso «Propuesta de rediseño independiente, no oficial» arriba y en el pie, sin logo ni marca del negocio; revisión visual de qa/capturas/ |
| C05 | Móvil 375 px en navegador real | **CUMPLE** | qa/capturas/movil-*.png; desbordamiento horizontal 0 px; axe y teclado en 375 px |
| C06 | Escritorio 1280 px en navegador real | **CUMPLE** | qa/capturas/escritorio-*.png; desbordamiento horizontal 0 px; axe y teclado en 1280 px |
| C07 | Español completo, botones y chatbot | **CUMPLE** | qa/chat-i18n.json (es) |
| C08 | Catalán completo, botones y chatbot | **CUMPLE** | qa/chat-i18n.json (ca) |
| C09 | Inglés completo, botones y chatbot | **CUMPLE** | qa/chat-i18n.json (en) |
| C10 | Francés completo, botones y chatbot | **CUMPLE** | qa/chat-i18n.json (fr) |
| C11 | Chatbot: conocida, sinónimo, desconocida y prohibición de inventar | **CUMPLE** | tests por idioma: preguntas conocidas con otras palabras, 2 desconocidas con respuesta «No dispongo de esa información», petición de confirmar disponibilidad (no la confirma) |
| C12 | CTA con destinos reales, sin falsa reserva | **CUMPLE** | solo mailto:, tel: y enlaces a páginas de reserva del propio negocio (project.json → book); sin motor propio; sec_scan |
| C13 | Transparencia: aviso demo no oficial y noindex | **CUMPLE** | aviso visible en los 4 idiomas, meta robots noindex,nofollow y robots.txt Disallow: / |
| C14 | Seguridad: sin secretos, XSS ni recolección engañosa | **CUMPLE** | qa/seguridad.json; el sitio no recoge datos |
| C15 | Entrega: ZIP, descomprimir, servir y navegar fuera de GitHub Pages | **CUMPLE** | qa/run_checks-zip.txt (HTTP y file:// sobre el ZIP descomprimido) |
| C16 | Rendimiento medido (Lighthouse 3 pasadas, mediana) | **CUMPLE** | qa/lighthouse-3pasadas.json · SEO < 90 por el `noindex,nofollow` y el `robots.txt` con `Disallow: /` (is-crawlable y robots-txt), exigidos por la V1.0; no se maquilla. |

## Lighthouse (mediana de 3 pasadas)
| | Rendimiento | Accesibilidad | Buenas prácticas | SEO |
|---|---|---|---|---|
| Móvil | 100 | 100 | 100 | 58 |
| Escritorio | 100 | 100 | 100 | 58 |

SEO < 90 por el `noindex,nofollow` y el `robots.txt` con `Disallow: /` (is-crawlable y robots-txt), exigidos por la V1.0; no se maquilla.

## Límites
- No probado en Safari ni Firefox ni con lector de pantalla.
- Las imágenes son ilustraciones propias: no muestran el establecimiento y así se rotulan.
- Tiempo del autocontrol automático (ZIP, clon limpio, Lighthouse, capturas): 7.7 min.
