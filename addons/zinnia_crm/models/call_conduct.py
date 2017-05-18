# -*- coding:utf-8 -*-

from odoo import fields, models, api
class callConduct(models.Model):
    _name = "crm.call_conduct"
    name=fields.Char(string="Description",required=True)
    code=fields.Char(string="Code")
    remkt=fields.Boolean(string="Use Re-Mkt")