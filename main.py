import os
import ccxt
from flask import Flask, render_template_string
app = Flask(__name__)
exchange = ccxt.bitget({
    'apiKey': os.getenv('BITGET_API_KEY'),
    'secret': os.getenv('BITGET_SECRET'),
    'password': os.getenv('BITGET_PASSPHRASE'),
    'options': {'defaultType': 'swap'}
})
HTML = """
<html><head><title>LIVE Bot</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{background:#0a0a0a;color:#fff;font-family:Arial;padding:20px;text-align:center}
.card{background:#1a1a1a;padding:20px;border-radius:15px;margin:10px}
.green{color:#00ff88}</style></head><body>
<h1>SPORTS-STREET LIVE</h1>
<div class="card"><h2>Status: <span class="green">LIVE CONNECTED</span></h2>
<p>Balance: {{balance}} USDT</p></div></body></html>
"""
@app.route('/')
def home():
    try:
        bal = exchange.fetch_balance()
        usdt = bal.get('USDT',{}).get('free','0')
        return render_template_string(HTML, balance=usdt)
    except Exception as e:
        return f"Bot LIVE! Add API keys in Render: {e}"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
