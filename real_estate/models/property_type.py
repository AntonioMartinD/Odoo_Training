from odoo import models,fields

class PropertyType(models.Model):
    _name = "property.type"
    _description = "Estate Property Type Model"

    name = fields.Char(required = True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique')
    ]
