import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, jsonify

# আপডেট করা ফাংশনটি ইম্পোর্ট করা হলো
from market_data import get_market_data

app = Flask(__name__)

def get_sheet():
    google_creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    if not google_creds_json:
        return None
        
    try:
        creds_dict = json.loads(google_creds_json)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("Website_Contacts").sheet1 
        return sheet
    except Exception as e:
        print(f"Google Sheets Error: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/risk-profiling')
def risk_profiling():
    return render_template('risk_profile.html')

@app.route('/financial-planning')
def financial_planning():
    return render_template('financial_planning.html')

@app.route('/sip-calculator')
def sip_calculator():
    return render_template('sip_calculator.html')

@app.route('/inflation-calculator')
def inflation_calculator():
    return render_template('inflation_calculator.html')

@app.route('/market-insight')
def market_insight():
    return render_template('market_insight.html')

@app.route('/connect')
def connect():
    return render_template('connect.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/blog-post')
def blog_post():
    return render_template('blog_post.html')

@app.route('/blog/beyond-the-noise')
def beyond_the_noise():
    return render_template('beyond_the_noise.html')

# লাইভ টিকার API (উভয় ডেটা একসাথে পাঠাবে)
@app.route('/api/live-ticker')
def live_ticker_api():
    try:
        data = get_market_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.form
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message', 'N/A')
        
        sheet = get_sheet()
        if sheet:
            sheet.append_row([name, email, phone, message])
            return jsonify({'status': 'success', 'message': 'Thank you! Your details have been recorded.'})
        else:
            return jsonify({'status': 'error', 'message': 'Database connection error.'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
