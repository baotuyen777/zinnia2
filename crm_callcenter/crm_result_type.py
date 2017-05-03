# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2014 BVTC (<http://benhvienthucuc.vn>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
from openerp import pooler

class crm_result_type(osv.osv):
    _name = 'crm.result.type'
    _rec_name = 'status'
    
    _columns = {
        'status_code': fields.char('Purpose Code', size=10),
        'status': fields.char('Purpose Description', size =50),
    }
    
    _defaults = {
        'status_code':'call',
        'status':'Call In'
    }
    
    _sql_constraints = [
        ('status_key', 'UNIQUE(status_code)', 'Status code has to be unique !')
        ]
crm_result_type()

class crm_request_type(osv.osv):
    _name = 'crm.request.type'
    
    _columns = {
        'code': fields.char('Mã', size=10),
        'name': fields.char('Name', size =250),
    }
    
    _defaults = {

    }
    
    _sql_constraints = [
        ('code_key', 'UNIQUE(code)', 'Mã đã tồn tại. Hãy chọn mã khác !')
        ]
crm_request_type()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

