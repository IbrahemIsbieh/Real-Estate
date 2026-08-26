from odoo import fields, models


class TAg(models.Model):
    _name = "tag"

    name = fields.Char()

