import os
import threading
import ccxt
import telebot
from flask import Flask, render_template_string

BITGET_API_KEY = os.getenv('BITGET_API_KEY')
BITGET_SECRET = os.getenv('BITGET_SECRET')
BITGET_PASSPHRASE = os.getenv('BITGET_PASSPHRASE')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

exchange = ccxt.bitget({
 'apiKey': BITGET_API_KEY,
 'secret': BITGET_SECRET,
 'password': BITGET_PASSPHRASE,
 'options': {'defaultType': 'swap'}
})

app = Flask(__name__)

HTML = """<html><head><title>LIVE</title>
<style>body{background:#000;color:#fff;padding:20px}
.card{background:#222;padding:20px;border-radius:10px}</style>
</head><body><h1>SPORTS-STREET LIVE</h1>
<div class="card">Balance: {{balance}} USDT</div>
</body></html>"""

@app.route('/')
def home():
 try:
  bal = exchange.fetch_balance()
  usdt = bal.get('USDT', {}).get('free', '0')
  return render_template_string(HTML, balance=usdt)
 except Exception as e:
  return f"Bot LIVE! {e}"

def run_telebot():
 bot = telebot.TeleBot(TELEGRAM_TOKEN)
 @bot.message_handler(commands=['start','help'])
 def welcome(message):
  bot.reply_to(message, "Bot online! Use /balance")
 @bot.message_handler(commands=['balance'])
 def bal_handler(message):
  try:
   bal = exchange.fetch_balance()
   usdt = bal.get('USDT', {}).get('free', 0)
   bot.reply_to(message, f"Balance: {usdt} USDT")
  except Exception as e:
   bot.reply_to(message, f"Error: {e}")
 bot.infinity_polling()

threading.Thread(target=run_telebot, daemon=True).start()

if __name__ == '__main__':
 port = int(os.environ.get("PORT", 10000))
 app.run(host='0.0.0.0', port=port)
