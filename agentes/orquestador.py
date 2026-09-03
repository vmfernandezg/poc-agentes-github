"""
La ORQUESTACIÓN: cómo se coordinan los 6 agentes.

Aquí es donde "varios chatbots" se convierten en "un sistema de agentes". El patrón
de esta POC es el más didáctico: un PIPELINE EN SERIE. Cada agente recibe el issue
más el trabajo acumulado de los anteriores (esto se llama 'handoff') y añade su parte.

Variantes que podrías probar tú (ver README §8):
  - Paralelo: Contexto y Planner podrían correr a la vez.
  - Autónomo: dejar que un agente DECIDA a qué agente llamar (en vez de orden fijo).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from openai import OpenAI

from . import github_tools as tools
from . import roles


@dataclass
class Issue:
    """Representa el issue a procesar (viene de GitHub o simulado en local)."""
    titulo: str
    cuerpo: str
    autor: str = "desconocido"


@dataclass
class ResultadoPipeline:
    """Todo lo que produjo el equipo, para publicar y/o inspeccionar."""
    informe_markdown: str = ""
    etiquetas: list[str] = field(default_factory=list)
    salidas_por_agente: dict[str, str] = field(default_factory=dict)


def _bloque(titulo: str, contenido: str) -> str:
    """Formatea una sección del 'expediente' compartido entre agentes."""
    return f"===== {titulo} =====\n{contenido}\n"


def _recopilar_contexto_repo(raiz: str, log) -> str:
    """HERRAMIENTA en acción: leemos el repo del disco para dárselo al agente Contexto.

    Le pasamos la lista de archivos y el contenido de unos pocos 'sospechosos' típicos
    (README y archivos de código raíz). Es una heurística sencilla a propósito: el
    objetivo didáctico es que veas 'un agente con ojos sobre el repo', no un RAG perfecto.
    """
    archivos = tools.leer_archivos_repo(raiz=raiz, limite=60)
    log(f"   herramienta leer_archivos_repo -> {len(archivos)} archivos encontrados")

    # Elegimos hasta 3 archivos para mostrar su contenido (los más 'informativos').
    preferidos = [a for a in archivos if a.lower() in
                  ("readme.md", "readme.txt", "package.json", "pyproject.toml")]
    otros = [a for a in archivos if a not in preferidos]
    muestra = (preferidos + otros)[:3]

    partes = ["ARCHIVOS DEL REPO (muestra):", *[f"  - {a}" for a in archivos[:40]], ""]
    for ruta in muestra:
        partes.append(f"--- CONTENIDO DE {ruta} ---")
        partes.append(tools.leer_archivo(ruta, raiz=raiz, max_chars=2500))
        partes.append("")
    return "\n".join(partes)


def _extraer_etiquetas(salida_reporter: str, salida_triage: str) -> list[str]:
    """Saca las etiquetas de la línea 'ETIQUETAS_FINALES:' (o cae al triage)."""
    for fuente in (salida_reporter, salida_triage):
        for linea in fuente.splitlines():
            clave = "ETIQUETAS_FINALES:" if "ETIQUETAS_FINALES:" in linea else \
                    ("ETIQUETAS:" if linea.strip().upper().startswith("ETIQUETAS:") else None)
            if clave:
                bruto = linea.split(":", 1)[1]
                etiquetas = [e.strip().lower() for e in bruto.split(",") if e.strip()]
                if etiquetas:
                    return etiquetas[:6]
    return ["agentes:analizado"]


def ejecutar_pipeline(cliente: OpenAI, issue: Issue, raiz_repo: str = ".",
                      log=print) -> ResultadoPipeline:
    """Ejecuta los 6 agentes en serie y devuelve el resultado.

    `log` recibe cada mensaje de progreso: en local imprime en la terminal, en Actions
    va al log del workflow. Ese log es LO QUE DEBES MIRAR para aprender: verás la
    salida cruda de cada agente y cómo se van pasando el trabajo.
    """
    resultado = ResultadoPipeline()

    # El "expediente" compartido: empieza con el issue y va creciendo con cada agente.
    expediente = _bloque("ISSUE",
                         f"Título: {issue.titulo}\nAutor: {issue.autor}\n\n{issue.cuerpo}")

    # --- Agente 1: TRIAGE ------------------------------------------------- #
    log("\n[1/6] 🧭 TRIAGE — clasificando el issue...")
    salida_triage = roles.TRIAGE.ejecutar(cliente, expediente)
    resultado.salidas_por_agente["Triage"] = salida_triage
    log(salida_triage)
    expediente += _bloque("TRIAGE", salida_triage)

    # El triage puede DECIDIR cortar el pipeline (spam/vacío). Un agente controlando flujo.
    if "CONTINUAR: no" in salida_triage.lower().replace(" ", " "):
        log("\n⛔ El agente de triage decidió NO continuar (issue vacío/spam).")
        resultado.informe_markdown = (
            "## 🤖 Análisis del equipo de agentes\n\n"
            "El agente de *triage* consideró que este issue no requiere procesamiento "
            "(vacío o spam). No se ejecutó el resto del pipeline.\n"
        )
        resultado.etiquetas = _extraer_etiquetas("", salida_triage)
        return resultado

    # --- Agente 2: CONTEXTO (usa herramienta de lectura de repo) ---------- #
    log("\n[2/6] 🔎 CONTEXTO — leyendo el repositorio...")
    contexto_repo = _recopilar_contexto_repo(raiz_repo, log)
    entrada_contexto = expediente + _bloque("MUESTRA DEL REPOSITORIO", contexto_repo)
    salida_contexto = roles.CONTEXTO.ejecutar(cliente, entrada_contexto)
    resultado.salidas_por_agente["Contexto"] = salida_contexto
    log(salida_contexto)
    expediente += _bloque("CONTEXTO", salida_contexto)

    # --- Agente 3: PLANNER ------------------------------------------------ #
    log("\n[3/6] 🗺️  PLANNER — descomponiendo la solución...")
    salida_plan = roles.PLANNER.ejecutar(cliente, expediente)
    resultado.salidas_por_agente["Planner"] = salida_plan
    log(salida_plan)
    expediente += _bloque("PLAN", salida_plan)

    # --- Agente 4: CODER -------------------------------------------------- #
    log("\n[4/6] 🛠️  CODER — proponiendo un cambio de código...")
    salida_coder = roles.CODER.ejecutar(cliente, expediente)
    resultado.salidas_por_agente["Coder"] = salida_coder
    log(salida_coder)
    expediente += _bloque("PROPUESTA DE CÓDIGO (Coder)", salida_coder)

    # --- Agente 5: REVISOR (critica al Coder) ----------------------------- #
    log("\n[5/6] 🕵️  REVISOR — buscando fallos en la propuesta...")
    salida_revisor = roles.REVISOR.ejecutar(cliente, expediente)
    resultado.salidas_por_agente["Revisor"] = salida_revisor
    log(salida_revisor)
    expediente += _bloque("REVISIÓN (Revisor)", salida_revisor)

    # --- Agente 6: REPORTER (sintetiza y decide etiquetas) ---------------- #
    log("\n[6/6] 📝 REPORTER — redactando el informe final...")
    salida_reporter = roles.REPORTER.ejecutar(cliente, expediente)
    resultado.salidas_por_agente["Reporter"] = salida_reporter
    log("   (informe final generado)")

    resultado.informe_markdown = salida_reporter
    resultado.etiquetas = _extraer_etiquetas(salida_reporter, salida_triage)
    return resultado
