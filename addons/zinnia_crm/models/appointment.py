# -*- coding:utf-8 -*-
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
    employee_id=fields.Many2one('res.partner',string="Employee")
    call_type_id=fields.Many2one('crm.call_type', string="Call type")
    agency_id=fields.Many2one('crm.agency',string='Agency')
    branch_id = fields.Many2one('crm.branch',string="Branch")
    maketing_channel_id = fields.Many2one('crm.maketing_channel',string="Maketing Channel")
    phone_number=fields.Char(string='Phone number')
    request_id=fields.Many2one('crm.request',string="Request")
    description_detail=fields.Text(string= "Description detail")
    history_id =fields.One2many('crm.history','apm_id',string='History')

    @api.multi
    def create(self, cr, uid, vals, context=None):
        cr.execute("""SELECT COUNT(*) FROM crm_apm WHERE partner_id=""" + str(vals['partner_id']))
        v = cr.fetchone()
        vals['call_count'] = v[0] + 1
        new_id = super(crm_apm, self).create(cr, uid, vals, context=context)
        log_val = {'user': uid, 'apm_id': new_id, 'description': 'Create new',
                   'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.pool.get('crm.log').create(cr, uid, log_val, context=context)
        return new_id
    #
    # def write(self, cr, uid, ids, vals, context=None):
    #     super(crm_apm, self).write(cr, uid, ids, vals, context=context)
    #     log_val = {'user': uid, 'apm_id': ids[0], 'description': 'Cập nhật thông tin',
    #                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    #     self.pool.get('crm.log').create(cr, uid, log_val, context=context)
    #     return True