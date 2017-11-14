# -*- coding: utf-8 -*-
from envelopes import Envelope

envelope = Envelope(
    from_addr=(u'jyang2@paypal.com', u'From Example'),
    to_addr=(u'jyang2@paypal.com', u'To Example'),
    subject=u'Envelopes demo',
    text_body=u"I'm a helicopter!"
)
envelope.add_attachment('/Users/jyang2/Downloads/GIS as Statistics SDK Service.png')

# Send the envelope using an ad-hoc connection...
envelope.send(host='atom.paypalcorp.com', port=25, login=None, password=None, tls=True)

