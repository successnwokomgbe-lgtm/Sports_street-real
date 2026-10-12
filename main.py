import os
import threading
import ccxt
from flask import Flask, render_template_string
import telebot

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
HTML = """<html><head><title>LIVE Bot</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#0a0a0a;color:#fff;font-family:Arial;padding:20px}
.card{background:#1a1a1a;padding:20px;border-radius:15px}
.green{color:#00ff88}</style></head><body>
<h1>SPORTS-STREET LIVE</h1>
<div class="card"><h2>Status: <span class="green">LIVE</span></h2>
<p>Balance: {{balance}} USDT</p></div></body></html>"""

@app.route('/')
def home():
    try:
        bal = exchange.fetch_balance()
        usdt = bal.get('USDT',{}).get('free','0')
        return render_template_string(HTML, balance=usdt)
    except Exception as e:
        return f"Bot LIVE! {e}"

def run_telebot():
   
