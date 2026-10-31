import os
import threading
from flask import Flask
import ccxt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!", 200

# --- Exchange setup ---
# If you have Binance keys, add them in Render Environment as:
# BINANCE_API_KEY and BINANCE_API_SECRET
# If you don't have them, /balance will just tell you.
exchange = None
try:
    api_key = os.getenv("BINANCE_API_KEY", "")
    api_secret = os.getenv("BINANCE_API_SECRET", "")
    if api_key and api_secret:
        exchange = ccxt.binance({
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
        })
except Exception as e:
    print(f"Exchange setup error: {e}")
    exchange = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is online! Send /balance to check balance.")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not exchange:
        await update.message.reply_text("No exchange API keys found. Add BINANCE_API_KEY and BINANCE_API_SECRET in Render Environment.")
        return
    try:
        bal = exchange.fetch_balance()
        usdt = bal.get("total", {}).get("USDT", 0)
        # Show all non-zero balances
        lines = []
        for coin, amount in bal.get("total", {}).items():
            if amount and amount > 0:
                lines.append(f"{coin}: {amount}")
        if not lines:
            lines.append("No balance found.")
        msg = "Your Balance:\n" + "\n".join(lines)
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"Error fetching balance: {e}")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    if not TOKEN:
        print("NO TELEGRAM TOKEN FOUND - Add TELEGRAM_TOKEN in Render Environment")
    else:
        # Flask runs in background thread, bot runs in main thread
        # This fixes the "no current event loop" error
        threading.Thread(target=run_flask, daemon=True).start()
        tg_app = ApplicationBuilder().token(TOKEN).build()
        tg_app.add_handler(CommandHandler("start", start))
        tg_app.add_handler(CommandHandler("balance", balance))
        print("Bot starting...")
        tg_app.run_polling()
