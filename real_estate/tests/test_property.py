from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class PropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(PropertyTestCase, cls).setUpClass()
        cls.property = cls.env['property'].create({
            "name" : "Big Villa",
            "state" : "new",
            "description" : "A nice and big villa",
            "postcode" : "12345",
            "date_availability" : "2023-05-02",
            "expected_price" : "1600000",
            "bedrooms" : "6",
            "living_area" : "100",
            "facades" : "4",
            "garage" : "True",
            "garden" : "True",
            "garden_area" : "10000",
            "garden_orientation" : "south",
            "property_type_id" : "4"
        })
    
    def test_action_sold_no_accepted_offer(self):
        self.env['property.offer'].create({
            'property_id': self.property.id,
            'partner_id': '1',
            'status': 'refused',
            'price' : 1600000
            
        })
        with self.assertRaises(UserError) as context:
            self.property.action_sold()

        self.assertIn("Property cannot be sold without any accepted offers", str(context.exception))
        self.assertEqual(self.property.state, 'received')

    def test_action_sold_accepted_offer(self):
        self.env['property.offer'].create({
            'property_id': self.property.id,
            'partner_id': '1',
            'status': 'accepted',
            'price' : 1600000
        })
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold')

    def test_onchange_garden(self):
        
        form = Form(self.property)
        property_record = form.save()

        property_record.garden = True
        property_record._onchange_garden()
        self.assertEqual(property_record.garden_area, 10)
        self.assertEqual(property_record.garden_orientation, "north")
        
        property_record.garden = False
        property_record._onchange_garden()
        self.assertEqual(property_record.garden_area, 0)
        self.assertFalse(property_record.garden_orientation)

