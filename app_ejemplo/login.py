"""
Mini-aplicación de EJEMPLO con un bug puesto A PROPÓSITO.

¿Por qué existe este archivo?
-----------------------------
Los agentes de la POC no inventan código: el agente CONTEXTO lee los archivos que
haya en el repositorio. Sin una app real, el ejemplo del issue "login devuelve 500
con email vacío" no tendría nada concreto sobre lo que actuar.

Este archivo es esa app: un endpoint de login que, cuando el email llega vacío o
ausente, REVIENTA con un error 500 en vez de devolver un 400 controlado. Es justo
el bug que describe el issue de ejemplo. Los agentes lo encontrarán aquí.

Para ejecutarlo de verdad (opcional):  pip install flask  &&  python app_ejemplo/login.py
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# "Base de datos" de juguete.
USUARIOS = {
    "ana@example.com": "1234",
    "luis@example.com": "abcd",
}


def normalizar_email(email):
    """Pasa el email a minúsculas y quita espacios.

    BUG A PROPÓSITO: da por hecho que 'email' siempre trae un texto. Si llega None
    (el cliente no mandó el campo) o vacío, esta línea lanza una excepción y Flask
    responde 500. Debería validarse ANTES de llamar aquí.
    """
    return email.strip().lower()


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True) or {}
    email = datos.get("email")        # <-- puede venir None o ""
    password = datos.get("password")

    # BUG: no se valida 'email' antes de usarlo. Con email vacío/ausente,
    # normalizar_email() lanza AttributeError y el usuario recibe un 500 feo
    # en lugar de un mensaje claro "el email es obligatorio" (400).
    email = normalizar_email(email)

    if USUARIOS.get(email) == password:
        return jsonify({"ok": True, "mensaje": "login correcto"}), 200

    return jsonify({"ok": False, "mensaje": "credenciales inválidas"}), 401


if __name__ == "__main__":
    app.run(debug=True)
