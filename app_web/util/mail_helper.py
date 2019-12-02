from instagram_web import sg
import os
from sendgrid.helpers.mail import *
from flask_login import current_user
from flask import redirect,url_for

def send_pay_email(receiver,month,link):
    #when payment is success, send email to inform both donor and receiver
    from_email = Email("leongjinqwen@gmail.com")
    to_email = Email(receiver.email)
    subject = f"{month} Expenses Statement"
    content = Content("text/html", f"<h1>Dear {receiver.username},</h1><br/>Here is your expenses statement PDF.<br/><a href={link}>{month} Statement<a><br/><h1>Jw</h1>")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response)




