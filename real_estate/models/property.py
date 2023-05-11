from odoo import fields,models,api

class Property(models.Model):
    _name = "property"
    _description = "Estate Property Model"
    
    name = fields.Char("Title", required = True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From")
    expected_price = fields.Float("Expected Price", required = True)
    selling_price = fields.Float ("Selling Price")
    bedrooms = fields.Integer("Bedrooms")
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean ("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [('north', 'North'),
                     ('south', 'South'),
                     ('east','East'), 
                     ('weast','Weast')]
    )
