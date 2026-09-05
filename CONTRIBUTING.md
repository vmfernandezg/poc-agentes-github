# 🤝 Guía de contribución

Este repo es una POC de **agentes nativos de GitHub Copilot**. No hay que instalar nada en
local: se trabaja sobre archivos de configuración (`.github/agents/` y workflows) y la web
estática de `web/`.

---

## 1) Añadir o modificar un agente

Los agentes son archivos Markdown en `.github/agents/NOMBRE.md`:

```markdown
---
name: mi-agente
description: Qué hace, en una frase.
---

Eres un agente que... (instrucciones: cómo se comporta, qué produce, qué NO debe tocar).
```

- **Modificar** un agente = editar su `.md`. El cambio aplica en el siguiente despacho.
- **Añadir** un agente nuevo:
  1. Crea `.github/agents/mi-agente.md`.
  2. Añade una etiqueta y su mapeo en `.github/workflows/despacho-agentes.yml`
     (el bloque `case "$LABEL" in ...`).
  3. Crea la etiqueta en el repo: `gh label create auto-mi-agente`.

---

## 2) Probar el flujo de agentes

1. Asegura el secret `COPILOT_AGENT_PAT` (PAT **classic** con scope `repo`).
2. Abre un issue describiendo la tarea.
3. Ponle la etiqueta `auto-*` correspondiente.
4. Revisa el workflow **Despacho de agentes IA** en *Actions* y el **PR** que abre el agente.
5. Revisa el PR y mergéalo si te convence (el agente propone; tú decides).

---

## 3) La web demo (`web/`)

Es una app estática. Para verla en local, abre `web/index.html` en el navegador. Al
mergear cambios en `web/` a `main`, `deploy-pages.yml` la republica en GitHub Pages.

---

## 4) Flujo recomendado

1. Los cambios de código los propone un **agente** vía PR (etiquetando un issue), o los
   haces tú en una rama.
2. Un cambio acotado por PR.
3. PR con: qué cambiaste, por qué y cómo validarlo.
4. Revisión humana antes de merge. Nunca commits directos a `main` para cambios de código.

---

## 5) Dónde tocar según el tipo de mejora

- **Comportamiento de un agente:** `.github/agents/<agente>.md`
- **Qué etiqueta lanza qué agente:** `.github/workflows/despacho-agentes.yml`
- **Despliegue de la web:** `.github/workflows/deploy-pages.yml`
- **La app demo:** `web/`
- **Documentación:** `README.md`, `ARQUITECTURA.md`, `V2-NATIVA.md`, `DEMO-PAGES.md`

Para entender el diseño antes de tocar nada, lee [`ARQUITECTURA.md`](ARQUITECTURA.md).
