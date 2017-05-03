# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2014 BVTC (VinhDL) (<http://benhvienthucuc.vn>). All Rights Reserved
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
{
    'name' : 'Call Center',
    'version' : '1.0',
    'author' : 'VinhDL',
    'category' : 'Generic Modules/Base',
    'website': 'http://www.benhvienthucuc.vn',
    'depends' : ['base','crm','hr'],
    'description': """
        This module create marketing channel to call center
    """,
    'data': [
        'crm_channel_view.xml',
        'crm_service_type_view.xml',
        'crm_result_type_view.xml',
        'crm_smssettings_view.xml',
        'crm_conduct_view.xml',
        'crm_progress_view.xml',
        'crm_agency_view.xml',
        'crm_callcenter_view.xml',
        'crm_sms_reminder.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

