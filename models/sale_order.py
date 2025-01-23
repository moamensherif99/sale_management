from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('waiting', 'Waiting For Approval'),
        ('sale', 'Sales Order'),
        ('cancel', 'Cancelled'),
    ], string="Status", tracking=True, default='draft')

    exceed_discount_limit = fields.Boolean()


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self:
            manger_group = self.env.ref('sales_team.group_sale_manager')
            if manger_group and manger_group in self.env.user.groups_id:
                continue
            elif rec.exceed_discount_limit:
                rec.state = 'waiting'
        return res

