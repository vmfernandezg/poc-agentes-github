# 🛠️ Roadmap v2 — de agentes que RECOMIENDAN a agentes que CORRIGEN

> Objetivo: que el equipo de agentes no solo escriba un informe, sino que **aplique el
> arreglo y abra un Pull Request** con el cambio real sobre el código.
>
> Estado: **planificado** (se ejecuta en la siguiente sesión). Este documento es el
> punto de continuación.

---

## 1. El cambio en una frase

Hoy el Coder *describe* el arreglo en texto y el Reporter lo comenta.
En la v2, el Coder *produce un cambio aplicable* y un nuevo paso **Integrador** crea una
rama, escribe los archivos, hace commit y **abre un Pull Request**. Tú revisas y haces merge.

**Regla de oro: siempre PR, nunca escribir en `main` directamente.** El humano es el
último filtro. (Es como trabaja el Copilot Coding Agent de GitHub.)

---

## 2. Arquitectura v2 (pipeline nuevo)

```
Issue → Actions
  1. TRIAGE        (igual que hoy)
  2. CONTEXTO      (igual: lee el repo)
  3. PLANNER       (igual: descompone)
  4. CODER         ★ ahora devuelve EDICIONES APLICABLES (archivo + contenido nuevo)
  5. REVISOR       ★ aprueba o RECHAZA; si rechaza → vuelve al Coder (bucle, máx 2-3)
  6. INTEGRADOR    ★ NUEVO: crea rama, aplica ediciones, commit, abre PULL REQUEST
  7. REPORTER      comenta en el issue con el enlace al PR
```

Dos patrones nuevos de aprendizaje respecto a v1:
- **Bucle de refinamiento** (4 ↔ 5): el Coder reintenta si el Revisor lo rechaza. Es el
  patrón "loop hasta aprobar", con un tope de intentos para no gastar de más.
- **Agente que modifica el mundo** (6): pasar de "leer/comentar" a "escribir código y abrir PR".

---

## 3. Cambios técnicos concretos (checklist para la próxima sesión)

### 3.1. Permisos del workflow (`.github/workflows/agentes.yml`)
```yaml
permissions:
  contents: write         # crear rama y commitear el arreglo
  pull-requests: write    # abrir el PR
  issues: write           # comentar en el issue
```

### 3.2. El Coder con SALIDA ESTRUCTURADA
El Coder debe devolver algo que una máquina pueda aplicar sin ambigüedad. Formato
propuesto (JSON), usando *structured outputs* de OpenAI para garantizar que es válido:
```json
{
  "resumen": "Validar email vacío y devolver 400",
  "ediciones": [
    { "ruta": "app_ejemplo/login.py", "contenido_nuevo": "<archivo completo ya corregido>" }
  ]
}
```
Decisión: **por ahora, archivo completo** (`contenido_nuevo`) en vez de *diff*. Aplicar
diffs generados por un LLM falla mucho (el contexto no cuadra); reemplazar el archivo
entero es aburrido pero **fiable**. El modo *diff/patch* queda como nivel 2.

### 3.3. Módulo nuevo `agentes/integrador.py`
Funciones:
- `crear_rama(nombre)` → `agentes/fix-issue-<N>`
- `aplicar_ediciones(ediciones)` → escribe cada `contenido_nuevo` en su `ruta`
- `commit_y_push(mensaje)`
- `abrir_pr(titulo, cuerpo, rama)` → vía API de GitHub o `gh`
En Actions se usa el `GITHUB_TOKEN` del workflow para push y PR.

### 3.4. Bucle Coder ↔ Revisor (en `orquestador.py`)
```
intentos = 0
mientras intentos < 3:
    edicion = Coder(...)
    veredicto = Revisor(edicion)
    si veredicto == "aprobado": romper
    intentos += 1
    # pasar los PROBLEMAS del revisor al Coder como feedback para el reintento
```

### 3.5. El Reporter enlaza el PR
El comentario final del issue incluye: "He abierto el PR #NN con el arreglo propuesto".

---

## 4. Guardarraíles de SEGURIDAD (no opcionales)

Un agente que escribe código puede hacer estropicios. Antes de aplicar nada:

- ✅ **Siempre PR, nunca `main`.** El merge lo hace un humano.
- ✅ **Lista blanca de rutas editables.** Prohibido tocar `.github/workflows/*` (que un
  agente edite su propio disparador o permisos es peligroso), `.env`, secretos, etc.
- ✅ **Límite de nº de archivos y tamaño** por edición (p. ej. máx 5 archivos, máx 50 KB).
- ✅ **Tope de reintentos** Coder↔Revisor (máx 3) y vigilar el coste.
- ✅ **El PR se abre en una rama**, con etiqueta `generado-por-agentes`, para que se vea
  claramente que viene de la IA.
- ✅ **Nada de auto-merge.** Ni ahora ni luego (en esta POC).

---

## 5. Cómo se probará

1. Abrir el issue "El login devuelve 500 con email vacío".
2. El pipeline corre en Actions.
3. Resultado esperado: **un PR nuevo** que corrige `app_ejemplo/login.py` (valida el email
   y devuelve 400) + un comentario en el issue enlazando ese PR.
4. Tú abres el PR, revisas el diff, y haces merge si te convence.

---

## 6. Nivel 2 (más adelante): agente AUTÓNOMO con tool-calling

El salto final: en vez de un pipeline fijo, dar al modelo *herramientas* (`leer_archivo`,
`escribir_archivo`, `buscar`) mediante *function calling* y dejar que **decida solo** qué
leer y editar, en bucle, hasta resolver el issue. Eso es un "agente" en el sentido más
moderno. Lo abordamos cuando la v2 esté sólida.

---

## 7. Orden de trabajo para la próxima sesión

1. [ ] Ampliar permisos del workflow.
2. [ ] Reescribir el prompt del Coder para salida JSON estructurada.
3. [ ] Crear `agentes/integrador.py` (rama + aplicar + commit + PR).
4. [ ] Añadir el bucle Coder↔Revisor en `orquestador.py`.
5. [ ] Añadir los guardarraíles (lista blanca de rutas, límites).
6. [ ] Actualizar `run_actions.py` para llamar al Integrador tras la aprobación.
7. [ ] Probar con el issue del login y revisar el PR resultante.
```
