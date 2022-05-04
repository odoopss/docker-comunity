# -*- coding: utf-8 -*-

{
	'name': """
 		PLE 05 - Libro Diario Sunat Perú TXT XLS
    """,

    'summary': """
        Permite generar los libros de 5.1 5.2 5.3 y 5.4. PLE de Sunat Perú. |
        Allows to generate the 5.1 5.2 5.3 and 5.4. PLE of Sunat Peru.
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
		'views/ple_report_views.xml',
	],
 
	'images': ['static/description/banner.gif'],
 
	'auto_install': False,
	'installable': True,
	'application': True,
}
