import os
from datetime import datetime

# Example: building the dashboard from cached historical data
dashboard = []
import json
import os

CACHE_FILE = os.path.join("StocksData", "historical_cache.json")

# Make sure the file exists
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        hist_cache = json.load(f)
else:
    # If the cache doesn't exist, start empty
    hist_cache = {"data": {}}

# Now hist_cache["data"] contains all your tickers and their historical prices
print(f"Loaded {len(hist_cache['data'])} tickers from cache")
# Terminal color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
for symbol, prices in hist_cache["data"].items():
    hist_7d = prices.get("7d", [])
    hist_30d = prices.get("30d", [])
    hist_1y = prices.get("1y", [])
    
    if not hist_7d:  # skip if no data
        continue
    
    current_price = hist_7d[-1]  # most recent price

    # Determine rating based on proximity to recent lows
    if current_price <= min(hist_7d):  # near 7-day low
        rating_text = "BUY"
        color = GREEN
    elif current_price <= min(hist_30d):  # near 30-day low
        rating_text = "HOLD"
        color = YELLOW
    else:  # price is high compared to recent lows
        rating_text = "SELL"
        color = RED

    dashboard.append({
        "symbol": symbol,
        "price": current_price,
        "rating": rating_text,
        "color": color
    })
# First, sort the dashboard by rating: BUY first, then HOLD, then SELL
rating_order = {"BUY": 0, "HOLD": 1, "SELL": 2, "Unknown": 3}
dashboard.sort(key=lambda x: rating_order.get(x['rating'], 3))

# ---------------- CONFIG ----------------
BASE_DIR = os.path.join(os.environ["USERPROFILE"], "StocksData")
os.makedirs(BASE_DIR, exist_ok=True)

# Timestamp for file name
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
OUTPUT_FILE = os.path.join(BASE_DIR, f"dashboard_{timestamp}.csv")

# ---------------- WRITE DASHBOARD (CSV FRIENDLY FOR EXCEL) ----------------
with open(OUTPUT_FILE, "w") as f:
    # Header
    f.write("Symbol,Price,Rating,% to 1Y High,Days of Data\n")

    for stock in dashboard:
        rating_text = stock.get("rating", "Unknown")

        # Get 1-year data safely
        hist_1y = hist_cache["data"].get(stock["symbol"], {}).get("1y", [])
        days_of_data = len(hist_1y)
        if hist_1y:
            high_1y = max(hist_1y)
            pct_to_1y_high = (high_1y - stock["price"]) / stock["price"] * 100
        else:
            pct_to_1y_high = 0.0

        # CSV line
        csv_line = f"{stock['symbol']},{stock['price']:.2f},{rating_text},{pct_to_1y_high:.1f},{days_of_data}\n"
        f.write(csv_line)

print(f"\nDashboard saved to: {OUTPUT_FILE}")