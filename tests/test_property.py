from odoo.tests.common import TransactionCase
from odoo import fields


class TestProperty(TransactionCase):

    def setUp(self,*args,**kwargs):
        super(TestProperty,self).setUp()

        self.property_01_record = self.env['property'].create({
            'name': 'Property 01',
            'description': 'Property 01120102',
            'postcode':'909090',
            'date_availability': fields.Date.today(),
            'bedroom': 10
        })

    def test_01_property_values(self):
        property_id = self.property_01_record

        self.assertRecordValues(property_id, [{
            'name': 'Property 01',
            'description': 'Property 01120102',
            'postcode': '909090',
            'date_availability': fields.Date.today(),
            'bedroom': 10

        }])

