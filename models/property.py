from email.policy import default

from odoo import fields, models,api
from odoo.exceptions import ValidationError
from datetime import  timedelta
from odoo.release import description


class Property(models.Model):
    _name = "property"
    _inherit = ['mail.thread','mail.activity.mixin']

    ref = fields.Char(default = 'New', readonly=True)
    name = fields.Char(required=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
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
         ("sold", "Sold"),
         ("closed", "Closed"),] , default='draft'
    )

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')
    create_time = fields.Datetime(default=fields.Datetime.now)
    next_time = fields.Datetime(compute='_compute_next_time')
    active = fields.Boolean(default=True)
    _sql_constraints = [('unique_name', 'unique("name")', 'This name is exist ')]
    property_line_ids = fields.One2many('property.line', 'property_id')
    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time+ timedelta(hours=6)
            else:
                rec.next_time = False
    @api.constrains('bedroom')
    def _check_bedroom_greater_zero(self):
     for rec in self:
      if rec.bedroom== 0:
        raise ValidationError('please add valid number of bedrooms')

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'


    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

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

        # هاي اشتعملتها داخل automated action
    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
               rec.is_late = True

    def action(self):
        print(self.env['property'].search([('name','!=','Property1')])
)


    @api.model
    def create(self, vals):
        rec = super(Property, self).create(vals)
        if rec.ref == 'New':
            rec.ref =self.env['ir.sequence'].next_by_code('property_seq')
        return rec

    def create_history_record(self,old_state,new_state,reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description':line.description,'area':line.area})
                             for line in rec.property_line_ids],
            })


    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.act_window']._for_xml_id('app_onee.change_state_action')
        action['context'] = {'default_property_id':self.id}
        return action

#مشان جملة ال CREATE
    #         @api.model_create_multi
    #        def create(self, vals_list):
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
class PropertyLine(models.Model):
    _name='property.line'
    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')

