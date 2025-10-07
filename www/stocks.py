import os
import json
from datetime import date
import yfinance as yf

# ---------------- CONFIGURATION ----------------
BASE_DIR = os.path.join(os.environ["USERPROFILE"], "StocksData")
os.makedirs(BASE_DIR, exist_ok=True)

TICKER_FILE = os.path.join(BASE_DIR, "tickers.txt")
HIST_CACHE_FILE = os.path.join(BASE_DIR, "historical_cache.json")
BATCH_SIZE = 200  # batch size for yfinance.download

# Terminal color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# ---------------- LOAD TICKERS ----------------
if os.path.exists(TICKER_FILE):
    with open(TICKER_FILE, "r") as f:
        tickers = [t.strip() for t in f if t.strip()]
else:
    tickers = ["AAPL","MSFT","TSLA"]  # fallback minimal list

# ---------------- LOAD HISTORICAL CACHE ----------------
hist_cache = {}
if os.path.exists(HIST_CACHE_FILE):
    with open(HIST_CACHE_FILE, "r") as f:
        hist_cache = json.load(f)
if "data" not in hist_cache:
    hist_cache = {"data": {}}

# ---------------- FILTER UNCACHED TICKERS ----------------
symbols_to_fetch = [t for t in tickers if t not in hist_cache["data"]]

# ---------------- FETCH HISTORICAL DATA ----------------
if symbols_to_fetch:
    print(f"Fetching historical data for {len(symbols_to_fetch)} tickers...")
    for i in range(0, len(symbols_to_fetch), BATCH_SIZE):
        batch = symbols_to_fetch[i:i+BATCH_SIZE]
        print(f"Fetching batch {i//BATCH_SIZE + 1} of {len(symbols_to_fetch)//BATCH_SIZE + 1}...")
        try:
            data = yf.download(batch, period="1y", group_by='ticker', threads=True)
            for symbol in batch:
                if symbol in data:
                    hist_cache["data"][symbol] = {
                        "7d": data[symbol]["Close"].tail(7).tolist(),
                        "30d": data[symbol]["Close"].tail(30).tolist(),
                        "1y": data[symbol]["Close"].tolist()
                    }
        except Exception as e:
            print(f"Batch failed for {batch}: {e}")

    # Save cache
    with open(HIST_CACHE_FILE, "w") as f:
        json.dump(hist_cache, f)
    print("Historical data cached successfully.")
else:
    print("All historical data already cached. Dashboard will run instantly.")

# ---------------- DASHBOARD LOGIC ----------------
def rate_stock(price, hist_7d, hist_30d, hist_1y):
    if not hist_7d or not hist_30d or not hist_1y:
        return "No Data", RESET

    low_7d = min(hist_7d)
    low_30d = min(hist_30d)
    high_1y = max(hist_1y)
    pct_to_1y_high = (high_1y - price) / price * 100

    # Assign BUY / HOLD / SELL based on buy-low strategy
    if price <= low_7d:  # near 7-day low → BUY
        return f"BUY (+{pct_to_1y_high:.1f}%)", GREEN
    elif price <= low_30d:  # near 30-day low → HOLD
        return f"HOLD (+{pct_to_1y_high:.1f}%)", YELLOW
    else:  # price is high → SELL
        return f"SELL (+{pct_to_1y_high:.1f}%)", RED

# ---------------- BUILD DASHBOARD ----------------
dashboard = []
for symbol, prices in hist_cache["data"].items():
    hist_7d = prices.get("7d", [])
    hist_30d = prices.get("30d", [])
    hist_1y = prices.get("1y", [])
    current_price = hist_7d[-1] if hist_7d else None
    if current_price is None:
        continue
    rating_text, color = rate_stock(current_price, hist_7d, hist_30d, hist_1y)
    dashboard.append({
        "symbol": symbol,
        "price": current_price,
        "rating": rating_text,
        "color": color
    })

# ---------------- PRINT DASHBOARD ----------------
print(f"\n{'Symbol':<8} {'Price':<8} {'Rating'}")
print("-"*40)
for stock in dashboard:
    print(f"{stock['symbol']:<8} ${stock['price']:<8.2f} {stock['color']}{stock['rating']}{RESET}")