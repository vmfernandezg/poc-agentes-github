"""
Qué ES un agente (la pieza conceptual central de la POC).

Un `Agente` = una IDENTIDAD (nombre + rol) + unas INSTRUCCIONES (system_prompt) +
la capacidad de recibir una entrada, "pensar" (llamar al modelo) y devolver una salida.

No hay nada más. Lo que convierte a varios agentes en un SISTEMA es la orquestación
(orquestador.py): encadenarlos y hacer que unos revisen a otros.
"""

from __future__ import annotations
from dataclasses import dataclass
from openai import OpenAI

from . import llm


@dataclass
class Agente:
    nombre: str          # p. ej. "Triage" (para los logs y el informe)
    rol: str             # descripción corta y humana de su función
    system_prompt: str   # LAS INSTRUCCIONES que definen su comportamiento. Su "cerebro".
    temperature: float = 0.2

    def ejecutar(self, cliente: OpenAI, entrada: str, model: str | None = None) -> str:
        """Ejecuta al agente sobre una entrada y devuelve su salida (texto).

        `entrada` es lo que este agente tiene que procesar: normalmente el issue
        más el trabajo acumulado de los agentes anteriores (el "handoff").
        """
        return llm.chat(
            cliente,
            system=self.system_prompt,
            user=entrada,
            model=model,
            temperature=self.temperature,
        )
