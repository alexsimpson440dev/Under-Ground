import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()

class EmailAPI(object):
    def __init__(self):
        pass