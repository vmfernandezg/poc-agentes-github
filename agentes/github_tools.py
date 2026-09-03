"""
Las HERRAMIENTAS (tools) con las que los agentes tocan el mundo real.

Un agente que solo habla es un chat. Un agente con herramientas ACTÚA: lee tu
repositorio, comenta en un issue, pone etiquetas. Aquí viven esas herramientas.

- Las funciones `leer_archivos_repo` / `leer_archivo` las usa el agente CONTEXTO.
- Las funciones `comentar_issue` / `poner_etiquetas` / `leer_issue` las usa el
  entrypoint de Actions (run_actions.py) para PUBLICAR el resultado del equipo.

En modo local no hace falta GitHub: leemos el repo del disco y "simulamos" la
publicación imprimiéndola por pantalla.
"""

from __future__ import annotations
import os
from pathlib import Path
import requests

API = "https://api.github.com"

# Carpetas/archivos que no aportan contexto útil y solo gastarían tokens.
_IGNORAR_DIRS = {".git", ".github", "node_modules", ".venv", "venv", "__pycache__",
                 "dist", "build", ".idea", ".vscode", ".mypy_cache", ".pytest_cache"}
_EXT_TEXTO = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb",
              ".php", ".c", ".h", ".cpp", ".cs", ".md", ".txt", ".yml", ".yaml",
              ".json", ".toml", ".cfg", ".ini", ".sh", ".ps1", ".html", ".css", ".sql"}


# --------------------------------------------------------------------------- #
#  Herramientas de LECTURA DEL REPO (las usa el agente Contexto)
# --------------------------------------------------------------------------- #

def leer_archivos_repo(raiz: str = ".", limite: int = 60) -> list[str]:
    """Devuelve una lista de rutas de archivos de texto del repo (hasta `limite`).

    En GitHub Actions el repo se 'checkoutea' en el directorio de trabajo, así que
    basta con recorrer el sistema de archivos. Es la versión sencilla y honesta de
    'darle ojos' a un agente sobre tu código.
    """
    raiz_path = Path(raiz).resolve()
    encontrados: list[str] = []
    for dirpath, dirnames, filenames in os.walk(raiz_path):
        # Poda de carpetas ruidosas (modifica dirnames in-place para no descender).
        dirnames[:] = [d for d in dirnames if d not in _IGNORAR_DIRS]
        for f in filenames:
            if Path(f).suffix.lower() in _EXT_TEXTO:
                rel = str(Path(dirpath, f).relative_to(raiz_path))
                encontrados.append(rel)
                if len(encontrados) >= limite:
                    return sorted(encontrados)
    return sorted(encontrados)


def leer_archivo(ruta: str, raiz: str = ".", max_chars: int = 4000) -> str:
    """Lee un archivo del repo (truncado) para dárselo como contexto a un agente."""
    p = (Path(raiz) / ruta).resolve()
    try:
        texto = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001 - en una POC queremos ver el error, no ocultarlo
        return f"[no se pudo leer {ruta}: {e}]"
    if len(texto) > max_chars:
        texto = texto[:max_chars] + f"\n... [truncado a {max_chars} caracteres]"
    return texto


# --------------------------------------------------------------------------- #
#  Herramientas de la API de GitHub (las usa run_actions.py)
# --------------------------------------------------------------------------- #

def _headers() -> dict:
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError(
            "Falta GH_TOKEN. En GitHub Actions se inyecta desde secrets.GITHUB_TOKEN "
            "(ver el workflow). En local no lo necesitas: usa run_local.py."
        )
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def leer_issue(repo: str, numero: int) -> dict:
    """Devuelve {'titulo', 'cuerpo', 'autor'} del issue indicado. `repo` = 'owner/name'."""
    r = requests.get(f"{API}/repos/{repo}/issues/{numero}", headers=_headers(), timeout=30)
    r.raise_for_status()
    data = r.json()
    return {
        "titulo": data.get("title") or "",
        "cuerpo": data.get("body") or "",
        "autor": (data.get("user") or {}).get("login") or "desconocido",
    }


def comentar_issue(repo: str, numero: int, cuerpo: str) -> None:
    """Publica un comentario en el issue (así es como el equipo 'entrega' su resultado)."""
    r = requests.post(
        f"{API}/repos/{repo}/issues/{numero}/comments",
        headers=_headers(), json={"body": cuerpo}, timeout=30,
    )
    r.raise_for_status()


def poner_etiquetas(repo: str, numero: int, etiquetas: list[str]) -> None:
    """Añade etiquetas al issue. GitHub las crea si no existen."""
    etiquetas = [e for e in (etiquetas or []) if e][:8]  # límite defensivo
    if not etiquetas:
        return
    r = requests.post(
        f"{API}/repos/{repo}/issues/{numero}/labels",
        headers=_headers(), json={"labels": etiquetas}, timeout=30,
    )
    r.raise_for_status()
