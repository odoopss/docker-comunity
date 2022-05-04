{
    'name': """
        Facturas con Impuesto de Retención Perú
    """,

    'summary': """
        Adds withholding tax move in customer and supplier invoices. |
        Agrega impuesto de retención en facturas de clientes y proveedores.
    """,

    'description': """
        
    """,

	'author': 'Develogers',
    'website': 'https://develogers.com',
    'support': 'especialistas@develogers.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'category': 'Accounting',
    'version': '14.0',

    'price': 49.99,
    'currency': 'EUR',

    'depends': [
        'base',
        'account',
    ],

    'data': [
        'data/withholding.tax.table.csv',
        'views/account_move_views.xml',
        'views/withholding_tax_table_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu_item_views.xml',
        'security/ir.model.access.csv',
    ],

    'images': ['static/description/banner.gif'],

    'application': True,
    'installable': True,
    'auto_install': False,
}
