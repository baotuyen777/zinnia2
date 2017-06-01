# -*- coding: utf-8 -*-
from odoo import models, fields,api, exceptions
import smtplib
class LibrarySMS(models.Model):
    _name = 'library.sms'
    # _rec_name = 'short_name'
    name = fields.Char('Title', required=True)
    content = fields.Char('content')

    @api.one
    def send_sms(self):
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()

        # Next, log in to the server
        smtpObj.login("test123.qsoft@gmail.com", "!@#$%$#@!")

        # Send the mail
        msg = "Hello!" # The /n separates the message from the headers
        smtpObj.sendmail("test123.qsoft@gmail.com", "baotuyen555@gmail.com", msg)
        return True




