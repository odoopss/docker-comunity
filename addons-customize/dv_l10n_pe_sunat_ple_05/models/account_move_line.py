from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def ple_5_1_fields(self):
        ple_5_1 = []
        sunat_number = self.move_id.get_sunat_number()
        sunat_partner_code = self.move_id.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code
        move_id = self.id
        move_name = self.name
        sunat_partner_vat = self.move_id.partner_id.vat or ''
        if move_name:
            move_name = move_name.replace(
                '\r', ' ').replace('\n', ' ').split()
            move_name = ' '.join(move_name)
        if not move_name:
            move_name = 'Movimiento'
        move_name = move_name[:200].strip()
        date = self.date
        # 1-4
        ple_5_1.extend([
            date.strftime('%Y%m00'),
            f"{self.move_id.seat_number}-{self.id}",
            ('M'+str(move_id).rjust(9, '0')),
            self.account_id.code.rstrip('0'),
        ])
        # 5-6
        ple_5_1.extend(['',
                        self.analytic_account_id.code or ''
                        ])
        # 7
        # ple_5_1.append(self.always_set_currency_id.name)
        ple_5_1.append(self.currency_id.name)
        # 8-9
        if sunat_partner_code and sunat_partner_vat:
            ple_5_1.extend([
                sunat_partner_code,
                sunat_partner_vat,
            ])
        else:
            ple_5_1.extend(['', ''])
        # 10
        ple_5_1.append((self.move_id.l10n_latam_document_type_code or '00'))
        # 11-12
        ple_5_1.extend(sunat_number)
        # 13-14
        ple_5_1.extend([date.strftime('%d/%m/%Y'), ''])
        # 15
        ple_5_1.append(date.strftime('%d/%m/%Y'))
        # 16-17
        ple_5_1.extend([
            move_name,
            '',
        ])
        # 18-20
        ple_5_1.extend([format(self.debit, '.2f'),
                        format(self.credit, '.2f'), ''])
        # 21-22
        ple_5_1.extend(['1', ''])
        return ple_5_1

    def ple_5_2_fields(self, ple_5_1):
        ple_5_2 = []
        # 1-4
        ple_5_2.extend(ple_5_1[0:4])
        # 5-6
        ple_5_2.extend(ple_5_1[4:6])
        # 7
        ple_5_2.append(ple_5_1[6])
        # 8-9
        ple_5_2.extend(ple_5_1[7:9])
        # 10
        ple_5_2.append(ple_5_1[9])
        # 11-12
        ple_5_2.extend(ple_5_1[10:12])
        # 13-14
        ple_5_2.extend(ple_5_1[12:14])
        # 15
        ple_5_2.append(ple_5_1[14])
        # 16-17
        ple_5_2.extend(ple_5_1[15:17])
        # 18-20
        ple_5_2.extend(ple_5_1[17:20])
        # 21-22
        ple_5_2.extend(ple_5_1[20:])
        return ple_5_2
