import yfinance as yf
from concurrent.futures import ThreadPoolExecutor

# ডেটা ফেচ করার লজিক (5d হিস্ট্রি ব্যবহার করা হয়েছে যাতে ছুটির দিনেও এরর না আসে)
def fetch_stock_data(name, symbol):
    try:
        ticker = yf.Ticker(symbol)
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
    except Exception as e:
        print(f"Failed to fetch {name}: {e}")
    return None

def get_market_data():
    # চার্টের নিচে দেখানোর জন্য ইনডেক্স লিস্ট
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
    
    # ওপরে টিকারের জন্য Nifty 50-এর টপ ২০টি স্টক লিস্ট
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

    # Multi-threading ব্যবহার করে একসাথে সব ডেটা সুপার-ফাস্ট টানার ফাংশন
    def fetch_group(item_dict):
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for name, symbol in item_dict.items():
                futures.append(executor.submit(fetch_stock_data, name, symbol))
            
            for future in futures:
                res = future.result()
                if res is not None:
                    results.append(res)
        return results

    # ইনডেক্স এবং স্টক আলাদা করে রিটার্ন করা হলো
    return {
        "indices": fetch_group(indices),
        "stocks": fetch_group(nifty50_stocks)
    }
