from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('discount')
    def _check_discount_limit(self):
        for rec in self:
            if rec.order_id.exceed_discount_limit:
                continue
            if rec.discount:
                if rec.product_id.discount_limit == 0 and rec.discount > rec.product_id.categ_id.discount_limit:
                    raise ValidationError(
                        f"Discount limit exceeded! The maximum discount allowed for this product is {rec.product_id.categ_id.discount_limit}%."
                    )
                elif rec.discount > rec.product_id.discount_limit:
                    raise ValidationError(
                        f"Discount limit exceeded! The maximum discount allowed for this product is {rec.product_id.discount_limit}%."
                    )
