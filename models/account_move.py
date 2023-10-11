import logging
from odoo import fields, models, api
from odoo.tools import (
    format_date,
)    

_logger = logging.getLogger(__name__)

class  AccountMove(models.Model):
    _inherit = "account.move"

    payment_term_details = fields.Binary(string="term details", compute="_compute_payment_term_details")

    def _compute_payment_term_details(self):
        '''
        Returns an [] containing the payment term's information to be displayed on the invoice's PDF.
        '''
        for invoice in self:
            sign = 1 if invoice.is_inbound(include_receipts=True) else -1
            payment_term_details = []
            for line in invoice.line_ids.filtered(lambda l: l.date_maturity).sorted('date_maturity'):
            # for line in invoice.line_ids:
                if line.date_maturity < invoice.invoice_date_due:
                    payment_term_details.append({
                        'date': format_date(self.env, line.date_maturity),
                        'amount': sign * line.amount_currency,
                    })
                    _logger.info("test %s ", payment_term_details)
            if len(payment_term_details) > 0 :
                invoice.payment_term_details = payment_term_details
            else: 
                invoice.payment_term_details = False