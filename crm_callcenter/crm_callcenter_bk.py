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
from dateutil.relativedelta import relativedelta
from datetime import datetime
import dateutil
import time
import pytz
from openerp import SUPERUSER_ID
from urllib2 import Request, urlopen, URLError, HTTPError
from urllib import urlencode


class crm_phonecall(osv.osv):
    _inherit = 'crm.phonecall'

    def _get_selection(self, cr, uid, context=None):
        v=[]
        service_ids = self.pool.get('crm.service.type').search(cr,uid,[],context=context)
        for id in service_ids:
            service = self.pool.get('crm.service.type').browse(cr,uid,id,context=context)
            vs=[]
            vs.append(service.name)
            vs.append(service.description)
            v.append(vs)

        return v

    def _get_channel_selection(self, cr, uid, context=None):
        v=[]
        service_ids = self.pool.get('crm.channel').search(cr,uid,[],context=context)
        for id in service_ids:
            channel = self.pool.get('crm.channel').browse(cr,uid,id,context=context)
            vs=[]
            vs.append(channel.shortname)
            vs.append(channel.channel_name)
            v.append(vs)

        return v

    def _get_status_selection(self, cr, uid, context=None):
        v=[]
        status_ids = self.pool.get('crm.result.type').search(cr,uid,[],context=context)
        for id in status_ids:
            status = self.pool.get('crm.result.type').browse(cr,uid,id,context=context)
            vs=[]
            vs.append(status.status_code)
            vs.append(status.status)
            v.append(vs)

        return v

    def _get_conduct_selection(self, cr, uid, context=None):
        v=[]
        status_ids = self.pool.get('crm.conduct').search(cr,uid,[],context=context)
        for id in status_ids:
            conduct = self.pool.get('crm.conduct').browse(cr,uid,id,context=context)
            vs=[]
            vs.append(conduct.conduct_code)
            vs.append(conduct.conduct)
            v.append(vs)

        return v

    def _send_sms_reminder(self, cr, uid,current_status ,new_status, context=None):
        if context is None:
            context = {}
        try:
            user_pool = self.pool.get('res.users')
            user = user_pool.browse(cr, SUPERUSER_ID, uid)
            tz = pytz.timezone(user.partner_id.tz) or pytz.utc

            sms_setting_ids = self.pool.get('crm.smssettings').search(cr, uid, [], limit=1, context=context)
            sms_setting = self.pool.get('crm.smssettings').browse(cr, uid, sms_setting_ids, context=context)[0]
            msg = sms_setting.reminder_message

            client_obj = self.pool.get('sms.smsclient')
            gateway_ids = client_obj.search(cr, uid, [], limit=1, context=context)
            gateway = client_obj.browse(cr, uid, gateway_ids, context=context)[0]

            phonecall_obj = self.pool.get('crm.phonecall')
            meeting_obj = self.pool.get('crm.meeting')

            sids = phonecall_obj.search(cr, uid, [
                ('result_status', '=', current_status)
                ], context=context)

            queue_obj = self.pool.get('sms.smsclient.queue')

            meeting_ids = meeting_obj.search(cr, uid,
                                [('date','>=',str(datetime.now()))], context=context)

            for meeting in meeting_obj.browse(cr, uid, meeting_ids, context=context):
                for partner in meeting.partner_ids:
                    if (partner.customer):
                        if gateway:
                            url = gateway.url
                            name = url
                            if gateway.method == 'http':
                                msg = msg.replace('[location]',meeting.location)
                                msg = msg.replace('[content]',meeting.brief)
                                #d = meeting.date.strftime('%H:%M %d/%m/%Y')
                                # get localized dates
                                d = pytz.utc.localize(datetime.strptime(meeting.date, '%Y-%m-%d %H:%M:%S')).astimezone(tz)
                                msg = msg.replace('[date]',d.strftime("%H:%M %d/%m/%y"))
                                prms = {}
                                for p in gateway.property_ids:
                                    if p.type == 'user':
                                        prms[p.name] = p.value.encode('utf-8')
                                    elif p.type == 'password':
                                        prms[p.name] = p.value.encode('utf-8')
                                    elif p.type == 'to':
                                        prms[p.name] = partner.mobile.encode('utf-8')
                                    elif p.type == 'sms':
                                        prms[p.name] = msg.encode('utf-8')
                                    elif p.type == 'extra':
                                        prms[p.name] = p.value.encode('utf-8')

                                params = urlencode(prms)
                                name = url + "?" + params

                                datas = {
                                        'name': name,
                                        'gateway_id': gateway.id,
                                        'state': 'draft',
                                        'mobile': partner.mobile,
                                        'msg': msg.encode('utf-8'),
                                        'validity': 10,
                                        'classes': '1',
                                        'deffered': 0,
                                        'priorirty': '3',
                                        'coding': '1',
                                        'tag': '',
                                        'nostop': True,
                                        }

                                queue_obj.create(cr, uid, datas, context=context)
                                meeting_obj.write(cr, uid, meeting.id, {'sms_status': 'remind'}, context=context)

                #for phone_call in phonecall_obj.browse(cr, uid, sids, context=context):



                #phonecall_obj.write(cr, uid, sids, {'result_status': new_status}, context=context)
                return True
        except Exception, e:
            raise osv.except_osv('Error', e)
            return False
        
    def onchange_result_status(self, cr, uid, ids, result_status, context=None):
        values = {}
        if result_status == 'booking':
            values = {
                      'has_meeting' : True,
                      }
        else:
            values = {
                      'has_meeting' : False,
                      }
        
        return {'value' : values}


    _columns = {
        'result_status': fields.selection(_get_status_selection,'Purpose',required=True),
        'channel': fields.selection(_get_channel_selection,'Channels'),
        'service': fields.selection(_get_selection,string='Type',required=True),
        'conduct': fields.selection(_get_conduct_selection,string='Conducted Result'),
        'sms_status': fields.selection([('new','Not Send'),('remind','Reminded'), ('confirm','Confirmed'),('cancel','Cancelled')],'SMS Status',readonly=True),
        'brief': fields.char('Meeting Brief',size=150),
        'staffs': fields.many2many('hr.employee','meeting_staff_relation','id','staff_id','Doctor/Staff'),
        'has_meeting': fields.boolean('Show meeting info ?'),
    }
    
    _defaults = {
        'has_meeting': False,
    }
crm_phonecall()

class crm_meeting(osv.osv):
    _inherit = 'crm.meeting'

    _columns = {
        'sms_status': fields.selection([('new','Not Send'),('remind','Reminded'), ('confirm','Confirmed'),('cancel','Cancelled')],'SMS Status',readonly=True),
        'brief': fields.char('Meeting Brief',size=150),
        'staffs': fields.many2many('hr.employee','meeting_staff_relation','id','staff_id','Doctor/Staff'),
    }

    _defaults = {
        'sms_status':'new',
    }
crm_meeting()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

