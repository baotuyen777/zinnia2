# -*- coding: utf-8 -*-
from odoo import http

# class ZinniaCrm(http.Controller):
#     @http.route('/zinnia__crm/zinnia__crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zinnia__crm/zinnia__crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zinnia__crm.listing', {
#             'root': '/zinnia__crm/zinnia__crm',
#             'objects': http.request.env['zinnia__crm.zinnia__crm'].search([]),
#         })

#     @http.route('/zinnia__crm/zinnia__crm/objects/<model("zinnia__crm.zinnia__crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zinnia__crm.object', {
#             'object': obj
#         })