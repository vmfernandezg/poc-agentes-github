# 🤖 v2 nativa — agentes de GitHub disparados por etiquetas

La v2 automatiza lo que antes hacías a mano en la pestaña *Agents*: ahora, **al poner una
etiqueta a un issue**, un workflow **dispara al agente nativo de Copilot** que corresponda,
y este **abre un Pull Request** con la propuesta. Tú revisas y haces merge.

## El equipo de agentes (`.github/agents/`)

| Agente | Qué hace | Etiqueta que lo dispara |
|--------|----------|-------------------------|
| `corrige-bugs` | Corrige un bug con el cambio mínimo + test | `auto-fix` |
| `implementa-feature` | Implementa una funcionalidad pequeña | `auto-feature` |
| `escribe-tests` | Añade tests (casos normales y límite) | `auto-tests` |
| `documenta` | Mejora documentación (sin tocar lógica) | `auto-docs` |
| `revisa-codigo` | Revisa y reporta problemas por severidad | `auto-review` |
| `verifica-ui` | Prueba la web en un navegador con Playwright → informe + capturas | `auto-qa` |

Cada agente es un archivo Markdown con `name`/`description` + instrucciones. Editarlos
cambia su comportamiento; añadir uno nuevo es copiar el patrón y mapear una etiqueta en el
workflow.

## Cómo funciona (flujo)

```
Pones la etiqueta "auto-fix" a un issue
   → .github/workflows/despacho-agentes.yml se activa
   → traduce la etiqueta al agente correspondiente
   → llama a POST /agents/repos/OWNER/REPO/tasks (API de tareas del agente)
   → Copilot trabaja en la nube siguiendo el archivo del agente y ABRE un PR
   → el workflow comenta en el issue que ha despachado al agente
   → tú revisas el PR y haces merge (o lo cierras)
```

## ⚠️ Configuración obligatoria: el PAT (el paso donde todos tropiezan)

La API de tareas del agente **solo acepta un token de usuario**. El `GITHUB_TOKEN` que
GitHub da a los workflows **NO sirve** (es *server-to-server*). Hay que darle un **PAT**.

### 1. Crea un Personal Access Token (fine-grained)
En GitHub: **Settings → Developer settings → Personal access tokens → Fine-grained tokens
→ Generate new token**.
- **Repository access**: solo este repo (`poc-agentes-github`).
- **Permissions** (Repository): **Read and write** en *Actions*, *Contents*, *Issues* y
  *Pull requests*.
- (Un PAT clásico con el scope `repo` también funciona, pero el fine-grained es más seguro.)

### 2. Guárdalo como secret del repo
**Settings → Secrets and variables → Actions → New repository secret**
- Name: `COPILOT_AGENT_PAT`
- Secret: *(el PAT que acabas de crear)*

### 3. Asegúrate de que las etiquetas existen
El repo ya trae creadas: `auto-fix`, `auto-feature`, `auto-tests`, `auto-docs`,
`auto-review`. (Si no, créalas en la pestaña *Issues → Labels* o con
`gh label create auto-fix`.)

## Cómo probarlo

1. Abre un issue describiendo un bug o tarea (p. ej. otro fallo en `app_ejemplo/`).
2. Ponle la etiqueta **`auto-fix`** (o la que toque).
3. Mira la pestaña **Actions**: verás correr *"Despacho de agentes IA"*.
4. A los pocos minutos aparece un **Pull Request** del agente y un comentario en el issue.
5. Revisa el PR y decide.

## Seguridad

- El agente trabaja en una **rama** y abre un **PR**; **nunca** escribe en `main`. El merge
  lo haces tú.
- Los agentes tienen prohibido tocar `.github/workflows/*` y secretos.
- El PAT vive solo como *secret*; nunca en el código.
- El título/cuerpo del issue se pasan al prompt de forma segura (como variables, escapadas
  con `jq`), no se ejecutan como comandos.

## Nota

La API `POST /agents/repos/.../tasks` está en **preview** y puede cambiar. Si algún día
falla, el workflow comenta el error en el issue y lo verás en los logs de Actions.
