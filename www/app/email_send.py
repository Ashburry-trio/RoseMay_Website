from __future__ import annotations

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser
import secrets
from time import time

def random_string(length):
    return secrets.token_urlsafe(length)


config = ConfigParser()
config.read('secrets.ini')
if not config.has_section('email') or not 'from' in config['email'].keys() \
        or not 'smtp_server' in config['email'].keys() or not 'password' in config['email'].keys():
    config['email'] = {}
    config['email']['from'] = 'from email'
    config['email']['password'] = 'your email password'
    config['email']['smtp_server'] = 'smtp.gmail.com'
    raise BaseException('Missing email configuration in www/app/secrets.ini')

sender_email = config['email']['from']
smtp_server = config['email']['smtp_server']
password = config['email']['password']

message = MIMEMultipart("alternative")
message["Subject"] = "[MyProxyIP] Confirm your email address."
message["From"] = sender_email


def send_email(receiver_email: str, username: str) -> None:
    message["To"] = receiver_email
    confirm = ConfigParser()
    confirm.read('confirm.ini')
    if not confirm.has_section('email'):
        confirm['email'] = {}
    if receiver_email in confirm['email'].keys() and confirm['email'][receiver_email] is not None:
        split_text = confirm['email'][receiver_email].split(' ')
        if time() - split_text[0] < 60 * 10:
            return
    randomstring = random_string(32)
    url = "https://www.MyProxyIP.com/confirm_email?email=" + randomstring
    confirm['email'][receiver_email] = str(int(time())) + ' ' + randomstring
    # Create the plain-text and HTML version of your message
    email_body = """\
    <html>
      <body>
        <p>Hello""" + username + """,<br>
           You are receiving this email because you signed up for MyProxyIP.com<br>
           If it was NOT you please ignore this email.<br>
           Otherwise to confirm your email address please click on the link below:<br>
           <a href=""" + "\'" + url + "\'" + ">" + url + """</a><br>
           Or copy and paste the link above into your browser:</p>
           <p>Thank You, from the MY PROXY IP team.</p>
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    email_body = MIMEText(email_body, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(email_body)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config['email']['smtp_server'], 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
