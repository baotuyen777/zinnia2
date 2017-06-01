# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)

    lps_id = fields.Many2one('crm.lps',
        string="Landing Page Source")

    birth = fields.Date(string="Birthday")
    # landing_page_source=fields.Char()
    contact_type=fields.Selection([
        ('normal','Normal'),
        ('zopim', 'Zompim Contact'),
        ('tawkto', 'Tawk.to'),
        ('getrespond', 'GetRespond'),
        ('mailchimp', 'Mailchimp'),
        ('orther', 'Other'),
    ])
    reference=fields.Char()

    member_level=fields.Selection([
        ('gold','Gold card'),
        ('silver', 'Silver card'),
        ('red', 'Red card'),
        ('diplomantic', 'Diplomantic card'),
    ])
    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('unknow','Unknow')
    ])
    branch=fields.Selection([
        ('thucuc','Thu Cuc Hospital'),
        ('228tayson','228 Tay son'),
        ('57nguyenkhachieu','57 Nguyen Khac Hieu'),
    ])
    maketing_channel=fields.Selection([
        ('email','Email'),
        ('sms','Sms'),
        ('facebook','Facebook')
    ])

    # @api.multi
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         result.append(
    #             (record.id,
    #              u"%s (%s)" % (record.name, '11111')
    #              ))
    #     return result

    @api.multi
    def appointment_form(self):
        return {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'crm.apm',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'readonly': True,
            'context': {
                'default_contact_id': self.id,
            }
            # 'res_id': self.id,
        }
    def appointment_list(self):
        return {
            'name':_('List'),
            'view_type':'tree',
            'view_mode':'tree',
            'res_model':'crm.apm',
            'view_id':False,
            'type':'ir.actions.act_window',
            'target':'new',
            'readonly':True,
            'domain': [('contact_id','=',self.id)]
        }
