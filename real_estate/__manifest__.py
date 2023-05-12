{
    "name": "real_estate",
    "summary": "Technical Training Module",
    "description": "The real state module is create base on the Odoo 16.0 documentation",
    "author": "Vauxoo",
    "license": "LGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "16.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base"],
    # always loaded
    "data": ["security/ir.model.access.csv", "views/property_views.xml", "views/property_type_views.xml", "data/estate_menus.xml"],
    # only loaded in demonstration mode
    "demo": [],
    "application": True,
}
