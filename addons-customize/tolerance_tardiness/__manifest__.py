{
    'name': 'Tolerance tardiness',
    'version': '14.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'This module manages tardiness',
    'category': 'Payroll',
    "license": "Other proprietary",
    'depends': ['hr_attendance', 'hr_work_entry'],
    'data': [
        'views/hr_views.xml',
        'views/resource_calendar_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}
