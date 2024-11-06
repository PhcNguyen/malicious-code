
# Copyright (C) PhcNguyen Developers
# Distributed under the terms of the Modified TUDL License.

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class EmailSender:
    def __init__(
        self, 
        sender_email: str, 
        password: str, 
        smtp_server: str = 'smtp.gmail.com', 
        smtp_port: int = 587
    ) -> None:
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def sendEmail(
        self, 
        receiver_email: str, 
        subject: str, 
        message: str
        ) -> bool:
        try:
            # Set up the email server connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure the connection
            server.login(self.sender_email, self.password)
            
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            
            # Add the email content
            msg.attach(MIMEText(message, 'plain'))
            
            # Send the email
            server.sendmail(self.sender_email, receiver_email, msg.as_string())
            server.quit()
            return True

        except Exception:
            return False