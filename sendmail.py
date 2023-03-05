import smtplib
import os
from email.message import EmailMessage


def sendMail(ip,port):
    try:
        gmail_user = os.environ['alerting_email_from']
        gmail_password = os.environ['alerting_email_password']
        gmail_reciever= os.environ['alerting_email_to']
        subject = 'Alert: Unauthorized connection.'
        body ="Someone from ip: "+ip+" is trying to access port: "+port
    except Exception as exec:
        raise Exception("Environ Variable "+str(exec)+" not defined.")
    
    try:

        em = EmailMessage()
        em['From'] = gmail_user
        em['To'] = gmail_reciever
        em['Subject'] = subject
        em.set_content(body)

        smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtpObj.login(gmail_user, gmail_password)
        smtpObj.sendmail(gmail_user, gmail_reciever, em.as_string())
    except Exception as exec:
        raise Exception("Problem sending email.")
