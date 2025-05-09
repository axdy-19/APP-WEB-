from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "12345"

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot_usuarios",
    ssl_disabled=True
)

cursor = conexion.cursor()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
       session["seccion"] = request.form.get("seccion")
       if session["seccion"] == "Jóvenes":
           return redirect(url_for("registro"))
       elif session["seccion"] == "Mayores":
           return redirect(url_for("registro_mayores"))
    return render_template("inicio.html")
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")

        cursor.execute("INSERT INTO jovenes (usuario, correo, contraseña) VALUES (%s, %s, %s)", (usuario, correo, contraseña))
        conexion.commit()
        return redirect(url_for('login'))
    return render_template("registro.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = ""

    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")

        cursor.execute("SELECT * FROM jovenes WHERE usuario=%s AND contraseña=%s", (usuario, contraseña))
        usuario = cursor.fetchone()

        if usuario:
            session["usuario_joven"] = usuario[2]
            return redirect("http://192.168.1.40:5001/Jóvenes")

        else:
            mensaje = "Usuario o contraseña incorrectos."

    return render_template("index.html", mensaje=mensaje)

@app.route('/registro_mayores', methods=['GET', 'POST'])
def registro_mayores():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")

        cursor.execute("INSERT INTO mayores (nombre, correo) VALUES (%s, %s)", (nombre, correo))
        conexion.commit()

        session["nombre_mayor"] = nombre

        return redirect(url_for("login_mayores"))

    return render_template("registro_mayores.html")

@app.route('/login_mayores', methods=['GET', 'POST'])
def login_mayores():
    mensaje ="Bienvenid@1234"


    if request.method == "POST":
        nombre = request.form.get("nombre")

        cursor.execute("SELECT * FROM mayores WHERE nombre=%s", (nombre,))
        usuario = cursor.fetchone()

        if usuario:
            session["nombre_mayor"] = nombre
            return redirect(url_for("mayores"))
        else:
            mensaje= "Nombre incorrecto. Inténtelo de nuevo."

    return render_template("login_mayores.html", mensaje=mensaje)

app.route('/Jóvenes', methods=['GET', 'POST'])
def jovenes():
    if "usuario_joven" in session:
       return render_template("jovenes.html")

    return render_template("jovenes.html")

@app.route('/Mayores')
def mayores():
    if "nombre_mayor" in session:
        return render_template("mayores.html")
  
    return redirect('login_mayores')

if __name__ == "__main__":
    app.run(host="192.168.1.40", port="5000", debug=True)
