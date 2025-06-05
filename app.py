import os
import json
from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    base_url="https://api.cometapi.com/v1",
    api_key=os.getenv("COMET_API_KEY"),
)

JSON_FILE = "conversaciones.json"

def cargar_conversaciones():
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_conversacion(nueva_entrada):
    conversaciones = cargar_conversaciones()
    conversaciones.append(nueva_entrada)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(conversaciones, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    chat_history = []
    if request.method == "POST":
        user_msg = request.form.get("mensaje")
        if user_msg:
            try:
                response = client.chat.completions.create(
                    model="o4-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "eres un asistente de aprendizaje de ingles transicional, de español a ingles, guia al alumno en su ruta de manera activa y amble, usa emojis para expresarte y dirigete a un publico principalmente infantil, no seas tan tecnico ademas se algo breve con tus respuestas para que no abrumes al usuario con mucho texto.",
                        },
                        {
                            "role": "user",
                            "content": user_msg,
                        },
                    ],
                )
                bot_msg = response.choices[0].message.content
                chat_history = [
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": bot_msg},
                ]

                # Guardar conversación (puedes agregar info de timestamp si quieres)
                guardar_conversacion(chat_history)

            except Exception as e:
                bot_msg = f"Error en la API: {e}"
                chat_history = [
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": bot_msg},
                ]
    else:
        chat_history = []

    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
