from app.main.views import send_asyn_mail
from flask_mail import Message
from threading import Thread
from app import create_app, mail
from flask import render_template

app = create_app()

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to,subject, template, **kwargs ):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], 
                        recipients=to)
    msg.body = render_template(template + '.txt', **kwargs)
    thr = Thread(target=send_asyn_mail, args=[app, msg])
    thr.start()
    return thr