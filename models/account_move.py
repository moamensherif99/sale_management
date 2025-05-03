from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    total_extra_fees = fields.Monetary(compute="_compute_total_extra_fees",currency_field="currency_id",store=1)


    @api.depends('invoice_line_ids.extra_fees')
    def _compute_total_extra_fees(self):
        for rec in self:
            rec.total_extra_fees = sum(rec.invoice_line_ids.mapped('extra_fees'))

