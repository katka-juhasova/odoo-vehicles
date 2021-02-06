# -*- coding: utf-8 -*-
{
    'name': "Vehicles",

    'summary': """Management of company vehicles""",

    'description': """
        System in Odoo which allows the monitoring of available company vehicles and their assignment to the employees.
    """,

    'author': "K. Juhásová",

    'category': 'Human Resources/Fleet',
    'version': '0.1',
    'sequence': 10,

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'fleet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_views.xml',
        'data/vehicles_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
