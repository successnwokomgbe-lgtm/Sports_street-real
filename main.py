
import os, threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler
import ccxt

app = Flask(__name__)
@app.route('/')
def home():
    return "Vault Bot LIVE - REAL 4 USDT"

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("BITGET_API_KEY")
SECRET = os.getenv("BITGET_SECRET")
PASSPHRASE = os.getenv("BITGET_PASSPHRASE")

def get_real_balance():
    try:
        ex = ccxt.bitget({'apiKey': API_KEY, 'secret': SECRET, 'password': PASSPHRASE})
        b = ex.fetch_balance()
        return b['USDT']['free']
    except Exception as e:
        return str(e)

async def balance(update, context):
    bal = get_real_balance()
    await update.message.reply_text(f"💰 REAL Balance: {bal}\nUSDT\nOn Bitget")

async def run(update, context):
    await update.message.reply_text("🚀 Vault Bot Running...")

def start_bot():
    if not TOKEN:
        print("NO TOKEN")
        return
    tg_app = ApplicationBuilder().token(TOKEN).build()
    tg_app.add_handler(CommandHandler("balance", balance))
    tg_app.add_handler(CommandHandler("run", run))
    tg_app.run_polling()

threading.Thread(target=start_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
