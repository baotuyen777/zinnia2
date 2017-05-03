# -*- codeing:utf-8 -*-
from odoo import models,fields,api

class Appointment(models.Model):
    _name='crm.apm'
    
    description=fields.Char(string='Description',required=True)
    phone=fields.Char(string="Phone", required=True)
    date=fields.Date(string="Date")
    duration=fields.Char(string="Duration", default="01:00")
    purpose_id=fields.Many2one('crm.call_purpose', string="Purpose")
    service_type_id=fields.Many2one('crm.service_type',string="Service type")
    contact_id=fields.Many2one('res.partner', string='Contact')
    conduct_id=fields.Many2one('crm.call_conduct',string="Conduct")
    product_id=fields.Many2one('crm.product',string ='Product service')
    employee=fields.Char()
    call_type=fields.Many2one('crm.call_type', string="Call type")
    agency_id=fields.Many2one('crm.agency',string='Agency')
    branch = fields.Selection([
        ('thucuc', 'Thu Cuc Hospital'),
        ('228tayson', '228 Tay son'),
        ('57nguyenkhachieu', '57 Nguyen Khac Hieu'),
    ])
    maketing_channel_id = fields.Many2one('crm.maketing_channel',string="Maketing Channel")
    phone_number=fields.Char(string='Phone number')
    request_id=fields.Many2one('crm.request',string="Request")
    description_detail=fields.Text(string= "Description detail")
    history_id =fields.One2many('crm.history','apm_id',string='History')