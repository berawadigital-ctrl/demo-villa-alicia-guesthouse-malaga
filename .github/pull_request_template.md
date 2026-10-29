## Resumen
<!-- Qué cambia y por qué, en 3 líneas. -->

## Hallazgos de Codex que corrige
<!-- Un id por línea: F-001 · severidad · qué se hizo · commit -->

## SHA para auditar
`<SHA completo de 40 caracteres del último commit>`  (la aprobación vale solo para este SHA)

## Autocontrol G04 (con evidencia enlazada)
- [ ] Idiomas ES/CA/EN/FR completos, sin restos de otros idiomas
- [ ] Chatbot: conocida / sinónimo / desconocida / intento de inventar, en los 4 idiomas
- [ ] Accesibilidad: axe sin violaciones, Lighthouse accesibilidad ≥ 95, teclado y foco
- [ ] Seguridad: sin innerHTML con datos, `rel="noopener noreferrer"`, sin terceros, CSP, cabeceras comprobadas con `curl -I`
- [ ] Entrega: ZIP descomprimido y probado por HTTP y `file://`
- [ ] Datos comerciales sin cambios no justificados (fuente y fecha)
- [ ] Aviso «Propuesta de rediseño independiente, no oficial» visible y `noindex`
- [ ] Fotos con licencia y `berawa/asset_manifest.json`

## Cambios de la V1.0 (aparte de lo que pidió Codex)
<!-- Lista corta, con enlace a berawa/V1.0-CAMBIOS.md -->

## No resuelto / no verificado
<!-- Honesto: qué queda y por qué. -->

## Pedir la re-auditoría
Pegar en Codex el prompt de `docs/CODEX-PROMPT-AUDITORIA.md` con `{REPO}`, `{SHA}` y `{PR}`.
Devuelve informe para personas + JSON de correcciones (`berawa-codex-audit/1`).

**No hacer merge sin dictamen APROBADA_TECNICAMENTE de este SHA y visto bueno de Juan: `main` publica en GitHub Pages.**
