# -*- coding: utf-8 -*-
{
    'name': "Employee Geolocation",
    'description': """
        Get geo location when employee check in or check out their attendance.
        Employee Location while check in and check out
        Track employee
        Employee Tracking 
        Geo Location
        Employee attendance location
    """,

    'author': "Zahid Mehmood",
    'website': "https://mediodconsulting.com/",
    'email': 'zahid_mehmood3@outlook.com',

    'category': 'General',
    'version': '0.1',
    'depends': ['hr', 'hr_attendance'],
    # always loaded
    'data': [
        'views/hr_attendance.xml',
    ],
    "images":['static/description/Banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'price': 17.00,
    'currency': 'EUR',
}
