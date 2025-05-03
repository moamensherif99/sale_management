from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    extra_fees = fields.Monetary(currency_field="currency_id")
