# -*- coding: utf-8 -*-
import yagmail

# yagmail.register('jyang2@paypal.com', '') # Run this alone to store .yagmail password in keyring

yag = yagmail.SMTP(host='atom.paypalcorp.com', port='25')
contents = ['This is the body, and here is just text http://somedomain/image.png']
yag.send(to='jyang2@paypal.com', subject='subject', contents=contents)