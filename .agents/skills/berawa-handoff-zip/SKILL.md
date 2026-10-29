---
name: berawa-handoff-zip
description: Empaquetar y comprobar la entrega de una landing estática de Berawa Solutions en ZIP portable, con HTML/CSS/JS, 4 idiomas y chatbot local. Usar durante la auditoría o al preparar entrega al cliente.
---

# Control de portabilidad y ZIP

1. Identificar el directorio que se publicaría, con `index.html` en raíz; no asumir que la raíz del repositorio es la web final si existe compilación.
2. Verificar que todos los recursos necesarios sean entregables legalmente, que no haya secretos y que no existan dependencias de APIs privadas o servicios de pago para idioma/chatbot.
3. Crear un ZIP del **sitio desplegable**, excluyendo `.git`, informes internos, credenciales, archivos de acceso y documentación comercial sensible. Si existen fuentes editables y hay un proceso de compilación, conservar también las fuentes por separado.
4. Descomprimir el ZIP en una carpeta temporal limpia. Servir el contenido mediante un servidor HTTP estático local.
5. Abrir en navegador y comprobar carga de CSS, fotografías y tipografías, navegación, botones, ES/CA/EN/FR y el chatbot; verificar que funcione sin GitHub Pages.
6. Crear `INSTALACION.md` con requisitos, pasos de subida al directorio público del hosting estático, comprobaciones posteriores y limitaciones de compatibilidad.
7. Reportar tamaño, archivos incluidos, prueba de apertura y errores. Si alguna parte no se ha comprobado, dar estado **NO VERIFICADO** y no certificar portabilidad.

La instalación en hosting del cliente solo puede realizarse con autorización, credenciales canalizadas de manera segura, respaldo y compatibilidad confirmada. No modificar DNS ni publicar por iniciativa propia.
