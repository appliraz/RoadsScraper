import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dateparser import getTodayAsString

SENDER_EMAIL = "USE_SENDER_EMAIL_ADDRESS_HERE"
APP_PASSWORD = "USE_APP_PASSWORD_HERE"
RECEIVERS = ["FOO_WILL_RECEIVE@THIS_EMAIL.COM", "AND_HIS_FRIEND@AS_WELL.COM"]

def getReceivers():
    return RECEIVERS

def getTodayEmailTitle():
    today = getTodayAsString()
    return f"What is expected on the road for today - {today}"

def send_email(subject, body, to):
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = APP_PASSWORD
    msg['From'] = SENDER_EMAIL
    msg['To'] = to
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(body, 'html'))

    # create SMTP session
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], password)

    # send the message via the server
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

def generateMessage(title, description):
    message =f"<div><strong>{title}</strong><p>{description}<br/></p></div>"
    return message

def getMessageToSend(events):
    message = "<div style='direction: rtl;'>"
    for title, description in events:
        message += generateMessage(title, description)
        message+= "<br/>"
    message += "</div>"
    return message

def sendEmailsToReceivers(events):
    msg_title = getTodayEmailTitle()
    message = getMessageToSend(events)
    receivers = getReceivers()
    email_count = 1
    for receiver in receivers:
        print(f"sending email {email_count}")
        send_email(msg_title, message, receiver)
        email_count += 1

def handle404(error=""):
    receivers = getReceivers()
    for receiver in receivers:
        try:
            send_email("404 Received", f"404 for some reason...\n{error}", receiver)
        except Exception as e:
            print(e)
