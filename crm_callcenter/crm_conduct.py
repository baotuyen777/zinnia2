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

class crm_conduct(osv.osv):
    _name = 'crm.conduct'
    _rec_name = 'conduct'
    
    _columns = {
        'conduct_code': fields.char('Conduct Code', size=10),
        'conduct': fields.char('Conducted Result', size =50),
    }
    
    _sql_constraints = [
        ('conduct_key', 'UNIQUE(conduct_code)', 'Conduct code has to be unique !')
        ]
crm_conduct()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

