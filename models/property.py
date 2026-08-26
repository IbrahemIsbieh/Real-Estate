from email.policy import default

from odoo import fields, models,api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = "property"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(required=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_price = fields.Float()
    diff = fields.Float(compute="_compute_diff")
    selling_price = fields.Float()
    bedroom = fields.Integer()
    facades = fields.Integer()
    living_area = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
     ]  , default=('north'))
    state=fields.Selection(
        [("draft", "draft"),
         ("pending", "Pending"),
         ("sold", "Sold"),]
    )

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')

    _sql_constraints = [('unique_name', 'unique("name")', 'This name is exist ')]

    @api.constrains('bedroom')
    def _check_bedroom_greater_zero(self):
     for rec in self:
      if rec.bedroom== 0:
        raise ValidationError('please add valid number of bedrooms')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'
    def action_sold(self):
        for rec in self:
            rec.write({'state':'sold'})

    @api.depends('expected_price','selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price
    @api.onchange('expected_price')
    def onchange_price(self):
          for rec in self:

            return {
                'warning':{'title':'warning','message':'negative value','type': 'notification'},
            }

#مشان جملة ال CREATE
    #         @api.model_create_multi
    #        def create(self, vals_list):
    #            print("inside create method")
#          res = super(Property, self).create(vals_list)
#           return res
#مشان جملة ال READE
#@api.model
#def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    # res = super(Property, self)._search(domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)
    # print("inside search method")
# return res
#هاي مشان جملة UPDETE
#def write(self, vals):
   #res= super(Property, self).write(vals)
    # print("inside write method")
# return res
#هاي هون مشان ال DELETE
#def unlink(self):
    # super(Property, self).unlink()
# print("inside unlink method")