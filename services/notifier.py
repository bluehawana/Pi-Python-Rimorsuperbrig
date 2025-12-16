import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import threading

class NotifierService:
    def __init__(self, config):
        self.config = config

    def send_email(self, subject, body, attachment_path=None):
        if self.config['MOCK_HARDWARE']:
            print(f"[MOCK] Sending Email: {subject} - {body} (Att: {attachment_path})")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['EMAIL_SENDER']
            msg['To'] = self.config['EMAIL_RECEIVER']
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            if attachment_path:
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename= {attachment_path.split("/")[-1]}')
                    msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.config['EMAIL_SENDER'], self.config['EMAIL_PASSWORD'])
            text = msg.as_string()
            server.sendmail(self.config['EMAIL_SENDER'], self.config['EMAIL_RECEIVER'], text)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_push(self, title, body):
        if self.config['MOCK_HARDWARE']:
            print(f"[MOCK] Sending Push: {title} - {body}")
            return

        if not self.config['PUSHBULLET_API_KEY']:
            return

        try:
            data = {
                'type': 'note',
                'title': title,
                'body': body
            }
            requests.post('https://api.pushbullet.com/api/pushes', 
                        data=data, 
                        auth=(self.config['PUSHBULLET_API_KEY'], ''))
        except Exception as e:
            print(f"Failed to send push: {e}")
