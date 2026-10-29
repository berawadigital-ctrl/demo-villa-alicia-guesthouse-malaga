# Berawa Solutions — Skills de Codex (piloto)

Estas Skills se han instalado en `.agents/skills/` para este repositorio. El repositorio de la demo puede seguir publicándose mediante GitHub Pages; estas instrucciones NO cambian su diseño ni su contenido.

## Primera prueba
Abre en Codex el repositorio `berawadigital-ctrl/demo-cazorla-rural` y solicita:

> Usa $berawa-demo-qa para auditar el SHA actual de Cazorla Rural conforme a AGENTS.md y docs/BERAWA-QA-CHECKLIST.md. No cambies el sitio ni publiques. Emite dictamen con evidencias y lista de correcciones para Grok.

Las Skills son **de este repositorio**, no globales a todos los repositorios de la cuenta. Para que funcionen en otros proyectos de Grok, habrá que incluirlas también allí o instalarlas globalmente en el entorno Codex; conectar GitHub no las replica automáticamente.

## Cómo trabajar con Grok
1. Grok fabrica demo y abre PR con el sitio y fuentes.
2. Code Review automático de Codex requiere activación independiente en ajustes de Codex; o puede pedirse `@codex review` en un PR. Esa revisión normal **no es la auditoría integral**.
3. Ejecuta además `$berawa-demo-qa` con acceso al entorno de navegador y código.
4. Si la QA falla, Grok corrige en nuevo commit y vuelve a pedir QA.
5. Usa `$berawa-release-gate` para pasar solo resultados aprobados a Juan.
6. Juan decide el contacto; estas Skills NO envían correos.

No se ha activado aquí ningún cron, ningún acceso a Gmail, ninguna acción de borrado ni un mecanismo automático de aprobación. La coordinación automática Grok→Codex se valida en una fase posterior.
