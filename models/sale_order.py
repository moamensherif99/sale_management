from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('waiting', 'Waiting For Approval'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('cancel', 'Cancelled'),
    ], string="Status", tracking=True, default='draft')

    exceed_discount_limit = fields.Boolean()


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self:
            if rec.exceed_discount_limit:
                rec.state = 'waiting'
        return res

