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
        res = super(SaleOrder, self).action_confirm()
        manger_group = self.env.ref('sales_team.group_sale_manager', raise_if_not_found=False)
        for rec in self:
            if manger_group and manger_group in self.env.user.groups_id:
                if rec.state == 'waiting':
                    rec.state = 'sale'
                continue
            if rec.exceed_discount_limit:
                rec.state = 'waiting'
        return res

