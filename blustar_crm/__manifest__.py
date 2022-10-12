# -*- coding: utf-8 -*-
{
    'name': "Blustar CRM",

    'summary': """
        """,

    'description': """

    """,

    'author': "Ammar",
    'website': "",
    'category': 'CRM',
    'version': '0.1',

    'depends': ['base', 'crm'],

    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
    ],
    'assets': {
        'web.report_assets_common': [
        ],
        'web.assets_qweb': [
            # 'custom_pos/static/src/xml/**/*',
        ],

    },
    'demo': [
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
