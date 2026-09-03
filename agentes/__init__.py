"""
Paquete `agentes`: una POC minimalista de sistema multi-agente.

Filosofía: NADA de magia. Un agente es un rol + una llamada al modelo + herramientas.
Lee los módulos en este orden para entenderlo:
    1. llm.py           -> cómo se habla con el modelo
    2. base.py          -> qué ES un agente
    3. github_tools.py  -> las herramientas con las que un agente actúa en el mundo real
    4. roles.py         -> los 6 agentes concretos (sus system prompts)
    5. orquestador.py   -> cómo se encadenan (la "orquestación")
"""
