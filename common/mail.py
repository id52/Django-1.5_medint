# - coding: utf-8  -
import threading
from mailsnake import MailSnake
from django.conf import settings


class EmailThread(threading.Thread):
    def __init__(self,  template, message):
        self.template = template
        self.message = message
        self.mapi = MailSnake(settings.EMAIL_HOST_PASSWORD, api='mandrill')

        threading.Thread.__init__(self)

    def run(self):
        print 'SENDING EMAIL'
        res = self.mapi.messages.send_template(template_name=self.template, template_content=[], message=self.message)
        print res
