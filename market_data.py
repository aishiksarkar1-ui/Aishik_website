import yfinance as yf

def get_nifty_live_data():
    # Yahoo Finance-এর জন্য NSE স্টকের সিম্বল (শেষে .NS দিতে হয়)
    tickers = {
        "Nifty 50": "^NSEI",
        "Bank Nifty": "^NSEBANK",
        "Reliance": "RELIANCE.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Infosys": "INFY.NS",
        "TCS": "TCS.NS",
        "ITC": "ITC.NS"
    }
    
    market_data = []
    
    for name, symbol in tickers.items():
        try:
            ticker_obj = yf.Ticker(symbol)
            info = ticker_obj.fast_info # fast_info খুব দ্রুত লাইভ প্রাইজ টেনে আনে
            
            current_price = info.last_price
            prev_close = info.previous_close
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
            
            market_data.append({
                "name": name,
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2)
            })
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            
    return market_data
