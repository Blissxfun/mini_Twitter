from flask import Flask, request, redirect, render_template_string
import json
import os

app = Flask(__name__)
ARCHIVO = "tweets.json"

# Cargar tweets desde archivo si existe
if os.path.exists(ARCHIVO):
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        tweets = json.load(f)
else:
    tweets = []

# HTML con la opción de darle "like" a los tweets
HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Mini Twitter</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: auto; background: #f0f2f5; padding: 20px; }
    h1 { color: #1DA1F2; }
    form { margin-bottom: 20px; }
    input, button {
      padding: 10px;
      margin: 5px 0;
      width: 100%;
      border-radius: 5px;
      border: 1px solid #ccc;
    }
    button { background: #1DA1F2; color: white; border: none; }
    .tweet {
      background: white;
      padding: 10px;
      border-radius: 10px;
      margin-bottom: 10px;
      box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    .username { font-weight: bold; color: #555; }
    .content { margin-top: 5px; }
    .likes { color: #1DA1F2; }
  </style>
</head>
<body>
  <h1>Mini Twitter 🐦</h1>
  <form method="post">
    <input name="usuario" placeholder="Tu nombre de usuario" required>
    <input name="tweet" placeholder="Escribe tu tweet" required>
    <button type="submit">Twittear</button>
  </form>

  <h2>Tweets recientes:</h2>
  {% for t in tweets %}
    <div class="tweet">
      <div class="username">@{{ t['usuario'] }}</div>
      <div class="content">{{ t['contenido'] }}</div>
      <div class="likes">
        <span>{{ t['likes'] }} Likes</span>
        <form method="post" action="/like/{{ loop.index0 }}">
          <button type="submit">Like</button>
        </form>
      </div>
    </div>
  {% endfor %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        usuario = request.form["usuario"]
        tweet = request.form["tweet"]
        nuevo_tweet = {"usuario": usuario, "contenido": tweet, "likes": 0}
        tweets.append(nuevo_tweet)

        # Guardar tweets al archivo
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)

        return redirect("/")
    return render_template_string(HTML, tweets=reversed(tweets))

@app.route("/like/<int:tweet_id>", methods=["POST"])
def like(tweet_id):
    tweets[tweet_id]["likes"] += 1

    # Guardar tweets actualizados
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
