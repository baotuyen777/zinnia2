# -*- coding:utf-8 -*-
from odoo import models, fields,api

class lps(models.Model):
    _name = 'crm.lps'
    code=fields.Char(string='Code',required=True)
    name=fields.Char(string="Landing page source")
    total = fields.Integer(string='Total Partner')
    # partner_ids = fields.Many2many('res.partner', string="Partner list")