import yfinance as yf

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
    
    # ওপরে টিকারের জন্য Nifty 50-এর টপ স্টক লিস্ট
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

    # ডেটা ফেচ করার কমন ফাংশন
    def fetch_info(ticker_dict):
        result = []
        for name, symbol in ticker_dict.items():
            try:
                info = yf.Ticker(symbol).fast_info
                current = info.last_price
                prev = info.previous_close
                change = current - prev
                pct = (change / prev) * 100
                result.append({
                    "name": name,
                    "price": round(current, 2),
                    "change": round(change, 2),
                    "change_percent": round(pct, 2)
                })
            except Exception as e:
                print(f"Error fetching {name}: {e}")
        return result
        
    # দুটো আলাদা লিস্ট একসাথে রিটার্ন করা হলো
    return {
        "indices": fetch_info(indices),
        "stocks": fetch_info(nifty50_stocks)
    }
