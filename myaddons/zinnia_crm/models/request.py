# -*- coding: utf-8 -*-
from odoo import fields, models,api

class request(models.Model):
    _name = 'crm.request'
    code=fields.Char(string='Code')
    name=fields.Char(string='Name')