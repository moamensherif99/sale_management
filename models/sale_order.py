from odoo import models, fields

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('waiting', 'Waiting For Approval'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('cancel', 'Cancelled'),
    ], string="Status", tracking=True, default='draft')

