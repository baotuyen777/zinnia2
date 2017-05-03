# -*- coding: utf-8 -*-
from odoo import fields, models,api

class treatmentCard(models.Model):
    _name = 'treatment.card'
    name=fields.Char(string="Code card",required=True)
    partner_id=fields.Many2one('res.partner', string="Customer",required=True)
    value=fields.Char(string='Value',default=0,readonly=True)
    residual_value=fields.Integer(string='Residua value')
    use_value=fields.Integer(string='Use value')
    amount_debit=fields.Integer(string="Amount debit")
    order_id=fields.Char()
    type=fields.Selection([
        ('cnc','CNC card'),
        ('skincare','SkinCare card'),
        ('pcell',"P'Cell card"),

    ])
    treatment_id=fields.Char(requied=True)
    start_date=fields.Date(string="Start date",required=True)
    end_date=fields.Date(string="Deadline")
    time=fields.Integer(string="Time")
    residual_time=fields.Integer(string="Residual time")
    sale_off=fields.Float(string='Sale off')
    card_form=fields.Selection([
        ('diplomatic','Diplomantic card'),
        ('residual','Residual up card'),
        ('maketing','Maketing card'),
    ])
    note=fields.Text(string="infomation")
    state=fields.Selection([
        ('draft',"Draft"),
        ('gave',"Gave out to customer"),
        ('returned',"Returned"),
    ])
    @api.multi
    def action_draft(self):
        self.state='draft'
    @api.multi
    def action_gave(self):
        self.state='gave'
    @api.multi
    def action_returned(self):
        self.state='returned'
