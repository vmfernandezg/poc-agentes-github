# 🤝 Guía de contribución

Gracias por contribuir a esta POC. La idea es mantener cambios **pequeños, claros y verificables**.

---

## 1) Preparar entorno local

### Linux/macOS (bash)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# completa OPENAI_API_KEY en .env
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# completa OPENAI_API_KEY en .env
```

---

## 2) Ejecutar la POC

### Pipeline local (sin publicar en GitHub)

```bash
python run_local.py
python run_local.py --titulo "..." --cuerpo "..."
```

Opcional: analizar otro repo local.

```bash
python run_local.py --repo /ruta/a/otro/repo
```

### Prueba del flujo en GitHub Actions (pipeline de 6 agentes)

1. Asegura el secret `OPENAI_API_KEY` en el repo.
2. Abre un issue (o comenta `/agentes` en uno existente).
3. Revisa la ejecución en **Actions** y el comentario final en el issue.

### Prueba del flujo nativo por etiquetas (v2)

1. Configura el secret `COPILOT_AGENT_PAT`.
2. Etiqueta un issue con `auto-fix`, `auto-feature`, `auto-tests`, `auto-docs` o `auto-review`.
3. Revisa el workflow **Despacho de agentes IA** y el PR creado por el agente.

---

## 3) Ejecutar tests

El repo incluye pruebas con `unittest`:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

> Nota: `tests/test_login.py` usa Flask (`app_ejemplo/login.py`). Si no lo tienes instalado, instala `flask` en tu entorno local antes de ejecutar ese test.

---

## 4) Flujo recomendado para contribuir

1. Crea una rama desde `main`.
2. Haz un cambio acotado (una mejora concreta por PR).
3. Verifica localmente lo que aplique (`run_local.py` y/o tests).
4. Abre PR explicando:
   - Qué cambiaste.
   - Por qué ese cambio mejora la POC.
   - Cómo lo validaste.

---

## 5) Dónde tocar según el tipo de mejora

- **Comportamiento de los agentes (pipeline v1):** `agentes/roles.py`
- **Orden/coordinación entre agentes:** `agentes/orquestador.py`
- **Herramientas de repo/GitHub:** `agentes/github_tools.py`
- **Agentes nativos (v2):** `.github/agents/*.md`
- **Documentación:** `README.md`, `ARQUITECTURA.md`, `DIAGRAMA.md`, `V2-NATIVA.md`

Para entender el diseño antes de tocar nada, lee [`ARQUITECTURA.md`](ARQUITECTURA.md).
