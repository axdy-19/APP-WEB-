from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime
app = Flask(__name__)
app.secret_key = "12345"

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot",
    ssl_disabled=True
)

cursor = conexion.cursor()

def obtener_respuesta(mensaje_usuario):
    mensaje_usuario = mensaje_usuario.lower()
    cursor.execute("SELECT * FROM preguntas_respuestas WHERE pregunta = %s", (mensaje_usuario,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado[3]
    else:
        return "Lo siento, no entiendo lo que acabas de decir."

@app.route('/Jóvenes', methods=['GET', 'POST'])
def jovenes():
    cursor = conexion.cursor(dictionary=True)
    user_id = session.get("user_id", 1)

    if request.method == "POST":
       mensaje_usuario = request.form["mensaje"]
       respuesta_bot = obtener_respuesta(mensaje_usuario)
       return render_template("jovenes.html", mensaje_usuario=mensaje_usuario, respuesta_bot=respuesta_bot)

    return render_template("jovenes.html")

@app.route('/agregar_respuesta', methods=['GET', 'POST'])
def agregar_respuesta():
    if request.method == "POST":
       pregunta = request.form["pregunta"].lower()
       respuesta = request.form["respuesta"]

    try:
       cursor.execute("INSERT INTO preguntas_respuestas (pregunta, respuesta) VALUES (%s, %s)", (pregunta, respuesta,))
       cursor.commit()
       mensaje = "Respuesta agregada correctamente."
    except:
       mensaje = "Esa pregunta ya tiene una respuesta guardada."

    return render_template("agregar_respuesta.html", mensaje=mensaje)

@app.route("/editar_respuesta", methods=["GET", "POST"])
def editar_respuesta():
    if request.method == "POST":
       pregunta = request.form["pregunta"].lower()
       nueva_respuesta = request.form["nueva_respuesta"]

       cursor.execute("UPDATE preguntas_respuestas SET respuesta = %s WHERE pregunta = %s", (nueva_respuesta, pregunta,))
       cursor.commit()

       mensaje = "Respuesta actualizada correctamente."
       return render_template("editar_respuesta", mensaje=mensaje)

    return render_template("editar_respuesta.html")

@app.route("/eliminar_respuesta", methods=["GET", "POST"])
def eliminar_respuesta():
     if request.method == "POST":
         pregunta = request.form["pregunta"].lower()

         cursor.execute("DELETE FROM preguntas_respuestas = %s", (pregunta,))

         mensaje = "Respuesta eliminada correctamente."
         return render_template("eliminar_respuesta.html", mensaje=mensaje)

     return render_template("eliminar_respuesta.html")

@app.route("/nuevo_chat")
def nuevo_chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('Jóvenes'))

@app.route("/borrar_chat", methods=["POST"])
def borrar_chat():
    chat_id = request.form["chat_id"]

    cursor = conexion.cursor()
    cursor.execute("DELETE FROM mensajes WHERE id=%s", (chat_id,))
    conexion.commit()
    return redirect("/jovenes")

@app.route("/borrar_todo", methods=["POST"])
def borrar_todo():
    user_id = session.get("user_id", 1)

    cursor.execute("DELETE FROM mensajes WHERE usuario_id=%s", (user_id,))
    conexion.commit()
    return redirect("/jovenes")

if __name__ == "__main__":
    app.run(host="192.168.1.40", port="5001", debug=True)
