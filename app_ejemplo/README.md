# app_ejemplo — aplicación de juguete (con un bug a propósito)

Esta carpeta **no es** parte del sistema de agentes. Es la "aplicación" ficticia
sobre la que los agentes practican, para que el issue de ejemplo tenga código real.

- `login.py` — un endpoint de login con un **bug intencionado**: si el email llega
  vacío o ausente, responde **500** en vez de un **400** controlado.

## El bug, en 10 segundos

```python
def normalizar_email(email):
    return email.strip().lower()   # si email es None o "", esto revienta -> 500
```

Falta validar el email **antes** de usarlo. Ese es exactamente el problema que
describe el issue de ejemplo *"El login devuelve 500 cuando el email está vacío"*.

## Qué harán los agentes con esto

1. **Contexto** encontrará `app_ejemplo/login.py` y lo señalará como archivo relevante.
2. **Planner** propondrá validar el email y devolver 400.
3. **Coder** escribirá el arreglo concreto sobre esta función.
4. **Revisor** buscará huecos (p. ej. "¿y si el email es solo espacios?").
5. **Reporter** te lo resumirá todo en el informe del issue.

> Recuerda: los agentes **solo proponen** el arreglo en el informe; no editan este
> archivo. Aplicarlo (o no) lo decides tú.
