---
name: berawa-demo-qa
description: Auditoría técnica independiente de una demo web creada por Grok Bot para Berawa Solutions, con navegador, 4 idiomas, chatbot, contenido, licencias y ZIP. Usar al recibir un PR, un SHA o una solicitud de aprobar una demo. No envía correos.
---

# Auditoría integral de una demo de Berawa Solutions

## Entradas
Repositorio y commit SHA comprobables, enlace publicado, web original del negocio, pruebas o evidencias de los hechos comerciales, licencias de imágenes y resultado del autocontrol de Grok.

Si falta una entrada imprescindible, indicarla y marcar el control correspondiente **NO VERIFICADO**. No inventar evidencias.

## Secuencia
1. Abrir el repositorio y verificar el SHA actual de la rama/PR. Distinguir código evaluado de la versión pública, que podría ser distinta.
2. Examinar `index.html`, CSS, JS y recursos. Identificar dependencias externas, llamadas de red y formularios.
3. Comprobar los requisitos básicos: landing de una sola página; idiomas exactos ES/CA/EN/FR con traducciones completas; CTA auténticos; aviso visible de demo no oficial; exclusión de indexación.
4. Abrir la demo en **navegador real** a 375 px y >=1280 px. Probar desplazamiento, menú, enlaces, imágenes, accesibilidad de controles, ausencia de scroll horizontal y de errores graves de consola.
5. Cambiar entre los cuatro idiomas y probar encabezados, descripciones, servicios, botones, contacto, títulos de documento y chatbot. Verificar que no haya mezclas ni campos vacíos.
6. Probar el chatbot en **cada idioma** con: consulta conocida, sinónimo, pregunta sin respuesta disponible y pregunta que intenta obtener un dato no publicado. Debe responder exclusivamente con datos respaldados y reconocer desconocimiento.
7. Cotejar nombre, contacto y al menos tres afirmaciones sobre el negocio con fuentes fiables y fechadas. No atribuir al sitio original problemas no demostrados.
8. Verificar origen y derechos de cada fotografía, fuente y logotipo usado. Si la autorización/licencia no se acredita, bloquear.
9. Evaluar seguridad (inyección HTML, secretos, enlaces externos, privacidad), rendimiento y requisitos externos.
10. Invocar `$berawa-handoff-zip`. Probar localmente, desde el ZIP descomprimido, el sitio y sus funciones principales. La URL de GitHub Pages no sustituye esta prueba.
11. Completar `docs/BERAWA-QA-CHECKLIST.md` con PASS/FAIL/NO VERIFICADO y pruebas reproducibles; emitir dictamen referido al SHA.

## Dictámenes
- **APROBADA_TECNICAMENTE**: todos los controles críticos PASS, sin información inventada y pruebas de navegador y ZIP realizadas.
- **CORREGIR**: defectos concretos subsanables, con localización y pasos de reproducción.
- **RECHAZADA**: problemas graves de seguridad, falsedad o derechos que impiden continuar sin rehacer el proyecto.
- **BLOQUEADA_POR_FALTA_DE_EVIDENCIA**: faltan pruebas, fuentes, derechos o acceso al entorno.

Nunca aprobar por ausencia de fallos detectados en una inspección incompleta. La aprobación solo habilita **revisión de Juan**, no contacto comercial. Cada nuevo commit invalida la aprobación anterior.
