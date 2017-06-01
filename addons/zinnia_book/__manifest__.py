# -*- coding: utf-8 -*-
{
    'name': "zinnia_Book",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
       Module CRM
    """,

    'author': "Tuyenbv",
    'website': "http://www.zinnia.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','decimal_precision','mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/templates.xml',
        'views/views.xml',
        'views/book.xml',
        'views/partner.xml',
        'views/book_category.xml',
        'views/library_member.xml',
        'views/library_loan_wizard.xml',
        'views/partner2.xml',
        'views/sms.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True
}