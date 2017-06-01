# -*- coding:utf-8 -*-
from odoo import fields, models,api

class History(models.Model):
    _name = 'crm.history'

    created_by=fields.Many2one('res.users',string="Employee",default=lambda self: self.env.user.id )
    date_create=fields.Datetime(readonly=True, default = fields.datetime.now(), required=True)
    content = fields.Char(string="Content",autofocus=True)
    apm_id = fields.Many2one('crm.apm')

    # _default = {
    #     'date_create': fields.datetime.now
    # }
    # @api.multi
    # def write(self, vals):
    #     vals={'date_create':fields.datetime.now()}
    #     super(History, self).write(vals)
    #     return True
