from datetime import timedelta

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = "property"
    _description = "Estate Property Model"
    _order = "id desc"

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From", default=lambda self: fields.Datetime.now() + timedelta(days=90), copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("weast", "Weast")],
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("acepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        copy=False,
        default="new",
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("property.type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)

    buyer_id = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("property.tag")
    offer_ids = fields.One2many("property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                prices = record.offer_ids.mapped("price")
                record.best_price = max(prices)
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError(_("Sold property cannot be canceled"))
            if record.state == "canceled":
                raise exceptions.UserError(_("Property is already canceled"))
            record.state = "canceled"
        return True

    def action_sold(self):
        for record in self:
            has_accepted_offer = any(offer.status == "accepted" for offer in record.offer_ids)
            if not has_accepted_offer:
                raise exceptions.UserError(_("Property cannot be sold without any accepted offers"))
            if record.state == "canceled":
                raise exceptions.UserError(_("Canceled property cannot be sold"))
            if record.state == "sold":
                raise exceptions.UserError(_("Property is already sold"))
            record.state = "sold"
        return True

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly bigger than 0"),
        ("check_selling_price", "CHECK(selling_price > -1)", "The selling price must be strictly bigger than 0"),
    ]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price > 0:
                limit_price = record.expected_price * 0.9
                compared_prices = float_compare(record.selling_price, limit_price, precision_digits=2)
                if compared_prices == -1:
                    raise ValidationError(_("The selling price cannot be lower than 90'%' of the expected price"))

    @api.ondelete(at_uninstall=False)
    def unlink(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise exceptions.UserError(_("Only new and canceled properties can be deleted"))
