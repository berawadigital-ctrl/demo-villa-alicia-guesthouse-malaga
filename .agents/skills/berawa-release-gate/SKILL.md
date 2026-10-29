---
name: berawa-release-gate
description: Verificar si una demo auditada por Codex está realmente lista para revisión comercial por Juan. Exige auditoría integral aprobada vinculada al SHA, sin permitir envíos automáticos.
---

# Puerta independiente de publicación comercial

Antes de dar `READY_FOR_JUAN_REVIEW`, comprobar **todas** estas condiciones:
- El SHA del código actual coincide exactamente con el SHA auditado.
- Hay dictamen **APROBADA_TECNICAMENTE** emitido por un proceso de Codex identificable, con informe y evidencias que Grok no pueda sustituir sin detección.
- La auditoría incluye prueba de navegador real, ES/CA/EN/FR, chatbot, hechos comerciales, licencias, CTA y ZIP local.
- No hay fallos críticos ni pruebas obligatorias sin verificar.
- La URL de muestra corresponde al código auditado y está identificada como propuesta no oficial.
- Se conservan referencias de revisión y hallazgos, y no hubo commits posteriores.

Si algo falla, devolver `BLOCKED` con motivos concretos. No inferir aprobación por una etiqueta, comentario de Grok o resultado parcial de CI.

`READY_FOR_JUAN_REVIEW` **no significa** `CONTACT_APPROVED`. Solo Juan decide si contactar, previa comprobación de la base jurídica del canal. No enviar mensajes ni activar recordatorios desde esta Skill.
