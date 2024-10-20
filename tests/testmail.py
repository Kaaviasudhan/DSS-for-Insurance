import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

email_user = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASS')
to_email = '2033016mdcs@cit.edu.in'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = to_email
msg['Subject'] = 'Test Email'

body = 'This is a test email'
msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    text = msg.as_string()
    server.sendmail(email_user, to_email, text)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
