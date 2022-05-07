# -*- coding: utf-8 -*-

{
	'name': """
		PLE 14 - Registro de Ventas Sunat Perú TXT XLS
    """,

    'summary': """
        Permite generar los libros de 14.1 y 14.2 PLE de Sunat Perú. |
        Allows to generate the 14.1 y 14.2 PLE of Sunat Peru.
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
		'dv_l10n_pe_sunat_ple',
	],
 
	'data': [
     	'security/ple_security.xml',
		'security/ir.model.access.csv',
        'views/account_move_views.xml',
		'views/ple_report_views.xml',
	],
	
	'images': ['static/description/banner.gif'],
 
	'auto_install': False,
	'installable': True,
	'application': True,
}