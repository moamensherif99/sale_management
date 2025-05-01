from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


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

    total_extra_fees = fields.Monetary(compute='_compute_total_extra_fees',currency_field='currency_id',store=1)

    @api.depends('order_line.extra_fees')
    def _compute_total_extra_fees(self):
        for rec in self:
            rec.total_extra_fees = sum(rec.order_line.mapped('extra_fees'))

    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent', 'waiting'}

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self:
            if self.env.user.has_group('sales_team.group_sale_manager'):
                if rec.state == 'waiting':
                    rec.state = 'sale'
                continue
            if rec.exceed_discount_limit:
                rec.state = 'waiting'
        return res

    # def action_confirm(self):
    #     for rec in self:
    #         if self.env.user.has_group('sales_team.group_sale_manager') and rec.state == 'waiting':
    #             rec.state = 'sale'
    #             continue
    #         if rec.exceed_discount_limit :
    #             rec.state = 'waiting'
    #             continue
    #     confirmable_orders = self.filtered(lambda order: order.state in ['draft', 'sent'])
    #     if confirmable_orders:
    #         res = super(SaleOrder, confirmable_orders).action_confirm()
    #         return res
    #     return True

