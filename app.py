from flask import Flask, request, redirect, render_template, session, url_for, flash
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Necesaria para usar sesiones
ARCHIVO_TWEETS = "tweets.json"
ARCHIVO_USUARIOS = "users.json"

# Cargar usuarios registrados desde archivo
if os.path.exists(ARCHIVO_USUARIOS):
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
        usuarios = json.load(f)
else:
    usuarios = []

# Cargar tweets desde archivo si existe
if os.path.exists(ARCHIVO_TWEETS):
    with open(ARCHIVO_TWEETS, "r", encoding="utf-8") as f:
        tweets = json.load(f)
else:
    tweets = []

@app.route("/", methods=["GET", "POST"])
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        usuario = session['usuario']
        tweet = request.form["tweet"]
        nuevo_tweet = {"usuario": usuario, "contenido": tweet, "likes": 0, "comentarios": []}
        tweets.append(nuevo_tweet)

        # Guardar tweets al archivo
        with open(ARCHIVO_TWEETS, "w", encoding="utf-8") as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)

        return redirect("/")
    return render_template("index.html", tweets=reversed(tweets))

@app.route("/like/<int:tweet_id>", methods=["POST"])
def like(tweet_id):
    if 0 <= tweet_id < len(tweets):
        tweets[tweet_id]["likes"] += 1

        # Guardar tweets actualizados
        with open(ARCHIVO_TWEETS, "w", encoding="utf-8") as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verificar si el usuario existe y la contraseña es correcta
        user = next((u for u in usuarios if u["username"] == username), None)

        if user and check_password_hash(user["password"], password):
            session['usuario'] = username  # Iniciar sesión
            return redirect(url_for('home'))
        else:
            flash("Usuario o contraseña incorrectos", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('usuario', None)  # Cerrar sesión
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Verificar si el usuario ya existe
        if any(u["username"] == username for u in usuarios):
            flash("El usuario ya está registrado", "error")
            return redirect(url_for('register'))

        # Verificar que las contraseñas coincidan
        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('register'))

        # Guardar el nuevo usuario con la contraseña encriptada
        hashed_password = generate_password_hash(password)
        usuarios.append({"username": username, "password": hashed_password})
        with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)

        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for('login'))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)