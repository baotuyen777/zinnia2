# -*- coding:utf-8 -*-
from odoo import fields, models, api
class Machine(models.Model):
    _name="crm.machine"
    code=fields.Char(string="Code")
    name=fields.Char(string="Name")
    status=fields.Boolean(string="Status")