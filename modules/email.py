import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, email, password):
        self.sender_email = email
        self.password = password

    def SendEmail(self, message, receiver_email) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = 'KEY'
            msg.attach(MIMEText(message, 'plain'))
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, receiver_email, msg.as_string())
            return True
        except Exception:
            return False