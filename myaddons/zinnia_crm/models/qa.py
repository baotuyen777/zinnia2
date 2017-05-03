# -*- coding:utf-8 -*-

from odoo import fields, models, api
class qa(models.Model):
    _name = 'crm.qa'
    name=fields.Char(string='Name')
    is_use=fields.Boolean(string="Use")
    create_by=fields.Many2one('res.partner', string="Create by")
    type=fields.Char(string="Type")
    key_word=fields.Char(string="Key word")
    date_create=fields.Datetime(string="Date create")
    field=fields.Char()
    answer=fields.Text(string="Answer")
    