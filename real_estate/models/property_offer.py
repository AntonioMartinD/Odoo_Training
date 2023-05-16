from datetime import timedelta

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status", selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("property", required=True)
    validity = fields.Integer(compute="_compute_validity", inverse="_inverse_validity", string="Validity", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Date Deadline"
    )
    property_type_id = fields.Many2one("property.type", related="property_id.property_type_id", store="True")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = int((record.date_deadline - fields.Date.today()).days)

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            if record.date_deadline:
                record.validity = int((record.date_deadline - fields.Date.today()).days)
            else:
                record.validity = 7

    def _inverse_validity(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def action_accept(self):
        for record in self:
            accepted_offer = record.property_id.offer_ids.filtered(lambda element: element.status == "accepted")
            if accepted_offer:
                raise exceptions.UserError(_("More than one offer can't be accepted"))
            record.status = "accepted"
            record.property_id.state = "acepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.selling_price = 0
            record.property_id.buyer_id = False

    _sql_constraints = [("check_price", "CHECK(price > 0)", "The price must be strictly bigger than 0")]

    @api.model
    def create(self, vals):
        actual_property = self.env["property"].browse(vals["property_id"])
        offers = actual_property.offer_ids
        max_offer = max(offers.mapped("price"), default=0)
        if vals["price"] < max_offer:
            raise ValidationError(_("The offer must be higher than %f", max_offer))
        actual_property.state = "received"
        return super().create(vals)

    def get_accepted_offer(self):
        return self.property_id.offer_ids.filtered(lambda element: element.status == "accepted")
