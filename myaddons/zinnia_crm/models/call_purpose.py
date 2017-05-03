# -*- coding:utf-8 -*-

from odoo import fields, models, api
class callPurpose(models.Model):
    _name = "crm.call_purpose"
    name=fields.Char(string="Description",required=True)
    code=fields.Char(string="Code",required=True)
