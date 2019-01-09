import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.managers.session_manager import SessionManager
import os

session = SessionManager()


class EmailManager(object):
    def __init__(self):
        self.from_email = "acc.utility.grounds@gmail.com"

    def send_email(self, manager_email):
        msg = MIMEMultipart()
        to_email = manager_email
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = "Utility-Grounds Manager Token"

        body = "Your new Manager Sign-Up token is, " + str(session.get_session('token'))
        msg.attach(MIMEText(body, 'plain'))

        email_server = smtplib.SMTP('smtp.gmail.com', 587)
        email_server.starttls()
        email_server.login(self.from_email, os.environ['EMAIL_PASSWORD'])
        text = msg.as_string()
        email_server.sendmail(self.from_email, to_email, text)
        email_server.quit()
