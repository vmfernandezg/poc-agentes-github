# 🗺️ Cómo funciona la POC (diagramas)

> GitHub dibuja estos diagramas automáticamente. Si ves código raro en vez de un
> dibujo, asegúrate de estar viendo el archivo en github.com (no en un editor local).

---

## 1. Vista general: del issue al comentario

Qué pasa desde que abres un issue hasta que el equipo de agentes te responde.
🔧 = el agente usa una **herramienta** (toca el mundo real: lee repo, comenta, etiqueta).

```mermaid
flowchart TD
    U(["👤 Abres un issue en tu repo"]) -->|evento issues opened| GA

    subgraph GA["⚙️ GitHub Actions — una máquina en la nube"]
        direction TB
        CO["1· Descarga tu repo e instala Python"] --> RUN["2· run_actions.py lee el issue real 🔧"]
        RUN --> P
        subgraph P["🤖 Pipeline de 6 agentes — orquestador.py"]
            direction TB
            A1["Agente 1 · TRIAGE<br/>clasifica: tipo y prioridad"] --> A2
            A2["Agente 2 · CONTEXTO<br/>lee archivos de tu repo 🔧"] --> A3
            A3["Agente 3 · PLANNER<br/>descompone en pasos"] --> A4
            A4["Agente 4 · CODER<br/>propone un arreglo"] --> A5
            A5["Agente 5 · REVISOR<br/>busca fallos en el arreglo"] --> A6
            A6["Agente 6 · REPORTER<br/>redacta el informe final"]
        end
    end

    P --> OUT1["💬 Comentario en tu issue 🔧"]
    P --> OUT2["🏷️ Etiquetas en tu issue 🔧"]
```

---

## 2. Qué ES un agente (la idea que desmitifica todo)

Un agente no es un programa complejo. Son tres piezas:

```mermaid
flowchart LR
    ROL["📋 ROL<br/>(instrucciones / system prompt)<br/>'Eres el que clasifica issues...'"] --> LLM
    IN["📥 ENTRADA<br/>(el issue + trabajo previo)"] --> LLM
    LLM["🧠 Llamada a la IA<br/>(OpenAI)"] --> OUT["📤 SALIDA<br/>(el 'trabajo' del agente)"]
    OUT -.->|"si tiene herramientas"| ACT["🔧 ACTÚA<br/>lee repo · comenta · etiqueta"]
```

> **Consecuencia clave:** cambiar el comportamiento de un agente = cambiar su texto de
> instrucciones (en `agentes/roles.py`). No hay más magia.

---

## 3. El "expediente que crece" (por qué es multi-agente y no un solo chat)

Cada agente recibe el issue **más el trabajo de todos los anteriores**. El expediente
se va llenando. Esto se llama *handoff* (traspaso).

```mermaid
flowchart LR
    I["📄 Issue"] --> T["+ Triage"]
    T --> C["+ Contexto"]
    C --> Pl["+ Plan"]
    Pl --> Co["+ Código propuesto"]
    Co --> R["+ Revisión"]
    R --> Rep["📝 REPORTER<br/>ve TODO el expediente<br/>y escribe el informe"]
```

El **Revisor (agente 5)** tiene delante lo que escribió el **Coder (agente 4)** y su
trabajo es **criticarlo**. Un agente vigilando a otro: *ese* es el motivo de usar varios
agentes en lugar de uno solo — se pillan los errores entre ellos.

---

## 4. Ejemplo real recorriendo la cadena

Issue de ejemplo: *"El login devuelve 500 cuando el email está vacío"*

```mermaid
flowchart TD
    START["📄 'login devuelve 500 con email vacío'"] --> T
    T["🧭 TRIAGE"] -->|"bug · prioridad alta"| C
    C["🔎 CONTEXTO"] -->|"toca auth/login.py, falta validar email"| P
    P["🗺️ PLANNER"] -->|"1 validar 2 devolver 400 3 test"| CO
    CO["🛠️ CODER"] -->|"código que valida el email"| RE
    RE["🕵️ REVISOR"] -->|"ojo: falta el caso 'solo espacios'"| REP
    REP["📝 REPORTER"] --> FIN["💬 Informe + 🏷️ etiquetas en tu issue"]
```

---

## 5. Qué archivo es cada cosa

| Archivo | Qué representa | Concepto |
|---------|----------------|----------|
| `agentes/roles.py` | Los 6 agentes (sus instrucciones) | **Qué es un agente** ← empieza aquí |
| `agentes/orquestador.py` | La cadena de montaje | **Orquestación / handoff** |
| `agentes/llm.py` | Cómo se habla con la IA | La llamada al modelo |
| `agentes/github_tools.py` | Leer repo, comentar, etiquetar | **Herramientas (tool use)** |
| `run_local.py` | Botón "probar en mi PC" | Ejecución local |
| `run_actions.py` | Botón que pulsa la nube | Ejecución en Actions |
| `.github/workflows/agentes.yml` | El vigilante que lo dispara | El disparador (evento → agentes) |
