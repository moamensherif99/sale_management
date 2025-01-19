from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    discount_limit = fields.Float(string='Discount Limit', default=0.0)

