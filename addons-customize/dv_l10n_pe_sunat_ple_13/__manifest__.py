# -*- coding: utf-8 -*-

{
    'name': """
		PLE 13 - Registro de Inventario Permanente Valorizado Sunat Perú TXT XLS
    """,

    'summary': """
        Permite generar el libros de 13.1 PLE de Sunat Perú. |
        Allows to generate the 13.1 PLE of Sunat Peru.
        Programa de Libros Electrónicos de Perú Sunat.
        Reportes PLE Sunat
        Reportes SUNAT
    """,

    'description': """
        Programa de Libros Electrónicos de Perú Sunat.
        Reportes PLE Sunat
        Reportes SUNAT
""",

    'author': 'Develogers',
    'website': 'https://develogers.com',
    'support': 'especialistas@develogers.com',
    'live_test_url': 'https://demoperu.develogers.com',
    'license': 'LGPL-3',

    'price': 149.99,
    'currency': 'EUR',

    'depends': [
            'base',
            'dv_l10n_pe_edi_table',
            'dv_l10n_pe_sunat_catalog',
            'dv_l10n_pe_sunat_ple',
    ],
    
    'data': [
        'security/ple_report_security.xml',
        'security/ir.model.access.csv',
        'views/ple_report_views.xml',
        'views/stock_picking_views.xml',
    ],

    'images': ['static/description/banner.gif'],

    'auto_install': False,
    'installable': True,
    'application': True,
}
