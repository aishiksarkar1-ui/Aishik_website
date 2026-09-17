import yfinance as yf
import time

# ক্যাশ মেমরি (যাতে সার্ভার ব্লক না হয়)
cache = {
    "data": None,
    "last_updated": 0
}

def get_market_data():
    global cache
    current_time = time.time()
    
    # ক্যাশ চেক (৬০ সেকেন্ড)
    if cache["data"] is not None and (current_time - cache["last_updated"]) < 60:
        return cache["data"]

    # সেক্টরাল এবং মূল ইনডেক্স লিস্ট (নিশ্চিত ও সঠিক সিম্বল সহ)
    indices = {
        "Nifty 50": "^NSEI",
        "Bank Nifty": "^NSEBANK",
        "Nifty IT": "^CNXIT",
        "Nifty Auto": "^CNXAUTO",
        "Nifty Pharma": "^CNXPHARMA",
        "Nifty FMCG": "^CNXFMCG",
        "Nifty Metal": "^CNXMETAL",
        "Nifty Energy": "^CNXENERGY",
        "Nifty Media": "^CNXMEDIA",
        "Nifty Realty": "^CNXREALTY"
    }
    
    # ওপরে টিকারের জন্য Nifty 50-এর স্টক লিস্ট
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

    all_symbols = list(indices.values()) + list(nifty50_stocks.values())
    
    fetched_indices = []
    fetched_stocks = []

    try:
        df = yf.download(all_symbols, period="5d", progress=False)
        closes = df['Close']
        
        def parse_data(name, symbol):
            try:
                series = closes[symbol].dropna()
                if len(series) >= 2:
                    current = float(series.iloc[-1])
                    prev = float(series.iloc[-2])
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

        for name, symbol in indices.items():
            res = parse_data(name, symbol)
            if res: fetched_indices.append(res)
            
        for name, symbol in nifty50_stocks.items():
            res = parse_data(name, symbol)
            if res: fetched_stocks.append(res)
            
    except Exception as e:
        print(f"Bulk Fetch Error: {e}")

    final_data = {
        "indices": fetched_indices,
        "stocks": fetched_stocks
    }
    
    if len(fetched_indices) > 0 or len(fetched_stocks) > 0:
        cache["data"] = final_data
        cache["last_updated"] = current_time
        
    return final_data
