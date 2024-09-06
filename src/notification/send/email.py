import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load configuration from environment variables
SMTP_SERVER = os.environ.get('SMTP_SERVER')  # e.g., 'smtp.sendgrid.net'
SMTP_PORT = os.environ.get('SMTP_PORT', 587)  # Default to port 587
USERNAME = os.environ.get('SMTP_USERNAME')  # Your Sendgrid username or API key
PASSWORD = os.environ.get('SMTP_PASSWORD')  # Your Sendgrid password or API key
FROM_EMAIL = os.environ.get('FROM_EMAIL')  # Sender email address

def notification(message):
    try:
        # Load the message from JSON format
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        TO_EMAIL = message["username"]

        # Email content
        subject = "MP3 Download"
        body = f"Dear Customer,\n\nYour MP3 file with ID {mp3_fid} is now ready for download.\n\nBest regards,\nYour Service Team"

        # Create the Email
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server = smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT))
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return str(e)
