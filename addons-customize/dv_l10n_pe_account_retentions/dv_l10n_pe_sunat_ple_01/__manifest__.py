# -*- coding: utf-8 -*-

{
    'name': """
        PLE 01 - Libro Caja y Bancos Sunat Perú TXT XLS
    """,

    'summary': """
        Permite generar los libros de 1.1 y 1.2 PLE de Sunat Perú. |
        Allows to generate the 1.1 y 1.2 PLE of Sunat Peru.
        Programa de Libros Electrónicos de Perú Sunat.
        Reportes PLE Sunat
        Reportes SUNAT
    """,

    'description': """
        Programa de Libros Electrónicos de Perú Sunat.
        Reportes PLE Sunat
        Reportes SUNAT
        PLE SUNAT
        Libro Caja y Bancos
        Libro Caja
        Libro Bancos
        Libro 1.1
        Libro 1.2
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
            'dv_l10n_pe_sunat_ple',
    ],
    
    'data': [
        'security/ple_report_security.xml',
        'security/ir.model.access.csv',
        'views/account_account_views.xml',
        'views/ple_report_views.xml',
    ],

    'images': ['static/description/banner.gif'],

    'auto_install': False,
    'installable': True,
    'application': True,
}
