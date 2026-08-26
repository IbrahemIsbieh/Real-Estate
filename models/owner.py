from  odoo import fields, models


class Owner(models.Model):
    _name = "owner"
    _description = "Owner"

    name = fields.Char()
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many('property', 'owner_id')


    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This name already exists!')
    ]