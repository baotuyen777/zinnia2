# -*- coding: utf-8 -*-
from odoo import http

# class ZinniaTodoApp(http.Controller):
#     @http.route('/zinnia_todo_app/zinnia_todo_app/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zinnia_todo_app/zinnia_todo_app/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zinnia_todo_app.listing', {
#             'root': '/zinnia_todo_app/zinnia_todo_app',
#             'objects': http.request.env['zinnia_todo_app.zinnia_todo_app'].search([]),
#         })

#     @http.route('/zinnia_todo_app/zinnia_todo_app/objects/<model("zinnia_todo_app.zinnia_todo_app"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zinnia_todo_app.object', {
#             'object': obj
#         })