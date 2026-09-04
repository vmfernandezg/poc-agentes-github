# POC: Equipo de 6 agentes de IA sobre GitHub (Actions + OpenAI)

> Una prueba de concepto **ejecutable** para aprender, viéndolo funcionar, cómo se
> construye y orquesta un sistema **multi-agente** que corre dentro de **GitHub Actions**
> y actúa sobre tu repositorio real (lee issues, comenta, pone etiquetas).

---

## 0. Lo primero: aclaremos "agentes de GitHub" (esto ya es aprendizaje)

Cuando la gente dice "los agentes de GitHub" suele mezclar cosas muy distintas:

| Nombre | Qué es | ¿Es esto? |
|--------|--------|-----------|
| **GitHub Copilot – Agent Mode** | *Un* asistente que edita tu código iterando dentro del editor | No |
| **GitHub Copilot Coding Agent** | Le asignas un *issue* y te abre un PR solo (producto cerrado de GitHub) | No |
| **GitHub Models** | Antiguo acceso gratis a modelos de IA con tu token de GitHub | **Murió el 30-jul-2026** |
| **GitHub Actions** | Automatización/CI que reacciona a eventos del repo | Sí, es el *motor* de esta POC |

**Dato clave (sep. 2026):** *GitHub Models fue retirado por completo el 30 de julio de 2026.*
GitHub ahora te dirige a **Azure AI Foundry** (para acceso a modelos) o a **GitHub Copilot**
(para features agénticos ya hechos). Por eso esta POC **no usa GitHub Models**: usa un
proveedor compatible con OpenAI (aquí, **OpenAI**), pero el código está escrito de forma
**agnóstica** para que puedas cambiar de proveedor tocando 2 variables.

> **La idea que quiero que te lleves:** "un agente" no es magia ni un producto. Es
> **un rol (system prompt) + una llamada a un modelo + herramientas para actuar**.
> Un "sistema multi-agente" es simplemente **varios de esos** especializados y
> **orquestados** (encadenados, y con unos revisando el trabajo de otros).

## Guías rápidas del repo

- **Arquitectura:** [`ARQUITECTURA.md`](ARQUITECTURA.md)
- **Cómo contribuir:** [`CONTRIBUTING.md`](CONTRIBUTING.md)
- **Diagrama visual:** [`DIAGRAMA.md`](DIAGRAMA.md)

---

## 1. Qué hace la POC

Cuando abres un **issue** en tu repo (o comentas `/agentes` en uno existente), GitHub
Actions arranca un pipeline de **6 agentes** que se pasan el trabajo en cadena:

```
   Nuevo issue  ─────────────────────────────────────────────► GitHub Actions
        │
        ▼
  ┌───────────┐   ┌────────────┐   ┌───────────┐   ┌─────────┐   ┌────────────┐   ┌────────────┐
  │ 1. TRIAGE │──▶│ 2. CONTEXTO│──▶│ 3. PLANNER│──▶│4. CODER │──▶│5. REVISOR  │──▶│ 6. REPORTER│
  │ clasifica │   │ lee el repo│   │ descompone│   │ propone │   │ critica el │   │ redacta y  │
  │ y decide  │   │ (tool real)│   │ en pasos  │   │ un fix  │   │ trabajo    │   │ PUBLICA    │
  └───────────┘   └────────────┘   └───────────┘   └─────────┘   └────────────┘   └─────┬──────┘
                                                                                         │
                                                                 comentario + etiquetas ▼
                                                                              en tu issue real
```

- **Cada caja es un agente** = 1 llamada al modelo con un system prompt distinto.
- La **salida de uno alimenta al siguiente** (esto es "orquestación por pipeline").
- El **Revisor critica al Coder** → patrón clave: *un agente supervisa a otro*.
- El **Reporter usa herramientas reales**: comenta en el issue y aplica etiquetas.
- El **Contexto también usa una herramienta real**: lee archivos de tu repo.

Resultado que verás en tu issue: un comentario con el análisis completo del equipo
y etiquetas automáticas (p. ej. `bug`, `prioridad:alta`).

---

## 2. Los 6 agentes (qué aprendes con cada uno)

| # | Agente | Concepto de agentes que ilustra |
|---|--------|---------------------------------|
| 1 | **Triage** | Un agente puede **decidir el flujo** (clasificar y decir si continuar). |
| 2 | **Contexto** | **Tool use**: un agente que *lee tu repositorio* antes de opinar. |
| 3 | **Planner** | **Descomposición**: partir un problema grande en pasos accionables. |
| 4 | **Coder** | **Generación**: producir un artefacto concreto (un parche propuesto). |
| 5 | **Revisor** | **Auto-crítica / verificación adversarial**: un agente que busca fallos en otro. |
| 6 | **Reporter** | **Síntesis + acción**: consolida todo y *actúa* (comenta, etiqueta). |

Los *system prompts* de cada uno están en [`agentes/roles.py`](agentes/roles.py) —
**ese archivo es el corazón didáctico**. Ábrelo y juega con él.

---

## 3. Requisitos

- Una cuenta de **GitHub** y un repositorio (puede ser nuevo y vacío).
- Una **clave de API de OpenAI** (`OPENAI_API_KEY`). Se crea en
  <https://platform.openai.com/api-keys>. Uso de pago por consumo; esta POC con
  `gpt-4o-mini` cuesta **céntimos** por ejecución.
- Para probar en local: **Python 3.10+** instalado.

### 3.1 Levantar el proyecto en local (rápido)

> Si quieres una guía más completa para aportar cambios, ve a `CONTRIBUTING.md`.

**Linux/macOS (bash):**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edita .env y rellena OPENAI_API_KEY
python run_local.py
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# edita .env y rellena OPENAI_API_KEY
python run_local.py
```

---

## 4. Camino recomendado: **pruébalo primero en LOCAL** (sin tocar GitHub)

Así ves cada agente pensar en tu terminal, sin esperar a Actions ni gastar en push.

```powershell
# 1. Entra en la carpeta
cd C:\Users\vfern\Downloads\gihub\poc-agentes-github

# 2. Crea un entorno virtual e instala dependencias
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Configura tu clave (copia el ejemplo y edítalo)
copy .env.example .env
notepad .env      # pega tu OPENAI_API_KEY

# 4. Ejecuta el pipeline con un issue SIMULADO
python run_local.py
```

Verás en la terminal, agente por agente, cómo se transforma la entrada. Puedes
cambiar el issue simulado editando `run_local.py`, o pasar el tuyo:

```powershell
python run_local.py --titulo "Login lanza 500 con email vacío" --cuerpo "Al enviar el formulario sin email, la API responde 500 en vez de 400."
```

> En modo local **no** comenta en GitHub (no hay issue real): imprime lo que
> *publicaría*. Es a propósito, para que experimentes sin miedo.

---

## 5. Ejecutarlo de verdad **dentro de GitHub Actions** (lo que elegiste)

### 5.1. Sube la POC a un repo

```powershell
cd C:\Users\vfern\Downloads\gihub\poc-agentes-github
git init
git add .
git commit -m "POC: equipo de 6 agentes IA sobre GitHub Actions"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

### 5.2. Da de alta el secret de OpenAI

En tu repo de GitHub: **Settings → Secrets and variables → Actions → New repository secret**

- Name: `OPENAI_API_KEY`
- Secret: *(tu clave de OpenAI)*

(Opcional) En la pestaña **Variables**, crea `OPENAI_MODEL` con el valor `gpt-4o-mini`
(o `gpt-4o` para más calidad). Si no la creas, se usa `gpt-4o-mini` por defecto.

### 5.3. Dispara a los agentes

Abre un **issue nuevo** en el repo (o comenta `/agentes` en uno existente). En unos
segundos verás en la pestaña **Actions** el workflow corriendo y, al terminar, un
**comentario del equipo de agentes** y **etiquetas** en tu issue.

> El workflow tiene los permisos justos: `contents: read` e `issues: write`. Nada más.

---

## 6. Qué OBSERVAR para aprender (no te saltes esto)

1. **Abre la ejecución en Actions** y despliega el paso "Ejecutar pipeline de agentes":
   verás el log de **cada agente por separado** con su salida cruda.
2. Fíjate en cómo el **agente 5 (Revisor)** encuentra pegas al **agente 4 (Coder)**:
   ese "diálogo" es el núcleo de por qué varios agentes > uno solo.
3. Cambia un *system prompt* en `roles.py`, vuelve a abrir un issue y compara. Verás
   que **el comportamiento del agente = su prompt**. No hay más truco.
4. Rompe algo a propósito (p. ej. pide al Triage que devuelva JSON y quítale el
   ejemplo) y observa cómo se degrada. Aprender los **modos de fallo** es clave.

---

## 7. Estructura del proyecto

```
poc-agentes-github/
├── .github/workflows/agentes.yml   # el workflow: eventos → corre el pipeline
├── agentes/
│   ├── llm.py                       # cliente de IA (agnóstico, compatible OpenAI)
│   ├── base.py                      # qué ES un agente (clase Agente)
│   ├── github_tools.py             # herramientas reales: leer repo, comentar, etiquetar
│   ├── roles.py                     # ★ los 6 agentes (system prompts) — el corazón
│   └── orquestador.py              # encadena los 6 agentes (la orquestación)
├── run_actions.py                   # entrypoint usado por el workflow (issue real)
├── run_local.py                     # modo aprendizaje: issue simulado, sin GitHub
├── requirements.txt
├── .env.example
└── README.md
```

---

## 8. Cómo extenderla (siguientes pasos de aprendizaje)

- **Que abra un PR de verdad**: haz que el Coder genere un diff y añade un paso que
  cree una rama y un pull request (`contents: write`, `pull-requests: write`). Hay una
  guía en los comentarios de `orquestador.py`.
- **Tool-calling nativo**: en vez de leer el repo "a mano", deja que el modelo *decida*
  qué archivos leer con *function calling* de OpenAI. Es el salto de "pipeline fijo" a
  "agente autónomo".
- **Añade un 7º agente** (p. ej. "Tester" que proponga casos de prueba). Copia un rol
  en `roles.py` y engánchalo en `orquestador.py`.
- **Orquestación en paralelo**: haz que Planner y Contexto corran a la vez (aquí van en
  serie por claridad didáctica).

---

## 9. Costes y seguridad

- **Coste**: con `gpt-4o-mini` cada ejecución son unos pocos céntimos. Vigila tu
  consumo en el panel de OpenAI y pon límites de gasto.
- **Seguridad**: la clave vive **solo** como *secret* de GitHub, nunca en el código.
  El workflow no tiene permiso de escritura sobre tu código (solo issues).
- **Bucles**: el workflow solo se dispara con issues nuevos o comentarios que contienen
  `/agentes`; el comentario del propio bot no los contiene, así que **no se autoreactiva**.

---

## 10. Glosario exprés

- **Agente**: rol (system prompt) + llamada a modelo + herramientas para actuar.
- **Orquestación**: cómo se coordinan varios agentes (aquí, un pipeline en serie).
- **Tool use / function calling**: cuando un agente ejecuta acciones en el mundo real.
- **Handoff**: pasar el resultado de un agente como entrada del siguiente.

¡Disfruta rompiéndola y arreglándola! Esa es la mejor forma de aprender agentes.
