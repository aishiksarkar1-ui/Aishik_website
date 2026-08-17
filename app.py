import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template

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
    # render_template ফাংশনটি templates ফোল্ডার থেকে index.html ফাইলটি লোড করবে
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
