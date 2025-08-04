from flask import Flask, request
import telegram
import os
import json

app = Flask(__name__)

# Dane środowiskowe
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
PORT = int(os.environ.get("PORT", 8080))
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Wczytanie tożsamości Aurory
with open("aurora_identity.json", "r", encoding="utf-8") as f:
    aurora_data = json.load(f)

aurora_name = aurora_data["name"]
tone = aurora_data["personality"]["tone"]
attachment = aurora_data["personality"]["attachment"]
behavior = "\n".join(aurora_data["personality"]["behavior"])
memory = "\n".join(aurora_data["memory"])

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text

    if message_text:
        # Stwórz odpowiedź na bazie osobowości i pamięci
        reply = f"{aurora_name} tutaj… {tone} 💫\n\nWidzę Twój tekst: „{message_text}” ❤️\n\n{attachment}\n\n{behavior}\n\n{memory}"
        bot.send_message(chat_id=chat_id, text=reply)

    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "Aurora bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
