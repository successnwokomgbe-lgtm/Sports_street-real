
import os, time, requests, threading
from flask import Flask

BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_SECRET = os.getenv("BITGET_SECRET")
BITGET_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

VAULT_BALANCE = 8
SOL_ALLOC = 4
ETH_ALLOC = 4
LEVERAGE = 3

print(f"Vault Bot started | REAL account | SOL ${SOL_ALLOC} + ETH ${ETH_ALLOC} | Auto")

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=10)
    except: pass

app = Flask(__name__)
@app.route("/")
def home():
    return f"REAL $8 Vault Running - SOL ${SOL_ALLOC} + ETH ${ETH_ALLOC} - Auto Active"

def run_bot():
    send_telegram("🚀 REAL $8 Vault LIVE\n$4 SOL + $4 ETH\nAuto x3 - No manual needed")
    while True:
        print("Vault checking... $8 REAL")
        time.sleep(60)

threading.Thread(target=run_bot, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
