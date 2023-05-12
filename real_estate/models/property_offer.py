from datetime import timedelta
from odoo import models,fields,api

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
    validity = fields.Integer(compute = '_compute_validity', inverse = '_inverse_validity' , string = 'Validity', default = 7)
    date_deadline = fields.Date(compute =  '_compute_date_deadline', inverse = '_inverse_date_deadline' ,string = "Date Deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = int((record.date_deadline - fields.Date.today()).days)

    @api.depends('date_deadline')
    def _compute_validity(self):
        for record in self:
            if (record.date_deadline):
                record.validity = int((record.date_deadline - fields.Date.today()).days)
            else:
                record.validity = 7
    
    def _inverse_validity(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days = record.validity)

