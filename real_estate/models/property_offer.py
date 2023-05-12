from odoo import models,fields

class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float('Price')
    status = fields.Selection(
        string = "Status",
        selection = [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy = False
    )
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('property', required = True)
