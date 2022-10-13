# -*- coding: utf-8 -*-
{
    'name': "BluStar Email Templates",

    'summary': """
        custom email templates""",

    'description': """
        Custom email template for BluStart connections
    """,

    'author': "Mediod Consulting",
    'website': "http://www.mediodconsulting.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'crm',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['mail', 'crm'],

    # always loaded
    'data': [
        'data/appointment_email_external.xml',
        'data/internal_email_template.xml',
    ],
    'installable': True,
    'application': True,
}
