# -*- coding:utf-8 -*-

from odoo import fields, models, api
class maketingChannel(models.Model):
    _name = "crm.maketing_channel"
    name=fields.Char(string="Description",required=True)
    code=fields.Char(string="Code",required=True)
