# -*- coding: utf-8 -*-
{
    'name': 'Automatic Backup (Dropbox, Google Drive, Amazon S3, SFTP)',
    'version': '1.6.0',
    'summary': 'Automatic Backup',
    'author': 'Grzegorz Krukar (grzegorzgk1@gmail.com)',
    'description': """
    Automatic Backup
    """,
    'data': [
        'data/data.xml',
        'views/automatic_backup.xml',
        'security/security.xml'
    ],
    'depends': [
        'mail',
    ],
    'assets': {
        "web.assets_backend": [
            "/automatic_backup/static/src/js/automatic_backup.js"]
    },
    'installable': True,
    'application': True,
    'price': 30.00,
    'currency': 'EUR',
}
