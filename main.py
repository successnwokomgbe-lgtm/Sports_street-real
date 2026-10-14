import os, threading, time, telebot
from flask import Flask
import ccxt

# --- ENV ---
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_SECRET = os.getenv("BITGET_SECRET")
BITGET_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set!")

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# Bitget REAL exchange
exchange = ccxt.bitget({
    'apiKey': BITGET_API_KEY,
    'secret': BITGET_SECRET,
    'password': BITGET_PASSPHRASE,
    'options': {'defaultType': 'spot'}
})

@app.route('/')
def home():
    return "Vault Bot LIVE - Bitget REAL"

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, 
        "✅ **Vault Bot LIVE**\n"
        "Exchange: Bitget REAL\n"
        "Strategy: SOL $4 + ETH $4 x3\n"
        "Auto loop: ON\n\n"
        "Commands:\n"
        "/balance - Check real balance\n"
        "/run - Start vault loop")

@bot.message_handler(commands=['balance'])
def balance(msg):
    try:
        bal = exchange.fetch_balance()
        usdt = bal.get('USDT', {}).get('free', 0)
        bot.reply_to(msg, f"💰 REAL Balance: {usdt} USDT\nOn Bitget")
    except Exception as e:
        bot.reply_to(msg, f"❌ Error: {e}\nCheck API keys in Render")

def run_bot():
    print("Vault Bot started | Bitget REAL | SOL $4 + ETH $4 x3 | Auto loop")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Bot crash {e}, restart in 5s")
            time.sleep(5)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
