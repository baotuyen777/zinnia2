# -*- coding:utf-8 -*-
from odoo import fields, models, api
class Agency(models.Model):
    _name="crm.agency"
    name=fields.Char(string="Name", required=True)
    code=fields.Char(string="Code",required=True)
    birth=fields.Date(string="Birhday")
    address=fields.Char(string='Address')
    phone = fields.Char(string='Phone')
    email=fields.Char(string='Email')
    bank_account_number=fields.Char(string='Bank Account Number')
    bank_name=fields.Char(string='Bank Name')
