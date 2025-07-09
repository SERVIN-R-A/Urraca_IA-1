from flask import Flask, render_template, request, jsonify
from aria import Aria
from utils import extraer_texto_archivo

app = Flask(__name__)
usuarios = {}

def obtener_ia(nombre_usuario):
    if nombre_usuario not in usuarios:
        usuarios[nombre_usuario] = Aria(nombre_usuario)
    return usuarios[nombre_usuario]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mensaje", methods=["POST"])
def mensaje():
    datos = request.get_json()
    entrada = datos.get("mensaje", "")
    idioma = datos.get("idioma", "es")
    usuario = datos.get("usuario", "anonimo")
    ia = obtener_ia(usuario)
    ia.set_language(idioma)
    respuesta = ia.procesar_entrada(entrada)
    return jsonify({"respuesta": respuesta})

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    datos = request.get_json()
    usuario = datos.get("usuario", "anonimo")
    ia = obtener_ia(usuario)
    ia.reiniciar()
    return jsonify({"respuesta": f"{usuario} ha sido reiniciado."})

@app.route("/consultar", methods=["POST"])
def consultar():
    datos = request.get_json()
    mensaje = datos.get("mensaje", "")
    usuario = datos.get("usuario", "anonimo")
    with open("consultas.txt", "a", encoding="utf-8") as f:
        f.write(f"[{usuario}] {mensaje}\n")
    return jsonify({"respuesta": "Consulta enviada al creador. Gracias."})

if __name__ == "__main__":
    app.run(debug=True)
