# BERAWA — Checklist obligatoria por commit

**Identificadores:** negocio, repositorio, URL publicada, PR, SHA auditado, fecha, auditor, fuentes consultadas, entorno y versión del navegador.

Para cada control anotar `PASS`, `FAIL` o `NO_VERIFICADO`, adjuntando evidencia (captura, archivo/línea, comando reproducible o URL).

| Código | Control | Exigencia |
|---|---|---|
| C01 | Repositorio y SHA | Confirmar HEAD y versión visible |
| C02 | Identidad y fuentes | Nombre, teléfono, dirección y datos comerciales respaldados |
| C03 | Licencias | Origen y derechos de imágenes, fuentes y logotipos |
| C04 | Diseño | Personalizado y no suplantador |
| C05 | Móvil | Navegador real a 375 px |
| C06 | Escritorio | Navegador real a 1280 px |
| C07 | Español | Completo, botones y chatbot |
| C08 | Catalán | Completo, botones y chatbot |
| C09 | Inglés | Completo, botones y chatbot |
| C10 | Francés | Completo, botones y chatbot |
| C11 | Chatbot | Respuesta conocida, sinónimo, desconocido y prohibición de inventar |
| C12 | CTA | Destinos reales, sin falsa reserva |
| C13 | Transparencia | Aviso demo no oficial y noindex |
| C14 | Seguridad | Sin secretos, XSS ni recolección engañosa |
| C15 | Entrega | ZIP, descomprimir, servir y navegar fuera de GitHub Pages |
| C16 | Rendimiento | Medir o declarar NO_VERIFICADO |

**Salida formal:**
- `APROBADA_TECNICAMENTE`: 16 controles críticos superados; evidencias verificadas.
- `CORREGIR`: fallos reparables, con pasos exactos.
- `RECHAZADA`: fallo grave que exige rehacer.
- `BLOQUEADA_POR_FALTA_DE_EVIDENCIA`: faltan medios o documentación para aprobar.

El informe debe incluir errores priorizados P0-P3, acciones para Grok y los resultados realmente comprobados. Nada de `PASS` sin evidencias.

## Referencia piloto
La demo histórica Cazorla Rural está en GitHub Pages; utiliza ES/EN/FR/DE. Es un **caso de prueba**: el requisito CA falla, por tanto no debe recibir `APROBADA_TECNICAMENTE` hasta que se corrija y el nuevo SHA se vuelva a auditar.
