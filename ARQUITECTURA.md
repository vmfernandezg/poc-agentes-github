# 🧱 Arquitectura del proyecto

Esta POC tiene **dos flujos de agentes** complementarios:

1. **Pipeline didáctico de 6 agentes** (analiza un issue y publica informe + etiquetas).
2. **Despacho nativo por etiquetas** (dispara agentes de Copilot y abre PR).

---

## 1) Componentes principales

| Ruta | Rol en la arquitectura |
|---|---|
| `agentes/roles.py` | Define los 6 agentes (sus prompts y formato de salida). |
| `agentes/orquestador.py` | Encadena agentes en serie y mantiene el "expediente" compartido. |
| `agentes/github_tools.py` | Herramientas: leer repo local + leer/comentar/etiquetar issues vía API. |
| `agentes/llm.py` | Crea el cliente compatible OpenAI (clave, modelo, base URL opcional). |
| `run_local.py` | Ejecuta el pipeline en local con issue simulado (sin publicar en GitHub). |
| `run_actions.py` | Ejecuta el pipeline sobre issue real y publica resultado. |
| `.github/workflows/agentes.yml` | Disparador del pipeline de 6 agentes (issues nuevos o `/agentes`). |
| `.github/workflows/despacho-agentes.yml` | Mapea etiquetas `auto-*` a agentes nativos de Copilot. |
| `.github/agents/*.md` | Instrucciones de los agentes nativos (`corrige-bugs`, `documenta`, etc.). |

---

## 2) Flujo A: pipeline de 6 agentes (v1 didáctica)

Disparadores (`agentes.yml`):
- `issues: opened`
- `issue_comment: created` cuando el comentario contiene `/agentes`

Secuencia:
1. `run_actions.py` lee el issue real (`leer_issue`).
2. `orquestador.py` ejecuta, en orden: **Triage → Contexto → Planner → Coder → Revisor → Reporter**.
3. Reporter genera el informe final en Markdown.
4. Se publica en el issue: comentario + etiquetas.

Notas de diseño:
- La orquestación es **en serie** para que el flujo sea fácil de entender.
- El agente **Revisor** actúa como control de calidad del **Coder**.
- `Triage` puede cortar el pipeline si detecta spam o issue vacío.

---

## 3) Flujo B: despacho por etiquetas (v2 nativa)

Disparador (`despacho-agentes.yml`):
- `issues: labeled` cuando la etiqueta empieza por `auto-`.

Mapa actual:
- `auto-fix` → `corrige-bugs`
- `auto-feature` → `implementa-feature`
- `auto-tests` → `escribe-tests`
- `auto-docs` → `documenta`
- `auto-review` → `revisa-codigo`

Secuencia:
1. El workflow traduce etiqueta → agente.
2. Construye un prompt con el issue.
3. Llama a `POST /agents/repos/{owner}/{repo}/tasks`.
4. El agente nativo trabaja en la nube y abre un PR.
5. El workflow deja comentario de confirmación en el issue.

Requisito clave:
- Este flujo necesita `COPILOT_AGENT_PAT` (token de usuario).  
  `GITHUB_TOKEN` no sirve para esa API.

---

## 4) Configuración y secretos

### Local (`run_local.py`)
- `.env` con:
  - `OPENAI_API_KEY` (obligatoria)
  - `OPENAI_MODEL` (opcional, por defecto `gpt-4o-mini`)
  - `OPENAI_BASE_URL` (opcional, proveedor compatible)

### GitHub Actions (`agentes.yml`)
- Secret: `OPENAI_API_KEY`
- Variable opcional: `OPENAI_MODEL`
- Automáticas del workflow: `GH_TOKEN`, `REPO`, `ISSUE_NUMBER`

### GitHub Actions (`despacho-agentes.yml`)
- Secret: `COPILOT_AGENT_PAT`

---

## 5) Límites intencionales de la POC

- El pipeline de 6 agentes **no abre PR**; publica análisis en issues.
- El flujo nativo sí puede abrir PR, pero depende de la API de tareas de agentes.
- La calidad final depende de prompts + contexto disponible en repo.

Para una vista más visual del flujo, consulta [`DIAGRAMA.md`](DIAGRAMA.md).
