# -*- coding: utf-8 -*-
{
    "name": "estate_account",
    "summary": "Account Module to Technical Training Module",
    "description": "The estate account module is create base on the Odoo 16.0 documentation",
    "author": "Vauxoo",
    "license": "LGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['base', 'real_estate', 'account'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [],
    "application": True,
}
