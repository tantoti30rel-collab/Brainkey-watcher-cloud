import requests
import time

# Konfigurasi
TELEGRAM_TOKEN = "8445382217:AAHUf4vyrhypYm-eUUAFu-y5E1YmmW7G1mQ"
CHAT_ID = "8355376419"
FINNHUB_API_KEY = "d2a1bkpr01qvhsfvktegd2a1bkpr01qvhsfvktf0"

# Daftar aset
ASSETS = {
    "stock_us": ["MSFT", "GOOGL", "AAPL", "META", "NVDA", "HUBS"],
    "stock_id": ["BBCA.JK", "TLKM.JK", "BMRI.JK", "UNVR.JK", "MDKA.JK"],
    "crypto": ["bitcoin", "ethereum", "sui", "vechain", "pepe"]
}

# Fungsi kirim pesan ke Telegram
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# Ambil harga saham dari Finnhub
def get_stock_price(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    r = requests.get(url).json()
    return r.get("c"), r.get("h"), r.get("l")

# Ambil harga crypto dari CoinGecko
def get_crypto_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd,idr"
    r = requests.get(url).json()
    return r[coin_id]["usd"], r[coin_id]["idr"]

# Analisa sederhana untuk rekomendasi
def analyze_price(current, high, low):
    if current <= low * 1.02:
        return "💰 *Rekomendasi Beli* — Harga mendekati titik terendah"
    elif current >= high * 0.98:
        return "📈 *Pertimbangkan Jual* — Harga mendekati titik tertinggi"
    else:
        return "🤝 *Hold* — Belum ada sinyal kuat"

# Main loop
def main():
    while True:
        message = "📊 *Laporan Harga Real-time & Rekomendasi*\n\n"

        # Saham US
        message += "🇺🇸 *Saham Amerika*\n"
        for stock in ASSETS["stock_us"]:
            price, high, low = get_stock_price(stock)
            if price:
                rec = analyze_price(price, high, low)
                message += f"{stock} — ${price} | {rec}\n"

        # Saham Indonesia
        message += "\n🇮🇩 *Saham Indonesia*\n"
        for stock in ASSETS["stock_id"]:
            price, high, low = get_stock_price(stock)
            if price:
                rec = analyze_price(price, high, low)
                message += f"{stock} — Rp{price*16000:,.0f} | {rec}\n"

        # Crypto
        message += "\n🪙 *Crypto*\n"
        for coin in ASSETS["crypto"]:
            usd, idr = get_crypto_price(coin)
            rec = analyze_price(usd, usd*1.05, usd*0.95)  # Range +/-5%
            message += f"{coin.upper()} — ${usd} / Rp{idr:,.0f} | {rec}\n"

        send_telegram(message)
        time.sleep(3600)  # Cek setiap 1 jam

if __name__ == "__main__":
    main()
