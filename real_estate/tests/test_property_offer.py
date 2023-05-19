from odoo.tests.common import TransactionCase
from odoo.exceptions import  ValidationError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class PropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(PropertyOfferTestCase, cls).setUpClass()
        cls.property = cls.env['property'].create({
            "name" : "Big Villa",
            "state" : "sold",
            "description" : "A nice and big villa",
            "postcode" : 12345,
            "date_availability" : "2023-05-02",
            "expected_price" : 1600000,
            "bedrooms" : 6,
            "living_area" : "100",
            "facades" : "4",
            "garage" : "True",
            "garden" : "True",
            "garden_area" : 10000,
            "garden_orientation" : "south",
            "property_type_id" : 4
        })

    def test_create_offer_with_sold_property(self):
        with self.assertRaises(ValidationError) as context:
            self.env['property.offer'].create({
                'property_id' : self.property.id,
                'partner_id': '1',
                'price': 1600000
            })

        self.assertIn("You can't add an offer to a sold property", str(context.exception))

