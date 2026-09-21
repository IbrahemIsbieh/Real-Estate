from odoo import models,fields
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property',string='Property')

    # def action_confirm(self):
    #     rec =super(SaleOrder).action_confirm()
    #     return rec
    #
    #  هاذ يعتبر كا تمرين على inherit+super
    #

