from odoo import fields, models


class PropertyTag(models.Model):
    _name = "property.tag"
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [("check_name", "UNIQUE(name)", "The name must be unique")]
