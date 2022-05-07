from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def ple_1_1_fields(self):
        m_01 = []
        move_line_data = self.read([
            'id',
            'name',
            'date',
            'debit',
            'credit',
        ])[0]
        move_data = self.move_id.read([
            'id',
            'name',
        ])[0]
        sunat_number = self.move_id.get_sunat_number()
        move_name = move_line_data.get('name')
        if move_name:
            move_name = move_name.replace('\r', ' ').replace('\n', ' ').split()
            move_name = ' '.join(move_name)
        if not move_name:
            move_name = 'Movimiento'
        move_name = move_name[:200].strip()
        currency_name = self.company_currency_id.name
        l10n_pe_document_type_code = self.move_id.l10n_latam_document_type_code or '00'
        account_code = self.account_id.code or ''
        analytic_account_code = self.analytic_account_id.code or ''
        analytic_tag_codes = self.analytic_tag_ids.mapped('code')
        analytic_tags = ''
        while analytic_tag_codes and analytic_tag_codes[0] and (len('&'.join([analytic_tags, analytic_tag_codes[0]])) <= 24):
            if analytic_tag_codes[0]:
                if analytic_tags:
                    analytic_tags = '&'.join(
                        [analytic_tags, analytic_tag_codes[0]])
                else:
                    analytic_tags = analytic_tag_codes[0]
            analytic_tag_codes = analytic_tag_codes[1:]
        # 1-4
        m_01.extend([
            move_line_data.get('date').strftime('%Y%m00'),
            f"{self.move_id.seat_number}-{self.id}",
            'M' + str(move_line_data.get('id')).rjust(9, '0'),
            account_code.rstrip('0'),
        ])
        # 5-6
        m_01.extend([analytic_tags, analytic_account_code])
        # 7
        m_01.append(currency_name)
        # 8
        m_01.append(l10n_pe_document_type_code)
        # 9-10
        m_01.extend(sunat_number)
        # 11-12
        m_01.extend(['', ''])
        # 13
        m_01.append(move_line_data.get('date').strftime('%d/%m/%Y'))
        # 14-15
        m_01.extend([
            move_name,
            '',
        ])
        # 16-18
        m_01.extend([
            format(move_line_data.get('debit'), '.2f'),
            format(move_line_data.get('credit'), '.2f'),
            '',
        ])
        # 19-20
        m_01.extend(['1', ''])
        return m_01

    def ple_1_2_fields(self):
        m_02 = []
        move_line_data = self.read([
            'id',
            'name',
            'date',
            'debit',
            'credit',
        ])[0]
        move_data = self.move_id.read([
            'id',
            'name',
        ])[0]
        sunat_number = self.move_id.get_sunat_number()
        move_name = move_line_data.get('name')
        if move_name:
            move_name = move_name.replace('\r', ' ').replace('\n', ' ').split()
            move_name = ' '.join(move_name)
        if not move_name:
            move_name = 'Movimiento'
        move_name = move_name[:200].strip()
        sunat_partner_code = self.move_id.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code or ''
        sunat_partner_vat = self.move_id.partner_id.vat or ''
        sunat_partner_name = self.move_id.partner_id.name or 'varios'
        payment = self.payment_id
        # V13
        #payment_backing = payment.communication
        # TODO Agregar numero de tramsaaccion
        payment_backing = payment.ref or self.name
        payment_method_code = payment.l10n_pe_payment_method_code
        # V13
        #partner_bank = payment.partner_bank_account_id
        partner_bank = payment.partner_bank_id or (
            payment.journal_id or self.move_id.journal_id).bank_account_id
        bank_acc_number = partner_bank.acc_number or ''
        bank_code = partner_bank.bank_id.l10n_pe_bank_code or ''
        # 1-3
        m_02.extend([
            move_line_data.get('date').strftime('%Y%m00'),
            f"{self.move_id.seat_number}-{self.id}",
            'M' + str(move_line_data.get('id')).rjust(9, '0'),
        ])
        # 4-5
        m_02.extend([
            bank_code,
            bank_acc_number,
        ])
        # 6-8
        m_02.extend([
            move_line_data.get('date').strftime('%d/%m/%Y'),
            payment_method_code or '001',
            move_name or '',
        ])
        # 9-12
        m_02.extend([
            sunat_partner_code,
            sunat_partner_vat,
            sunat_partner_name,
            payment_backing,
        ])
        # 13-14
        m_02.extend([
            format(move_line_data.get('debit'), '.2f'),
            format(move_line_data.get('credit'), '.2f'),
        ])
        # 15-16
        m_02.extend([
            '1',
            '',
        ])
        return m_02
