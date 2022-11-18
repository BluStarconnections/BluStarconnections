# -*- coding: utf-8 -*-
{
    'name': "BluStar data import",

    'summary': """
        Custom module to import data from wizard to selected model""",

    'description': """
    BluStar custom data import module
    """,

    'author': "Mediod Consulting",
    'website': "http://www.mediodconsulting.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'CRM',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/get_csv.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'license': 'LGPL-3',
}
