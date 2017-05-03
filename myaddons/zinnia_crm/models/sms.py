# -*- coding: utf-8 -*-
from odoo import fields, models, api
class Sms(models.Model):
    _name='crm.sms'
    date= fields.Date(string='Date')
    partner_id=fields.Many2one('res.partner', string="Customer")
    phone=fields.Char(string="Mobile No")
    content= fields.Text(string='SMS')
    user_name=fields.Many2one('res.partner', string ="User name")
    description=fields.Char(string='Description ')
    gateway_id=fields.Many2one('crm.gateway',string="SMS Gateway")