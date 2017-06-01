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

class crm_channel(osv.osv):
    _name = "crm.channel"
    _description = "Marketing Chanel"
    _rec_name = 'channel_name'
    
    _columns = {
        'shortname': fields.char('Short Name', size=10),
        'channel_name': fields.char('Channel', size =50),
    }
    
    _defaults = {
        'shortname':'',
        'channel_name':''
    }
crm_channel()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

