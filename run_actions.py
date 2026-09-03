"""
Entrypoint que ejecuta GitHub Actions (ver .github/workflows/agentes.yml).

Diferencia con run_local.py: aquí el issue es REAL (lo leemos de la API de GitHub)
y el resultado se PUBLICA de verdad (comentario + etiquetas en tu issue).

Variables de entorno que inyecta el workflow:
  - OPENAI_API_KEY : secret del repo.
  - OPENAI_MODEL   : variable del repo (opcional; por defecto gpt-4o-mini).
  - GH_TOKEN       : el GITHUB_TOKEN del workflow (para comentar/etiquetar).
  - REPO           : 'owner/nombre' del repositorio.
  - ISSUE_NUMBER   : número del issue que disparó el workflow.
"""

from __future__ import annotations
import os
import sys

from agentes import llm
from agentes import github_tools as tools
from agentes.orquestador import Issue, ejecutar_pipeline


def main() -> int:
    repo = os.environ.get("REPO", "")
    numero_str = os.environ.get("ISSUE_NUMBER", "")
    if not repo or not numero_str:
        print("Faltan REPO o ISSUE_NUMBER en el entorno.", file=sys.stderr)
        return 1
    numero = int(numero_str)

    print(f"== Equipo de agentes sobre {repo}#{numero} ==")

    # 1) Leemos el issue real de GitHub (herramienta).
    datos = tools.leer_issue(repo, numero)
    issue = Issue(titulo=datos["titulo"], cuerpo=datos["cuerpo"], autor=datos["autor"])

    # 2) Ejecutamos el pipeline de 6 agentes. El log va al output del workflow:
    #    ahí es donde puedes ver a cada agente pensar.
    cliente = llm.crear_cliente()
    resultado = ejecutar_pipeline(cliente, issue, raiz_repo=".", log=print)

    # 3) PUBLICAMOS el resultado en el issue (la parte 'agente que actúa').
    pie = ("\n\n---\n*Generado por una POC de 6 agentes de IA en GitHub Actions. "
           "El código de cada agente está en `agentes/roles.py`.*")
    tools.comentar_issue(repo, numero, resultado.informe_markdown + pie)
    tools.poner_etiquetas(repo, numero, resultado.etiquetas)

    print(f"\n✅ Publicado comentario y etiquetas {resultado.etiquetas} en {repo}#{numero}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
