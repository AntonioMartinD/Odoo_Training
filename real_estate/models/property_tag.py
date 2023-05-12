from odoo import models,fields

class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Estate Property Tag Model"

    name = fields.Char(required = True)
