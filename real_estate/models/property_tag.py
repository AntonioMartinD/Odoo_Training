from odoo import models,fields

class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(required = True)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique')
    ]
