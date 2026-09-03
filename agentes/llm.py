"""
Cliente del modelo de IA — AGNÓSTICO al proveedor.

Elegiste OpenAI, pero este mismo código funciona con CUALQUIER proveedor compatible
con la API de OpenAI (Azure AI Foundry, Groq, etc.): solo cambia OPENAI_BASE_URL y
OPENAI_MODEL. Ese patrón es exactamente lo que reemplaza al difunto GitHub Models.

CONCEPTO CLAVE
--------------
Cada "agente" de esta POC es, por dentro, UNA llamada a la función `chat()` de aquí,
con un `system` prompt distinto. Si entiendes esta función, entiendes la mitad de
lo que es un agente. La otra mitad es la orquestación (ver orquestador.py).
"""

from __future__ import annotations
import os
from openai import OpenAI


def crear_cliente() -> OpenAI:
    """Crea el cliente del modelo leyendo la configuración del entorno.

    Variables de entorno:
      - OPENAI_API_KEY  (obligatoria): tu clave.
      - OPENAI_BASE_URL (opcional): úsala para apuntar a otro proveedor compatible.
                                    Si no está, se usa el endpoint de OpenAI.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Falta OPENAI_API_KEY. En local ponla en el archivo .env; "
            "en GitHub Actions, créala como 'secret' del repositorio."
        )

    base_url = os.environ.get("OPENAI_BASE_URL")  # None => OpenAI por defecto
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def modelo_por_defecto() -> str:
    """Modelo a usar. `gpt-4o-mini` es barato y suficiente para la POC."""
    return os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def chat(cliente: OpenAI, system: str, user: str,
         model: str | None = None, temperature: float = 0.2) -> str:
    """Una sola vuelta de conversación: system + user -> texto de respuesta.

    - `system`: define QUIÉN es el agente y CÓMO se comporta (su rol).
    - `user`:   la entrada concreta a procesar (el issue, el trabajo del agente previo...).
    - `temperature` baja (0.2) => respuestas más deterministas, mejor para tareas de análisis.
    """
    model = model or modelo_por_defecto()
    respuesta = cliente.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return (respuesta.choices[0].message.content or "").strip()
