# -*- coding:utf-8 -*-

from odoo import fields, models, api
class Progress(models.Model):
    _name = "crm.progress"
    name=fields.Char(string="Description",required=True)
    code=fields.Char(string="Code",required=True)
