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
from openerp import tools
from openerp.tools.translate import _
import string
import re
import math
import logging

_logger = logging.getLogger(__name__)

def khongdau(utf8_str):
    VI_STR = 'ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸĐ'
    VI_STR = [ch.encode('utf8') for ch in unicode(VI_STR, 'utf8')]
    EN_STR = 'aaaaaaaaaaaaaaaaaoooooooooooooooooeeeeeeeeeeeuuuuuuuuuuuiiiiiyyyyydAAAAAAAAAAAAAAAAAOOOOOOOOOOOOOOOOOEEEEEEEEEEEUUUUUUUUUUUIIIIIYYYYYD'
    re = ''
    ustr=utf8_str.encode("utf-8")
    ustr = [ch.encode('utf8') for ch in unicode(ustr, 'utf8')]
    #raise orm.except_orm(_('Error'),ustr)
    #ustr = [ch.encode('utf8') for ch in unicode(ustr, 'utf8')]
    for s in ustr :
        try :
            ind = VI_STR.index(s)
            re = re + EN_STR[ind]
        except Exception, e:
            re= re + s
            continue
            
    return re

class crm_smssettings(osv.osv):
    _name = "crm.smssettings"
    _description = "SMS Reminder Settings"
    
    def send_sms_reminder(self,cr,uid, ids, context=None):
        if context is None:
            context = {}
        try:
            user_pool = self.pool.get('res.users')
            user = user_pool.browse(cr, SUPERUSER_ID, uid)
            tz = pytz.timezone(user.partner_id.tz) or pytz.utc

            sms_setting_ids = self.pool.get('crm.smssettings').search(cr, uid, [], limit=1, context=context)
            sms_setting = self.pool.get('crm.smssettings').browse(cr, uid, sms_setting_ids, context=context)[0]
            
            client_obj = self.pool.get('sms.smsclient')
            gateway_ids = client_obj.search(cr, uid, [], limit=1, context=context)
            gateway = client_obj.browse(cr, uid, gateway_ids, context=context)[0]
            
            strtz = datetime.now(tz).strftime('%z')
            tzoff = strtz[0:3] + ':' + strtz[3:]
            
            if sms_setting.time_unit != 'inday' :
                btime = '-24:00:00'
                if sms_setting.time_unit == 'mi' :
                    btime = '-00:' + str(sms_setting.reminder_before) + ':' + '00'
                elif sms_setting.time_unit == 'hr' :
                    btime = '-' + str(sms_setting.reminder_before) + ':00:00'
                elif sms_setting.time_unit == 'day' :
                    btime = '-' + str(sms_setting.reminder_before*24) + ':00:00'
                
                sql = """select id from crm_phonecall where (now() <= date + \'""" + tzoff + """\') and (now() >= date + \' """ + tzoff + """\' + \'""" + btime + """\') and (sms_status is null) and result_status IN (\'DLTV\',\'DLSEOTV\',\'TH\',\'DLSEOTH\',\'BHDV\')"""
            else :
                btime = '07:00'
                hr = math.floor(sms_setting.remider_time)
                mi = math.ceil((sms_setting.remider_time - hr)*60)
                
                if mi < 10 :
                    btime= str(int(hr)) + ':0' + str(int(mi))
                else :
                    btime= str(int(hr)) + ':' + str(int(mi))
                
                sql = """select id from crm_phonecall where (now() <= date + \'""" + tzoff + """\') and (now() >= date(date + \' """ + tzoff + """\')::timestamp + time \'""" + btime + """\') and (sms_status is null) and result_status IN (\'DLTV\',\'DLSEOTV\',\'TH\',\'DLSEOTH\',\'BHDV\')"""
            
            cr.execute(sql)
            sids = cr.fetchall()

            phonecall_obj = self.pool.get('crm.phonecall')
            
            queue_obj = self.pool.get('sms.smsclient.queue')
            
            for cid in sids:
                msg = khongdau(sms_setting.reminder_message)
                booking = phonecall_obj.browse(cr,uid,cid[0],context=context)
                try :
                    if gateway:
                        url = gateway.url
                        name = url
                        if gateway.method == 'http':
                            pname =''
                            if booking.product :
                                pname = khongdau(booking.product.name_template)
                                
                            msg = msg.replace('[service]',pname)
                            
                            if booking.progress_status :
                                msg = msg.replace('[location]',booking.progress_status)
                            else :
                                msg = msg.replace('[location]','')
                                    
                            d = pytz.utc.localize(datetime.strptime(booking.date, '%Y-%m-%d %H:%M:%S')).astimezone(tz)
                            msg = msg.replace('[date]',d.strftime("%d/%m/%Y"))
                            msg = msg.replace('[time]',d.strftime("%H:%M"))
                            
                            phone = booking.partner_mobile.replace('+','')
                            
                            if phone[0] == '0' :
                                phone = phone[1:]
                            
                            if phone[0:2] != '84' :
                                phone = '84' + phone
                                
                            prms = {}
                            for p in gateway.property_ids:
                                if p.type == 'user':
                                    prms[p.name] = p.value.encode('utf-8')
                                elif p.type == 'password':
                                    prms[p.name] = p.value.encode('utf-8')
                                elif p.type == 'to':
                                    prms[p.name] = phone.encode('utf-8')
                                elif p.type == 'sms':
                                    prms[p.name] = msg
                                elif p.type == 'extra':
                                    prms[p.name] = p.value.encode('utf-8')
        
                            params = urlencode(prms)
                            name = url + "?" + params
                            
                            datas = {
                                'name': name,
                                'gateway_id': gateway.id,
                                'state': 'draft',
                                'mobile': phone,
                                'msg': msg,
                                'validity': 10,
                                'classes': '1',
                                'deffered': 0,
                                'priorirty': '3',
                                'coding': '2',
                                'tag': '',
                                'nostop': True,
                            }
        
                            queue_obj.create(cr, uid, datas, context=context)
                            booking.write({'sms_status': 'remind'})
                except Exception, e1 :
                    _logger.info(str(e1))
            return True
        except Exception, e:
            raise osv.except_osv('Error', str(e))
            return False
    
    _columns = {
        'reminder_before': fields.integer('Reminder Before'),
        'time_unit': fields.selection([('mi','Minute(s)'), ('hr','Hour(s)'),('day','Day(s)'),('inday','In Service Date')],'Time Unit'),
        'remider_time' : fields.float('Reminder Time'),
        'reminder_message': fields.text('Message Template'),
    }
    
    _defaults = {
        'reminder_before': 1,
        'time_unit' : 'hr',
    }
crm_smssettings()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: