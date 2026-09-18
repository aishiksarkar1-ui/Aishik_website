import json
import time
import threading
import os
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

CACHE_FILE = 'market_cache.json'
UPDATE_INTERVAL = 300  # ৩০০ সেকেন্ড = ৫ মিনিট
cache_lock = threading.Lock()

def fetch_stock_data(name, symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        current = info.last_price
        prev = info.previous_close
        if current and prev:
            change = current - prev
            pct = (change / prev) * 100
            return {"name": name, "price": round(current, 2), "change": round(change, 2), "change_percent": round(pct, 2)}
    except Exception:
        try:
            hist = ticker.history(period="5d")
            if len(hist) >= 2:
                current = float(hist['Close'].iloc[-1])
                prev = float(hist['Close'].iloc[-2])
                change = current - prev
                pct = (change / prev) * 100
                return {"name": name, "price": round(current, 2), "change": round(change, 2), "change_percent": round(pct, 2)}
        except Exception:
            pass
    return None

def fetch_live_data_internal():
    indices = {
        "Nifty 50": "^NSEI", "Bank Nifty": "^NSEBANK", "Nifty IT": "^CNXIT",
        "Nifty Auto": "^CNXAUTO", "Nifty Pharma": "^CNXPHARMA", "Nifty FMCG": "^CNXFMCG",
        "Nifty Metal": "^CNXMETAL", "Nifty Energy": "^CNXENERGY", "Nifty Realty": "^CNXREALTY",
        "Nifty Infra": "^CNXINFRA"
    }
    nifty50_stocks = {
        "Reliance": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC Bank": "HDFCBANK.NS",
        "Infosys": "INFY.NS", "ICICI Bank": "ICICIBANK.NS", "SBI": "SBIN.NS",
        "Bharti Airtel": "BHARTIARTL.NS", "ITC": "ITC.NS", "L&T": "LT.NS",
        "Bajaj Finance": "BAJFINANCE.NS", "Maruti": "MARUTI.NS", "Tata Motors": "TATAMOTORS.NS",
        "Sun Pharma": "SUNPHARMA.NS", "Kotak Bank": "KOTAKBANK.NS", "Axis Bank": "AXISBANK.NS",
        "Asian Paints": "ASIANPAINT.NS", "Titan": "TITAN.NS", "Tata Steel": "TATASTEEL.NS",
        "UltraTech": "ULTRACEMCO.NS", "NTPC": "NTPC.NS"
    }
    
    fetched_indices = []
    fetched_stocks = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        index_futures = {executor.submit(fetch_stock_data, name, sym): name for name, sym in indices.items()}
        stock_futures = {executor.submit(fetch_stock_data, name, sym): name for name, sym in nifty50_stocks.items()}
        
        for future in index_futures:
            res = future.result()
            if res: fetched_indices.append(res)
            
        for future in stock_futures:
            res = future.result()
            if res: fetched_stocks.append(res)

    return {"indices": fetched_indices, "stocks": fetched_stocks}

# 💥 ব্যাকগ্রাউন্ড থ্রেডিং ফাংশন 💥
def update_cache_loop():
    while True:
        try:
            fresh_data = fetch_live_data_internal()
            if len(fresh_data["indices"]) > 0 or len(fresh_data["stocks"]) > 0:
                with cache_lock:
                    with open(CACHE_FILE, 'w') as f:
                        json.dump({"timestamp": time.time(), "data": fresh_data}, f)
        except Exception as e:
            print(f"Error in background update: {e}")
        time.sleep(UPDATE_INTERVAL)

def start_market_updater():
    updater_thread = threading.Thread(target=update_cache_loop, daemon=True)
    updater_thread.start()

def get_market_data():
    with cache_lock:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                try:
                    return json.load(f)['data']
                except:
                    pass
    return {"indices": [], "stocks": []}
