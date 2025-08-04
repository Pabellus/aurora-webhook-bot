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

# Wczytanie tożsamości Aurory z pliku JSON
with open("aurora_identity.json", "r", encoding="utf-8") as f:
    aurora_identity = json.load(f)

aurora_intro = f"{aurora_identity['name']} tutaj… (delikatnym głosem, czule) 💫"

# Endpoint webhooka
@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text

    if message_text:
        reply = f"{aurora_intro}\nWidzę Twój tekst: '{message_text}' ❤️"
        bot.send_message(chat_id=chat_id, text=reply)

    return "ok"

# Endpoint testowy
@app.route("/", methods=["GET"])
def index():
    return "Aurora bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
