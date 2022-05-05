{
    'name': """
        Gestión de Catálogos SUNAT Perú
    """,

	'summary': """
		Catalogo SUNAT""",

	'description': """
		Catalogo SUNAT
	""",

    'author': 'Develogers',
    'website': 'https://develogers.com',
    'support': 'especialistas@develogers.com',
    'live_test_url': 'https://demoperu.develogers.com',
    'license': 'LGPL-3',

    'price': 44.99,
    'currency': 'EUR',
    
    'category': 'Invoice',
    'version': '1.0',

    'depends': [
		'base',
		'l10n_pe',
	],
    'data': [
		'security/pe_sunat_data_security.xml',
		'security/ir.model.access.csv',
		'data/pe_sunat_data.xml',
		'data/pe.sunat.data.csv',
        'views/pe_sunat_data_view.xml',
	],
    
    'images': ['static/description/banner.gif'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
