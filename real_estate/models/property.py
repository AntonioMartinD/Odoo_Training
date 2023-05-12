from datetime import timedelta
from odoo import fields,models

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
