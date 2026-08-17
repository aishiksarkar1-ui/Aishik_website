import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask

app = Flask(__name__)

# গুগল শিটের সাথে কানেকশন তৈরি করার ফাংশন
def get_sheet():
    # আমরা পরে Render-এ গুগল ক্রেডেনশিয়ালস সেট করব যাতে গিটহাবে সিক্রেট লিক না হয়
    google_creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    
    if not google_creds_json:
        return "Google Credentials not found!"
        
    try:
        creds_dict = json.loads(google_creds_json)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # 'Website_Contacts' নামের শিটটি ওপেন করবে
        sheet = client.open("Website_Contacts").sheet1 
        return sheet
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return "<h1>Hello Aishik! Backend with Google Sheets is ready to connect.</h1>"

if __name__ == '__main__':
    app.run(debug=True)
