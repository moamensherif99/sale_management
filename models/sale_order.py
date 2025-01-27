from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    SALE_ORDER_STATE = [
        ('draft', "Quotation"),
        ('sent', "Quotation Sent"),
        ('waiting', 'Waiting For Approval'),
        ('sale', "Sales Order"),
        ('cancel', "Cancelled"),
    ]
    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    exceed_discount_limit = fields.Boolean()

    def action_confirm(self):
        for rec in self:
            if self.env.user.has_group('sales_team.group_sale_manager') and rec.state == 'waiting':
                rec.state = 'sale'
                continue
            if rec.exceed_discount_limit :
                rec.state = 'waiting'
                continue
        confirmable_orders = self.filtered(lambda order: order.state in ['draft', 'sent'])
        if confirmable_orders:
            res = super(SaleOrder, confirmable_orders).action_confirm()
            return res
        return True

