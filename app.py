import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Google Sheets কানেকশন ফাংশন
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

# ==========================================
# ওয়েবসাইট রাউটস (Pages)
# ==========================================

# হোমপেজ রুট
@app.route('/')
def home():
    return render_template('index.html')

# About পেজ রুট
@app.route('/about')
def about():
    return render_template('about.html')

# Learn পেজ রুট
@app.route('/learn')
def learn():
    return render_template('learn.html')

# Self-Risk Profiling পেজ রুট
@app.route('/risk-profiling')
def risk_profiling():
    return render_template('risk_profile.html')

@app.route('/financial-planning')
def financial_planning():
    return render_template('financial_planning.html')

@app.route('/sip-calculator')
def sip_calculator():
    return render_template('sip_calculator.html')

# ==========================================
# এপিআই এবং ফর্ম সাবমিশন
# ==========================================

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

# অ্যাপ রান করার কোড
if __name__ == '__main__':
    app.run(debug=True)
