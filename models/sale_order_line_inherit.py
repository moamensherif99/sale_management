from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.constrains('discount')
    def _check_discount(self):
        for rec in self:
            if rec.discount and rec.discount > rec.product_template_id.discount_limit:
                raise ValidationError(
                    f"Discount limit exceeded! The maximum discount allowed for this product is {rec.product_template_id.discount_limit}%."
                )