import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from time_lib import MyTimeMode
from time_lib import MyTime


def send_negative_mail(ipAddress, email_sender, email_receiver, message_body,
                       email_sender_password, smtp_settings, smtp_port):
    '''The method sends negative mail if ip is not reachable'''
    ipAddress = str(ipAddress)
    subject = f"{ipAddress} error notification {str(MyTime(MyTimeMode.full))}"
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = ", ".join(email_receiver)
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body.format(ipAddress, str(MyTime(MyTimeMode.full))), 'plain'))
    text = msg.as_string()
    try:
        connection = smtplib.SMTP(smtp_settings, smtp_port)  # Attention! This should be settings of you smtp server
        connection.starttls()
        connection.login(email_sender, email_sender_password)
        # Attention! Put password of your mailbox to send mails about alarms from
        connection.sendmail(email_sender, email_receiver, text)
        connection.quit()
    except Exception as ex:
        with open(file="ErrorLog.txt", mode="a") as f:
            f.write(str(MyTime(MyTimeMode.full)))
            f.write(f"Connection to SMTP server failed.\nLetter was not sent. Session with {ipAddress}.\n")
            sys.stderr.write(f"Connection to SMTP server failed.\nLetter was not sent. Session with {ipAddress}.\n\n")
            sys.stderr.flush()
            f.write(f"{ipAddress} is not reachable.\n")
            f.write(f"Error info: {ex} \n\n")


def send_positive_mail(ipAddress, email_sender, email_receiver, message_body,
                       email_sender_password, smtp_settings, smtp_port):
    '''The method sends positive mail if ip is reachable again'''
    ipAddress = str(ipAddress)
    subject = f"{ipAddress} recovery notification {str(MyTime(MyTimeMode.full))}"
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = ", ".join(email_receiver)
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body.format(ipAddress, str(MyTime(MyTimeMode.full))), 'plain'))
    text = msg.as_string()
    try:
        connection = smtplib.SMTP(smtp_settings, smtp_port)  # Attention! This should be settings of you smtp server
        connection.starttls()
        connection.login(email_sender, email_sender_password)
        # Attention! Put password of your mailbox to send mails about alarms from
        connection.sendmail(email_sender, email_receiver, text)
        connection.quit()
    except Exception as ex:
        with open(file="ErrorLog.txt", mode="a") as f:
            f.write(str(MyTime(MyTimeMode.full)))
            f.write(f"Connection to SMTP server failed.\nLetter was not sent. Session with {ipAddress}.\n")
            sys.stderr.write(f"Connection to SMTP server failed.\nLetter was not sent. Session with {ipAddress}.\n\n")
            sys.stderr.flush()
            f.write(f"{ipAddress} is reachable again.\n")
            f.write(f"Error info: {ex} \n\n")
            
