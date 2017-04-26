# -*- coding: utf-8 -*-
from odoo import fields, models, api
class maketingCampaign(models.Model):
    _name='crm.maketing_campaign'
    code=fields.Char(string="Campaign Code",required=True)
    name= fields.Char(string='Campaign Name')

    ld_source = fields.Many2one('crm.lps', string="LD Source")
    total=fields.Integer(string="Total Partner")

