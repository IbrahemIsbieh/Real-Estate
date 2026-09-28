from odoo import models,fields
class AccountIn(models.Model):
    _inherit = 'account.move'

    property_id = fields.Many2one('property', string='Property')
    # def action_do_something(self):
    #     print('do something')


