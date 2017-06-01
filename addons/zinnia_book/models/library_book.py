# -*- coding: utf-8 -*-
from odoo import models, fields,api, exceptions
from odoo.addons import decimal_precision as dp
from datetime import timedelta as td
from odoo.exceptions import UserError

class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=False)
    @api.multi
    def do_archive(self):
        for record in self:
            record.active = not record.active

class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['base.archive','mail.thread']
    _description = 'Library Book'
    _order = 'date_release desc, name'
    # _rec_name = 'short_name'
    name = fields.Char('Title', required=True,track_visibility=True)
    short_name = fields.Char(
        string='Short Title',
        size=100,  # For Char only
        translate=False,  # also for Text fields
    )
    notes = fields.Text('Internal Notes')
    # state = fields.Selection(
    #     [('draft', 'Not Available'),
    #      ('available', 'Available'),
    #      ('lost', 'Lost')],
    #     'State')
    description = fields.Html(
        string='Description',
        # optional:
        sanitize=True,
        strip_style=False,
        translate=False,
    )
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date', track_visibility=True)
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer(
        string='Number of Pages',
        default=0,
        help='Total book page count',
        groups='base.group_user',
        states={'cancel': [('readonly', True)]},
        copy=True,
        index=False,
        readonly=False,
        required=False,
        company_dependent=False,
    )
    reader_rating = fields.Float(
        'Reader Average Rating',
        (14, 4),  # Optional precision (total, decimals),
    )
    # active = fields.Boolean('Active', default=True)
    author_ids = fields.Many2many('res.partner', string='Authors')
    cost_price=fields.Float('Book cost',dp.get_precision('Book Price'))
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price',
        # optional: currency_field='currency_id',
    )
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    publisher_city = fields.Char(
        'Publisher City',
        related='publisher_id.city')
    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book title must be unique.')
    ]

    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document')
    state = fields.Selection([('draft', 'Unavailable'),
                              ('available', 'Available'),
                              ('borrowed', 'Borrowed'),
                              ('lost', 'Lost')],
                             'State')

    def _track_subtype(self, init_values):
        if 'date_release' in init_values:
            return 'mail.mt_comment'
        return False
    # @api.multi
    # def name_get(self):
    #     result = []
    #
    #     for record in self:
    #         result.append(
    #             (record.id,
    #              u"%s (%s)" % (record.name, record.date_release)
    #              ))
    #     return result

    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise exceptions.ValidationError("date invalid!")



    @api.model
    def _referencable_models(self):
        models = self.env['res.request.link'].search([])

        return [(x.object, x.name) for x in models]

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]

        return (old_state, new_state) in allowed

    # @api.multi
    # def change_state(self, new_state):
    #     for book in self:
    #         if book.is_allowed_transition(book.state,new_state):
    #             book.state = new_state
    #         else:
    #             continue
    @api.onchange('date_updated')
    def onchange_short_name(self):
        print(self.date_updated)
        if self.date_updated  and self.date_updated < fields.Date.today():
            raise exceptions.ValidationError('date_update invalid');
    #
    # @api.multi
    # def save(self, filename):
    #     if '/' in filename or '\\' in filename:
    #         raise UserError('Illegal filename %s' % filename)
    #         path = os.path.join('/opt/exports', filename)
    #         try:
    #             with open(path, 'w') as fobj:
    #                 for record in self:
    #                     fobj.write(record.data)
    #                     fobj.write('\n')
    #         except (IOError, OSError) as exc:
    #             message = 'Unable to save file: %s' % exc
    #             raise UserError(message)
    #
    # @api.model
    # def get_all_library_members(self):
    #     library_member_model = self.env['library.member']
    #     return library_member_model.search([])
    #
    # @api.model
    # def create_partner(self):
    #     today_str = fields.Date.context_today()
    #     val1 = {'name': u'Eric Idle',
    #             'email': u'eric.idle@example.com',
    #             'date': today_str}
    #     val2 = {'name': u'John Cleese',
    #             'email': u'john.cleese@example.com',
    #             'date': today_str}
    #     partner_val = {
    #         'name': u'Flying Circus',
    #         'email': u'm.python@example.com',
    #         'date': today_str,
    #         'is_company': True,
    #         'child_ids': [(0, 0, val1),
    #                       (0, 0, val2),
    #                       ]
    #     }
    #     record = self.env['res.partner'].create(partner_val)
    #
    # @api.model
    # def add_contacts(self, partner, contacts):
    #     partner.ensure_one()
    #
    #     if contacts:
    #         partner.date = fields.Date.context_today()
    #         partner.child_ids |= contacts
    #
    # @api.model
    # def find_partners_and_contacts(self, name):
    #     partner = self.env['res.partner']
    #     domain = ['|',
    #               '&',
    #               ('is_company', '=', True),
    #               ('name', 'like', name),
    #               '&',
    #               ('is_company', '=', False),
    #               ('parent_id.name', 'like', name)
    #               ]
    #     return partner.search(domain)
    #
    # @api.model
    # def partners_with_email(self, partners):
    #     def predicate(partner):
    #         if partner.email:
    #             return True
    #         return False
    #     return partners.filter(predicate)
    #
    # @api.model
    # def get_email_addresses(self, partner):
    #     partner.ensure_one()
    #     return partner.mapped('child_ids.email')
    #
    # @api.model
    # def get_companies(self, partners):
    #     return partners.mapped('parent_id')



