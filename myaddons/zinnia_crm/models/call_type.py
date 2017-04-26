# -*- coding:utf-8 -*-

from odoo import fields, models, api
class callType(models.Model):
    _name = "crm.call_type"
    name=fields.Char(string="Name",required=True)
    self_team_id=fields.Char()
