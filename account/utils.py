from webbrowser import get
from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_mail(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMIAL_FROM'),
            to=[data['to_email']]
        )
        email.send()
