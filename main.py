
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

app = Flask(__name__)

@app.route('/')
def home():
    return f"Vault Bot LIVE | REAL ${VAULT_BALANCE} - ${SOL_ALLOC} SOL + ${ETH_ALLOC} ETH x{LEVERAGE} | OK", 200

@app.route('/health')
def health():
    return "OK", 200

def send_telegram(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=10)
    except:
        pass

def bot_loop():
    print(f"Vault Bot started | REAL account | SOL ${SOL_ALLOC} + ETH ${ETH_ALLOC} x{LEVERAGE} | Auto loop")
    send_telegram(f"🚀 REAL ${VAULT_BALANCE} Vault LIVE - ${SOL_ALLOC} SOL + ${ETH_ALLOC} ETH x{LEVERAGE}")
    while True:
        time.sleep(60)

threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
