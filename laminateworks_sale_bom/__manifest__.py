# -*- coding: utf-8 -*-
{
    'name': 'Laminate Works: Sales + BoM Dev',
    'summary': 'Create a bill of materials from the sales order',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '1.1',
    'author': 'Odoo Inc',
    'description': """
        Task ID: 2361742
    """,
    'category': 'Custom Development',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom_views.xml',
        'views/sale_views.xml',
        'views/product_family_views.xml',
        'views/product_template_views.xml',
        'data/cron.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}