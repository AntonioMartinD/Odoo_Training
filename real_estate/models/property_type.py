from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "property.type"
    _description = "Estate Property Type Model"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1, help="Used to order what kind of property is the best seller.")
    offer_ids = fields.One2many("property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [("check_name", "UNIQUE(name)", "The name must be unique")]

    def get_offers(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Properties Offer",
            "view_mode": "tree",
            "res_model": "property.offer",
            "domain": [("property_type_id", "=", self.id)],
            "context": "{'create': False}",
        }
