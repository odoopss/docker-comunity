from odoo import models, fields


class AccountAccount(models.Model):
    _inherit = 'account.account'

    def ple_5_3_fields(self, period):
        ple_5_3 = [
            period,
            self.code,
            self.name[:100],
            '01',
            '',
            '',
            '',
            '1',
            ''
        ]
        return ple_5_3

    def ple_5_4_fields(self, period):
        ple_5_4 = [
            # 1
            period,
            # 2
            self.code,
            # 3
            self.name[:100],
            # 4
            '01',
            # 5
            '',
            # 6
            '',
            # 7
            '',
            # 8
            '1',
            # 9
            ''
        ]

        return ple_5_4
