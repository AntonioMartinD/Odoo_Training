from datetime import timedelta
from odoo import fields,models,api,exceptions
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

class Property(models.Model):
    _name = "property"
    _description = "Estate Property Model"
    
    name = fields.Char("Title",required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From",default=lambda self: fields.Datetime.now() + timedelta(days=90),copy = False)
    expected_price = fields.Float("Expected Price",required=True)
    selling_price = fields.Float ("Selling Price",readonly=True)
    bedrooms = fields.Integer("Bedrooms", default = 2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean ("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north','North'),
                     ('south','South'),
                     ('east','East'), 
                     ('weast','Weast')]
    )
    state = fields.Selection(
        string = 'Status',
        selection = [('new','New'), 
                     ('received','Offer Received'), 
                     ('acepted','Offer Accepted'), 
                     ('sold','Sold'), 
                     ('canceled','Canceled')],
        copy = False,
        default = 'new'
    )
    active = fields.Boolean('Active',default=False)
    property_type_id = fields.Many2one('property.type')
    salesperson_id = fields.Many2one('res.users', 
                                     string="Salesperson", 
                                     index=True, 
                                     default=lambda self: self.env.user)
    
    buyer_id = fields.Many2one('res.partner', copy = False)
    tag_ids = fields.Many2many('property.tag')
    offer_ids = fields.One2many('property.offer', 'property_id')
    total_area = fields.Integer(compute = '_compute_total_area', string = 'Total Area (sqm)')
    best_price = fields.Float(compute = '_compute_best_offer', string = 'Best Offer')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
                record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if (record.offer_ids):    
                prices = record.offer_ids.mapped("price")
                record.best_price = max(prices)
            else:
                record.best_price = 0
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'north'      
        else:
            self.garden_area = 0
            self.garden_orientation = False 

    def action_cancel(self):
        for record in self:
            if (record.state == 'sold'):
                raise exceptions.UserError("Sold property cannot be canceled")
            elif (record.state == 'canceled'):
                raise exceptions.UserError("Property is already canceled")
            record.state = 'canceled'
        return True
    
    def action_sold(self):
        for record in self:
            if (record.state == 'canceled'):
                raise exceptions.UserError("Canceled property cannot be sold")
            elif (record.state == 'sold'):
                raise exceptions.UserError("Property is already sold")
            record.state = 'sold'
        return True
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly bigger than 0'),
        ('check_selling_price', 'CHECK(selling_price > -1)', 'The selling price must be strictly bigger than 0')
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if (record.selling_price > 0):
                limit_price = record.expected_price * 0.9
                compared_prices = float_compare(record.selling_price, limit_price, precision_digits = 2 )
                if (compared_prices == -1):
                    raise ValidationError("The selling price cannot be lower than 90'%' of the expected price")

