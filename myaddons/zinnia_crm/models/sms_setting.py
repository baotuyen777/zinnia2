# -*- coding:utf-8 -*-
from odoo import fields, models, api
class smsSetting(models.Model):
    _name="crm.sms_setting"
    time=fields.Integer(string="Time", default="1")
    unit=fields.Selection([
        ('hour',"Hour"),
        ('minute',"Minute"),
        ('in_service_date',"In Service Date"),
    ],string="Unit")
    content=fields.Text(string='Sms form')
