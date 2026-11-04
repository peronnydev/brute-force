from flask import Flask, request, jsonify

app = Flask(__name__)

USUARIOS = {
    "admin": "123456",
    "cofre": "583",
}


@app.route("/")
def inicio():
    return "Servico de login (vulneravel - apenas para estudo). Use POST /login"


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario", "")
    senha = request.form.get("senha", "")

    if USUARIOS.get(usuario) == senha:
        return jsonify({"ok": True, "mensagem": "Login realizado com sucesso"}), 200

    return jsonify({"ok": False, "mensagem": "Usuario ou senha invalidos"}), 401


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
