# -*- coding:utf-8 -*-
from odoo import fields, models,api

class History(models.Model):
    _name = 'crm.history'

    created_by=fields.Many2one('res.partner',default= lambda self: self.env.uid)
    date_create=fields.Datetime(readonly=True, default = fields.datetime.now(), required=True)
    content = fields.Char(string="Content",  required=True,autofocus=True)
    apm_id = fields.Many2one('crm.apm')

    # _default = {
    #     'date_create': fields.datetime.now
    # }
    @api.model
    def create(self, values):
        a = super(History, self).create(values)
        user = self.env['res.partner'].search([('id', '=', values['created_by'])])
        # print lambda self: self.env.user
        print values



        return a