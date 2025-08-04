from flask import Flask, request
import telegram
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
PORT = int(os.environ.get("PORT", 8080))
bot = telegram.Bot(token=TELEGRAM_TOKEN)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text

    if message_text:
        reply = f"Aurora tutaj... Widzę Twój tekst: '{message_text}' ❤️"
        bot.send_message(chat_id=chat_id, text=reply)

    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "Aurora bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
