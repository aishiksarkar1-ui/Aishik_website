import yfinance as yf
import time
from concurrent.futures import ThreadPoolExecutor

# ক্যাশ মেমরি (যাতে পেজ রিফ্রেশ করলে সার্ভার ব্লক না হয়)
cache = {
    "data": None,
    "last_updated": 0
}

def fetch_stock_data(name, symbol):
    try:
        # fast_info সবচেয়ে দ্রুত এবং নিখুঁতভাবে লাইভ ডেটা দেয়
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        
        current = info.last_price
        prev = info.previous_close
        
        if current and prev:
            change = current - prev
            pct = (change / prev) * 100
            return {
                "name": name,
                "price": round(current, 2),
                "change": round(change, 2),
                "change_percent": round(pct, 2)
            }
    except Exception:
        # যদি fast_info কোনো কারণে কাজ না করে, তবে history ব্যবহার করবে (ব্যাকআপ)
        try:
            hist = ticker.history(period="5d")
            if len(hist) >= 2:
                current = float(hist['Close'].iloc[-1])
                prev = float(hist['Close'].iloc[-2])
                change = current - prev
                pct = (change / prev) * 100
                return {
                    "name": name,
                    "price": round(current, 2),
                    "change": round(change, 2),
                    "change_percent": round(pct, 2)
                }
        except Exception:
            pass
    return None

def get_market_data():
    global cache
    current_time = time.time()
    
    # ৬০ সেকেন্ডের ক্যাশ (বারবার রিফ্রেশ করলেও ব্লক হবে না)
    if cache["data"] is not None and (current_time - cache["last_updated"]) < 60:
        return cache["data"]

    # আপনার আগের অরিজিনাল Nifty Indices
    indices = {
        "Nifty 50": "^NSEI",
        "Bank Nifty": "^NSEBANK",
        "Nifty IT": "^CNXIT",
        "Nifty Auto": "^CNXAUTO",
        "Nifty Pharma": "^CNXPHARMA",
        "Nifty FMCG": "^CNXFMCG",
        "Nifty Metal": "^CNXMETAL",
        "Nifty Energy": "^CNXENERGY",
        "Nifty Realty": "^CNXREALTY",
        "Nifty Infra": "^CNXINFRA"
    }
    
    # Nifty 50-এর টপ ২০টি স্টক
    nifty50_stocks = {
        "Reliance": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Infosys": "INFY.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "SBI": "SBIN.NS",
        "Bharti Airtel": "BHARTIARTL.NS",
        "ITC": "ITC.NS",
        "L&T": "LT.NS",
        "Bajaj Finance": "BAJFINANCE.NS",
        "Maruti": "MARUTI.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "Sun Pharma": "SUNPHARMA.NS",
        "Kotak Bank": "KOTAKBANK.NS",
        "Axis Bank": "AXISBANK.NS",
        "Asian Paints": "ASIANPAINT.NS",
        "Titan": "TITAN.NS",
        "Tata Steel": "TATASTEEL.NS",
        "UltraTech": "ULTRACEMCO.NS",
        "NTPC": "NTPC.NS"
    }

    fetched_indices = []
    fetched_stocks = []

    # একসাথে সব ডেটা আলাদা আলাদা করে টানা হচ্ছে (যাতে একটা ফেল করলে অন্যটা বাদ না যায়)
    with ThreadPoolExecutor(max_workers=20) as executor:
        index_futures = {executor.submit(fetch_stock_data, name, sym): name for name, sym in indices.items()}
        stock_futures = {executor.submit(fetch_stock_data, name, sym): name for name, sym in nifty50_stocks.items()}
        
        for future in index_futures:
            res = future.result()
            if res: fetched_indices.append(res)
            
        for future in stock_futures:
            res = future.result()
            if res: fetched_stocks.append(res)

    final_data = {
        "indices": fetched_indices,
        "stocks": fetched_stocks
    }
    
    # ডেটা সফলভাবে আসলে ক্যাশে সেভ হবে
    if len(fetched_indices) > 0 or len(fetched_stocks) > 0:
        cache["data"] = final_data
        cache["last_updated"] = current_time
        
    return final_data
