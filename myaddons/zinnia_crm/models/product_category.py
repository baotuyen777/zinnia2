# -*- coding:utf-8 -*-
from odoo import fields,models,api
class product_category(models.Model):
    _name = 'crm.product_category'
    name=fields.Char(string="Name", required=True)
    category=fields.Many2one('crm.product_category', string="Category")
