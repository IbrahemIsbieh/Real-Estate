from odoo import models,fields,api

class Owner(models.Model):

    _name = 'owner'
    _description = 'Owner'

    name = fields.Char(string='Name',required=True)
    phone = fields.Char(string='Phone',required=True)
    address = fields.Char(string='Email',required=True)
    property_ids = fields.One2many(
        'property',
        'owner_id'
    )
    _sql_constraints = [('unique_name', 'unique("name")','This name is exist')]