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
    
    def _get_progress_selection(self, cr, uid, context=None):
        v=[]
        status_ids = self.pool.get('crm.progress').search(cr,uid,[],context=context)
        for id in status_ids:
            progres = self.pool.get('crm.progress').browse(cr,uid,id,context=context)
            vs=[]
            vs.append(progres.progress_code)
            vs.append(progres.progress_name)
            v.append(vs)

        return v
        
        
    def _get_agency_selection(self, cr, uid, context=None):
        v=[]
        status_ids = self.pool.get('crm.agency').search(cr,uid,[],context=context)
        for id in status_ids:
            agency = self.pool.get('crm.agency').browse(cr,uid,id,context=context)
            vs=[]
            vs.append(agency.agency_code)
            vs.append(agency.agency_name)
            v.append(vs)

        return v
        
    def _send_sms_reminder(self, cr, uid, context=None):
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

    def on_change_categ_id(self, cr, uid, ids, categ_id, context=None):
        values = {}

        return True
        

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        values = {}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            cr.execute("""SELECT COUNT(*) FROM crm_phonecall WHERE partner_id=""" + str(partner_id))
            v = cr.fetchone()
            values = {
                'partner_phone' : partner.phone,
                'partner_mobile' : partner.mobile,
                'call_count': v[0] + 1,
            }
        return {'value' : values}
    
    _columns = {
        'result_status': fields.selection(_get_status_selection,'Purpose',required=True),
        'channel': fields.selection(_get_channel_selection,'Channels'),
        'service': fields.selection(_get_selection,string='Type',required=True),
        'conduct': fields.selection(_get_conduct_selection,string='Conducted Result'),
        'sms_status': fields.selection([('new','Not Send'),('remind','Reminded'), ('confirm','Confirmed'),('cancel','Cancelled')],'SMS Status',readonly=True),
        'brief': fields.char('Meeting Brief',size=150),
        'staffs': fields.many2many('hr.employee','meeting_staff_relation','id','staff_id','Consultants'),
        'doctors': fields.many2many('hr.employee','meeting_doctor_relation','id','doctor_id','Doctors'),
        'has_meeting': fields.boolean('Show meeting info ?'),
        'progress_status': fields.selection(_get_progress_selection,'Progress State'),
        #'agency': fields.selection(_get_agency_selection,'Agency'),
        'agency': fields.many2one('crm.agency','Agency'),
        'has_agency': fields.boolean('Has Agency ?'),
        'logs': fields.one2many('crm.log','phonecall_id','Modified Logs',ondelete='cascade'),
        'city': fields.related('partner_id','state_id',type ='many2one',relation='res.country.state',string='City',store=True),
        'call_count' : fields.integer('No.Calls'),
        'request_type' : fields.many2one('crm.request.type','Yêu cầu'),
    }
    
    _defaults = {
        'has_meeting': False,
    }
    
    def create(self, cr, uid, vals, context=None):
        cr.execute("""SELECT COUNT(*) FROM crm_phonecall WHERE partner_id=""" + str(vals['partner_id']))
        v = cr.fetchone()
        vals['call_count'] = v[0] + 1
        new_id = super(crm_phonecall, self).create(cr, uid, vals, context=context)
        log_val = {'user': uid,'phonecall_id': new_id,'description': 'Tạo mới ','date':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.pool.get('crm.log').create(cr, uid, log_val, context=context)
        return new_id
    
    def write(self, cr, uid, ids, vals, context=None):
        super(crm_phonecall, self).write(cr, uid,ids, vals, context=context)
        log_val = {'user': uid,'phonecall_id': ids[0],'description': 'Cập nhật thông tin','date':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.pool.get('crm.log').create(cr, uid, log_val, context=context)
        return True
crm_phonecall()

class crm_progress(osv.osv):
    _name = 'crm.progress'
    _description = "Progress State for Appointment"
    _rec_name = 'progress_name'

    _columns = {
        'progress_code': fields.char('Progress Code',size=10,required=True),
        'progress_name': fields.char('Description',size=100,required=True),
    }
crm_progress()

class crm_log(osv.osv):
    _name = 'crm.log'
    _description = "Logged Modified User"

    _columns = {
        'user': fields.many2one('res.users','Modified By'),
        'phonecall_id': fields.many2one('crm.phonecall','Log for Call'),
        'description': fields.char('Description',size=250),
        'date': fields.datetime('Logged Date', readonly=1),
    }
    
    _defaults = {
        'user': lambda self,cr,uid,ctx: uid,
        'date': fields.datetime.now,
    }
    
crm_log()


class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    
    def on_change_birth_date(self, cr, uid, ids, birthdate, context=None):
        result = {}
        if (birthdate):
            d = datetime.strptime(birthdate,'%Y-%m-%d')
            result = {
                'birth_year' : d.strftime('%Y'),
            }
        else:
            result = {
                'birth_year' : '',
            }
                
        return {'value' : result}


    _columns = {
        'partner_gender': fields.selection([('male','Male'),('female','Female'), ('unknown','Unknown')],'Gender'),
        'birth_year': fields.char('Birth Year',size=4),
        'receipt_code': fields.char('Receipt Code',size=200),
        'create_date' : fields.datetime('Create Date', readonly=True),
    }

    _defaults = {
        'partner_gender':'female',
    }

res_partner()

class HistoryLine(osv.Model):
    _inherit = 'sms.smsclient.history'
    
    def _get_sms_customer(self, cr, uid, ids, name, args, context=None):
        res = {}

        for line in self.browse(cr, uid, ids, context=context):
            mobile = line.to.replace('84','0')
            customer_ids = self.pool.get('res.partner').search(cr,uid,[('mobile','ilike', mobile)],context=context)
            customer = self.pool.get('res.partner').browse(cr,uid,customer_ids,context=context)
            if customer and len(customer) > 0 :
                res[line.id] = customer[0].name
                if customer[0].mobile :
                    res[line.id] = res[line.id] + '-' + customer[0].mobile
            else :
                res[line.id] = ''
            
        return res
        
    def _search_sms_customer(self, cr, uid, obj, name, args, context):      
        res = []
        sql1 = '''SELECT a.id FROM sms_smsclient_history AS a where replace(a.to,\'84\',\'0\') in (select mobile from res_partner where lower(name) like \'%'''
        
        if args[0] and args[0][0] == 'customer' :
            sql1 = sql1 +  args[0][2] + '%\')'''
            cr.execute(sql1)
            res = cr.fetchall()
        
        return [('id','in',res)]
    
    _columns = {
        'customer': fields.function(_get_sms_customer,type='char',size=160, fnct_search=_search_sms_customer,string='Customer'),
    }
    
HistoryLine()

class change_trans(osv.osv_memory):
    _name = 'change.trans'
    _description = 'Transaction Changing'
        
    def on_change_new_number(self, cr, uid, ids,new_number, context=None):
        values = {}
        domain =()
        phones =''
        l = list(domain)
        if new_number :
            trans_id = self.pool.get('crm.phonecall').search(cr,uid,[('partner_mobile','=',new_number)])
            for tran in self.pool.get('crm.phonecall').browse(cr,uid,trans_id) :
                values.update({'new_name' : tran.partner_id.name})
                values.update({'partner_id' : tran.partner_id.id})
                if tran.partner_mobile not in phones :
                    phones = phones + tran.partner_mobile + ', '
                
            values.update({'phones' : phones})   
            return {
                'value' : values,
            }
            
        raise osv.except_osv(_('Error'), _('Phone number is required.'))
        
        return True
    
    def change_trans(self, cr, uid, ids,context=None):
        for trans in self.browse(cr,uid,ids):
            trans.current_trans.write({'partner_id' : trans.partner_id.id, 'partner_mobile' : trans.new_number})
            
        return True
    
    _columns = {
        'current_trans' : fields.many2one('crm.phonecall','Current Transaction'),
        'new_number' : fields.char('Số ĐT cần tìm', required=True),
        'new_name' : fields.char('Tên khách hàng'),
        'phones' : fields.char('Các số điện thoại'),
        'partner_id' : fields.many2one('res.partner','Customer'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

