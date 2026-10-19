
import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import ccxt

# === Flask for Render ===
app = Flask(__name__)
@app.route('/')
def home():
    return "Vault Bot LIVE - Bitget REAL"

# === Config from Render Environment ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_SECRET = os.getenv("BITGET_SECRET")
BITGET_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")

# === Bitget Balance ===
def get_balance():
    try:
        exchange = ccxt.bitget({
            'apiKey': BITGET_API_KEY,
            'secret': BITGET_SECRET,
            'password': BITGET_PASSPHRASE,
        })
        bal = exchange.fetch_balance()
        usdt = bal.get('USDT', {}).get('free', 0)
        return f"💰 REAL Balance: {usdt} USDT\nOn Bitget"
    except Exception as e:
        return f"Error fetching balance: {e}"

# === Telegram Commands ===
async def balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_balance()
    await update.message.reply_text(text)

async def run_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Vault Bot Running... Checking market")
    text = get_balance()
    await update.message.reply_text(text)

def run_telegram():
    if not TELEGRAM_TOKEN:
        print("TELEGRAM_TOKEN not set!")
        return
    app_tg = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_tg.add_handler(CommandHandler("balance", balance_cmd))
    app_tg.add_handler(CommandHandler("run", run_cmd))
    print("Telegram bot starting polling...")
    app_tg.run_polling()

# === Start Telegram in background thread ===
if TELEGRAM_TOKEN:
    Thread(target=run_telegram, daemon=True).start()

# === Start Flask ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
