from odoo import fields, models


class Client(models.Model):
    _name = "client"
    _inherit="owner"

