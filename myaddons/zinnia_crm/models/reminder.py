# -*- coding:utf-8 -*-
from odoo import fields, models, api
class Reminder(models.Model):
    _name="crm.reminder"
    time=fields.Char(string="Time reminder", default="07:00")
    content=fields.Text(string='Sms form')
