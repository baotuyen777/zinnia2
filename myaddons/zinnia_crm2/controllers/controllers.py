# -*- coding: utf-8 -*-
from odoo import http

# class ZinniaCrm2(http.Controller):
#     @http.route('/zinnia_crm2/zinnia_crm2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zinnia_crm2/zinnia_crm2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zinnia_crm2.listing', {
#             'root': '/zinnia_crm2/zinnia_crm2',
#             'objects': http.request.env['zinnia_crm2.zinnia_crm2'].search([]),
#         })

#     @http.route('/zinnia_crm2/zinnia_crm2/objects/<model("zinnia_crm2.zinnia_crm2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zinnia_crm2.object', {
#             'object': obj
#         })