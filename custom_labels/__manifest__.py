# -*- coding: utf-8 -*-
{
    'name': "Laminate Works: Custom Labels",

    'summary': """
    Customize labels to work with Zebra printer connected to IOT box
        """,

    'description': """
        BMU - Task ID: 2375362
        
    """,

    'author': "PS-US Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Custom Development',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'mrp'],

    # always loaded
    'data': [
        'views/view_order_form_inhert.xml',
        'views/mrp_production_form_view_inherit.xml',
        'views/mrp_production_backorder_inherit.xml',
        'views/mrp_zebra_label_inherit.xml',
    ],
    'license': 'OEEL-1',
}