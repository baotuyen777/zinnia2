# -*- coding: utf-8 -*-
from odoo import fields, models, api
class zopimSetting(models.Model):
    _name='crm.zopim_setting'
    name=fields.Char(string="Name")
    client_id= fields.Char(string='Client ID')
    authentication_type=fields.Selection([
        ('basic_authentication','Basic Authentication'),
        ('oauth2','OAuth 2.0')
    ])
    url=fields.Char(string='URL path')
    client_secret=fields.Char(string="Client Secret")

