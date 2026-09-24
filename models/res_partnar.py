from odoo import models,fields,api
class ResPartner(models.Model):
    _inherit = 'res.partner'
    property_id = fields.Many2one('property')
   # هاي هي الطريقة الثانية الي اسهل للاستخدام
    price = fields.Float(related='property_id.selling_price')


# هاي طريقة مشان تعمل انو ال field يتخزن في البيانات الي انتا راح تستعملها بس في طرية ثانية اسهل والي راح استعملها فوق
    # price = fields.Float(compute='_compute_price',store=True)
    # @api.depends('property_id')
    # def _compute_price(self):
    #     for rec in self:
    #         rec.price = rec.property_id.selling_price