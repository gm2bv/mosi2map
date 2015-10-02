import sendgrid
import logging
from django.conf import settings

class webmail:
    __username   = settings.SENDGRID_USER
    __password   = settings.SENDGRID_PASS
    __hd_from    = settings.MAIL_FROM
    __hd_subject = "{appname}からのお知らせ"
    __baseurl    = settings.SITE_URL
    __body       = """
以下のイベントに招待されています。
【詳細】
{detail}

【日時】
{deadline}

【メッセージ】
{message}

--------------------------------
このメールは{appname}サービスから自動送信されています。
{url}

ご利用ありがとうございました。
--------------------------------"""

    
    def __init__(self, event):
        event_url = self.__baseurl + "/event/" + event.identifier

        self.__evlp = sendgrid.Mail()
        self.__evlp.set_from(self.__hd_from)
        self.__evlp.set_subject(
            self.__hd_subject.format(
                **{
                    'appname': settings.SITE_NAME
                }
            )
        )
        self.__evlp.set_text(
            self.__body.format(
                **{
                    'appname' : settings.SITE_NAME,
                    'url'     : settings.SITE_URL,
                    'detail'  : event_url,
                    'deadline': event.deadline,
                    'message' : event.message,
                }
            )
        )

    def add_to(self, addr):
        self.__evlp.add_to(addr)

    def send(self):
        sg = sendgrid.SendGridClient(self.__username, self.__password)
        if not settings.MAIL_DEBUG:
            status, msg = sg.send(self.__evlp)
            print (status)
            print (msg)

    
