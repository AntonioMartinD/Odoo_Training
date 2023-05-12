from odoo import models,fields

class PropertyType(models.Model):
    _name = "property.type"
    _description = "Estate Property Type Model"

    name = fields.Char(required = True)
