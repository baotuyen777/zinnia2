# -*- coding: utf-8 -*-
{
    'name': "zinnia_CRM",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
       Module CRM
    """,

    'author': "Zinia",
    'website': "http://www.zinnia.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/partner.xml',
        'views/landing_page_source.xml',
        'views/appointment.xml',
        'views/request.xml',
        'views/product.xml',
        'views/product_category.xml',
        'views/machine.xml',
        'views/treatment_card.xml',
        'views/qa.xml',
        'views/sms.xml',
        'views/zopim_setting.xml',
        'views/maketing_campaign.xml',
        'views/call_type.xml',
        'views/call_purpose.xml',
        'views/service_type.xml',
        'views/call_conduct.xml',
        'views/progress.xml',
        'views/maketing_channel.xml',
        'views/agency.xml',
        'views/sms_setting.xml',
        'views/reminder.xml',
        'views/branch.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True
}