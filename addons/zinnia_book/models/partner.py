from odoo import models,fields,api
class ResPartner(models.Model):
    _inherit = 'res.partner'
    authored_book_ids = fields.Many2many(
        'library.book',
        string='Authored Books',
        # relation='library_book_res_partner_rel'
    )
    count_books = fields.Integer(
        'Number of Authored Books',
        compute='_compute_count_books'
    )

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)

    @api.model
    def partners_by_country(self):
        sql = ('SELECT country_id, array_agg(id) '
               'FROM res_partner '
               'WHERE active=true AND country_id IS NOT NULL '
               'GROUP BY country_id')
        self.env.cr.execute(sql)
        country_model = self.env['res.country']
        result = {}
        for country_id, partner_ids in self.env.cr.fetchall():
            country = country_model.browse(country_id)
        partners = self.search(
            [('id', 'in', tuple(partner_ids))]
        )
        result[country] = partners
        return result
