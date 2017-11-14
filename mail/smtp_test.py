# -*- coding: utf-8 -*-
import smtplib


# msg = MIMEText(content, 'html', 'utf-8')
# msg['From'] = sender
# msg['To'] = ','.join(receivers)
# msg['Subject'] = title

smtp = smtplib.SMTP('atom.paypalcorp.com')
smtp.sendmail('jyang2@paypal.com', 'jyang2@paypal.com', 'HI!')
smtp.quit()