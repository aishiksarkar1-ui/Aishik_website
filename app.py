import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# গুগল শিটের সাথে কানেকশন তৈরি করার ফাংশন
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
        print(e)
        return None

# ওয়েবসাইটের মূল পেজ
@app.route('/')
def home():
    return render_template('index.html')

# কন্টাক্ট ফর্ম সাবমিট হলে এই রুটটি কাজ করবে এবং ডেটা গুগল শিটে পাঠাবে
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
            # গুগল শিটের রো-তে ডেটা যুক্ত করা (Name, Email, Phone, Message)
            sheet.append_row([name, email, phone, message])
            return jsonify({'status': 'success', 'message': 'Thank you! Your details have been recorded.'})
        else:
            return jsonify({'status': 'error', 'message': 'Database connection error.'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
