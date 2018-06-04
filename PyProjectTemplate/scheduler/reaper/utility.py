# -*- coding: utf-8 -*-
from dateutil import parser
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from reaper.settings import *


def get_cur_time():
    return datetime.now(TIMEZONE)


#  ISO 8601 datetime to python datetime
def iso_string_to_datetime(iso_string):
    return parser.parse(iso_string).astimezone(TIMEZONE)


class EmailTool:
    @staticmethod
    def send_email_with_html_and_imgs(host, port, from_addr, to_addr,
                                      subject, html_body, img_files, img_cid_names):
        MIME_msg_root = MIMEMultipart('related')
        MIME_msg_root['From'] = ','.join(from_addr)
        MIME_msg_root['To'] = ','.join(to_addr)
        MIME_msg_root['Subject'] = subject
        MIME_msg_root.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an 'alternative' part,
        # so message agents can decide which they want to display.
        msg_alt = MIMEMultipart('alternative')
        # alt plain text
        msg_plain_text = MIMEText('This is the alternative plain text message.')
        msg_alt.attach(msg_plain_text)
        # alt html text
        msg_html_text = MIMEText(html_body, 'html')
        msg_alt.attach(msg_html_text)

        MIME_msg_root.attach(msg_alt)

        # attach imgs
        for i in range(len(img_files)):
            with open(img_files[i], 'rb') as img:
                msg_img = MIMEImage(img.read())
                msg_img.add_header('Content-ID', img_cid_names[i])
                MIME_msg_root.attach(msg_img)

        # Send the email
        smtp = smtplib.SMTP()
        smtp.connect(host=host, port=port)
        smtp.sendmail(from_addr, to_addr, MIME_msg_root.as_string())
        logger_.debug('sent email with html/imgs, subject="{}", to_addr="{}".'.format(subject, to_addr))
        smtp.quit()

    @staticmethod
    def send_email_with_text(host='atom.paypalcorp.com', port=25, from_addr=['jyang2@paypal.com', ], to_addr=['jyang2@paypal.com', ],
                             subject="[Spider-Skynet] Default Error Subject", text_body="Default Body"):
        MIME_msg_root = MIMEMultipart('related')
        MIME_msg_root['From'] = ','.join(from_addr)
        MIME_msg_root['To'] = ','.join(to_addr)
        MIME_msg_root['Subject'] = subject
        MIME_msg_root.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an 'alternative' part, so message agents can decide which they want to display.
        msg_alt = MIMEMultipart('alternative')
        # alt plain text
        msg_plain_text = MIMEText(text_body)
        msg_alt.attach(msg_plain_text)

        MIME_msg_root.attach(msg_alt)

        # Send the email
        smtp = smtplib.SMTP()
        smtp.connect(host=host, port=port)
        smtp.sendmail(from_addr, to_addr, MIME_msg_root.as_string())
        logger_.debug('sent email with text, subject="{}", to_addr="{}".'.format(subject, to_addr))
        smtp.quit()