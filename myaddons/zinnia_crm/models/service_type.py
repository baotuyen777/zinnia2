# -*- coding:utf-8 -*-

from odoo import fields, models, api
class serviceType(models.Model):
    _name = "crm.service_type"
    name=fields.Char(string="Description",required=True)
    code=fields.Char(string="Code",required=True)
