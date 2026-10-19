import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Vault Bot LIVE - Bitget REAL"

# --- Telegram bot part (if you use python-telegram-bot) ---
# Put your bot code here, make sure bot is defined BEFORE you use it
# Example:
# from telegram.ext import Application
# TOKEN = os.getenv("TELEGRAM_TOKEN")
# application = Application.builder().token(TOKEN).build()
# application.run_polling() in a thread

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    run_flask()
