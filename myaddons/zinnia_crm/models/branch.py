# -*- coding:utf-8 -*-

from odoo import fields, models, api
class Branch(models.Model):
    _name = "crm.branch"
    name=fields.Char(string="Description",required=True)
    code=fields.Char(string="Code",required=True)
