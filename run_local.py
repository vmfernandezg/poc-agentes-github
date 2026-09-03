"""
Modo APRENDIZAJE: ejecuta el equipo de agentes en tu máquina, con un issue SIMULADO,
sin tocar GitHub. Ideal para ver a cada agente pensar y para experimentar rápido.

Uso:
    python run_local.py
    python run_local.py --titulo "..." --cuerpo "..."
    python run_local.py --repo C:\\ruta\\a\\otro\\proyecto   # analiza OTRO repo

Requisitos: un archivo .env con OPENAI_API_KEY (copia .env.example a .env).
"""

from __future__ import annotations
import argparse

from dotenv import load_dotenv

from agentes import llm
from agentes.orquestador import Issue, ejecutar_pipeline


# Un issue de ejemplo, para que funcione con solo `python run_local.py`.
ISSUE_DEMO_TITULO = "El login devuelve 500 cuando el email está vacío"
ISSUE_DEMO_CUERPO = (
    "Al enviar el formulario de login sin rellenar el email, la API responde con un "
    "error 500 en lugar de un 400 con un mensaje claro. Debería validar la entrada y "
    "devolver un error controlado. Pasa tanto en web como en la app móvil."
)


def main() -> int:
    load_dotenv()  # carga OPENAI_API_KEY (y opcionalmente OPENAI_MODEL/BASE_URL) desde .env

    parser = argparse.ArgumentParser(description="Ejecuta el equipo de 6 agentes en local.")
    parser.add_argument("--titulo", default=ISSUE_DEMO_TITULO, help="Título del issue simulado.")
    parser.add_argument("--cuerpo", default=ISSUE_DEMO_CUERPO, help="Cuerpo del issue simulado.")
    parser.add_argument("--repo", default=".",
                        help="Carpeta del repo a analizar (por defecto, esta misma POC).")
    args = parser.parse_args()

    print("=" * 70)
    print(" POC · Equipo de 6 agentes de IA (modo local, sin publicar en GitHub)")
    print("=" * 70)
    print(f" Issue simulado: {args.titulo}")
    print(f" Repo analizado: {args.repo}")

    issue = Issue(titulo=args.titulo, cuerpo=args.cuerpo, autor="tu-usuario-local")
    cliente = llm.crear_cliente()

    resultado = ejecutar_pipeline(cliente, issue, raiz_repo=args.repo, log=print)

    # En local NO publicamos: mostramos lo que se publicaría.
    print("\n" + "=" * 70)
    print(" INFORME FINAL (esto es lo que el agente Reporter publicaría en el issue)")
    print("=" * 70 + "\n")
    print(resultado.informe_markdown)
    print("\n[Etiquetas que se aplicarían]:", ", ".join(resultado.etiquetas))
    print("\nSugerencia: abre agentes/roles.py, cambia un system prompt y vuelve a ejecutar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
