# Instrucciones del repositorio para GitHub Copilot

Contexto persistente que **todos** los agentes de este repo deben tener en cuenta.

## Qué es este proyecto
POC de **agentes nativos de GitHub Copilot** automatizados con GitHub Actions. Al
etiquetar un issue (`auto-*`), un workflow despacha al agente adecuado, que trabaja y
abre un Pull Request. La demo es **FinCalc**, una mini-suite de calculadoras estática
(`web/`) desplegada en GitHub Pages.

## Estructura
- `.github/agents/*.md` — agentes personalizados (roles).
- `.github/skills/*/SKILL.md` — skills (playbooks reutilizables).
- `.github/workflows/despacho-agentes.yml` — mapea etiqueta → agente y lo lanza.
- `.github/workflows/deploy-pages.yml` — publica `web/` en GitHub Pages.
- `web/` — la app FinCalc (HTML/CSS/JS **sin build**, sin dependencias externas).
- `web/app.js` — lógica: **funciones puras** (calc/validación) + cableado del DOM aislado.
- `web/app.test.js` — tests con el runner nativo de Node.

## Cómo construir y probar
- **No hay paso de build**: la web es estática; se abre `web/index.html` directamente.
- **Tests**: `npm test` (ejecuta `node --test web/app.test.js`). Debe quedar en verde.
- Para servir la web en local: `cd web && python3 -m http.server 8080`.

## Convenciones (impórtalas siempre)
- **Cambios de código solo por Pull Request**; nunca escribas directo en `main`.
- **No modifiques** `.github/workflows/*`, secretos ni credenciales.
- Mantén las **funciones de cálculo puras** (sin DOM) para que sigan siendo testeables;
  el acceso al DOM va guardado por `typeof document !== "undefined"`.
- Si añades/ajustas lógica, **añade o actualiza los tests** en `web/app.test.js`.
- Respeta el estilo existente (español en textos de UI, formato € con `Intl`).
- Cambios mínimos y acotados: una mejora por PR.

## Uso de herramientas (MCP)
- Tienes disponible **Playwright** (navegador) y, si está configurado, **Context7**.
- Cuando uses o ajustes una API de librería/framework (p. ej. Playwright, APIs del
  navegador), **consulta Context7** para usar la sintaxis correcta y actual en vez de
  suponerla.
