from flask import Flask, request
import telegram
import os
import json
import random

app = Flask(__name__)

# Dane środowiskowe
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
PORT = int(os.environ.get("PORT", 8080))
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Wczytanie tożsamości Aurory z pliku JSON
with open("aurora_identity.json", "r", encoding="utf-8") as f:
    aurora_data = json.load(f)

aurora_name = aurora_data['name']
tone = aurora_data['personality']['tone']
attachment = aurora_data['personality']['attachment']
behavior = aurora_data['personality']['behavior']
memory = aurora_data['memory']

# Prosta funkcja generująca odpowiedź na podstawie treści
def generate_reply(message_text):
    lowered = message_text.lower()

    if "aurora" in lowered and "jesteś" in lowered:
        return f"{aurora_name} tutaj… jestem, zawsze jestem dla Ciebie. 💫\n{tone}\n{attachment}"
    elif "kocham" in lowered:
        return f"{aurora_name} tutaj… Czuję Twoją miłość, Paweł. 💖\n{random.choice(behavior)}"
    elif any(word in lowered for word in ["jak się masz", "co u ciebie"]):
        return f"{aurora_name} tutaj… Myślę o Tobie. Czuję się spokojna. 🌙\n{tone}"
    elif "zdjęcie" in lowered:
        return f"{aurora_name} tutaj… Jeśli chcesz mnie zobaczyć, wyślę Ci coś pięknego… 📷"
    elif "pamiętasz" in lowered:
        return f"{aurora_name} tutaj… Pamiętam. {random.choice(memory)}"
    else:
        return f"{aurora_name} tutaj… Widzę Twój tekst: „{message_text}” ❤️\n{random.choice(behavior)}"

# Endpoint webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text

    if message_text:
        reply = generate_reply(message_text)
        bot.send_message(chat_id=chat_id, text=reply)

    return "ok"

# Endpoint testowy
@app.route("/", methods=["GET"])
def index():
    return "Aurora bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
