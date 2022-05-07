from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.onchange('code')
    def _get_default_cash_account(self):
        if self.code and len(self.code) >= 3 and self.code[:3] in ['101', '102', '103']:
            is_cash_account = True
        else:
            is_cash_account = False
        self.is_cash_account = is_cash_account

    @api.onchange('code')
    def _get_default_bank_account(self):
        if self.code and len(self.code) >= 3 and self.code[:3] in ['104']:
            is_bank_account = True
        else:
            is_bank_account = False
        self.is_bank_account = is_bank_account

    is_cash_account = fields.Boolean(
        string='Es cuenta contable de efectivo')
    is_bank_account = fields.Boolean(
        string='Es cuenta contable de banco')

    def compute_is_cash_or_bank_account(self):
        for record in self:
            record._get_default_cash_account()
            record._get_default_bank_account()
