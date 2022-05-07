from datetime import datetime
from dateutil import relativedelta

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_sunat_number(self):
        if self.move_type in ['in_invoice', 'in_refund', 'in_receipt']:
            sunat_number = [self.l10n_pe_in_edi_serie,
                            self.l10n_pe_in_edi_number]
        elif self.move_type in ['out_invoice', 'out_refund', 'out_receipt']:
            sunat_number = [self.l10n_pe_edi_serie,
                            self.l10n_pe_edi_number]
        else:
            sunat_number =  ['0', '0']
        
        return sunat_number
    
    l10n_pe_payment_indicator = fields.Char(
        string='Indicador de Comprobantes de pago cancelados con medios de pago', compute='_compute_payment_indicator', store=True)
    
    @api.depends('payment_state')
    def _compute_payment_indicator(self):
        for record in self:
            if record.payment_state in ['in_progress', 'paid']:
                payment_indicator = '1'
            else:
                payment_indicator = ''
            record.l10n_pe_payment_indicator = payment_indicator
            
    def get_emission_date(self):
        return str(self.invoice_date.strftime('%d/%m/%Y'))

    def get_invoice_date_due(self):
        invoice_date_due = self.invoice_date_due #.strftime('%d/%m/%Y')
        date = self.date #.strftime('%d/%m/%Y')
        nextmonth_date = date + relativedelta.relativedelta(months=1)
        if self.l10n_latam_document_type_id.code == '14':
            str_invoice_date_due = str(invoice_date_due.strftime('%d/%m/%Y'))
        elif invoice_date_due <= nextmonth_date:
            str_invoice_date_due = str(invoice_date_due.strftime('%d/%m/%Y'))
        else:
            str_invoice_date_due = ''
        return str_invoice_date_due

    def get_correlative_move(self):
        if self.move_type != 'entry':
            move_number = "M1"
        else:
            move_number = f"M{self.seat_number}"
        return move_number

    def get_partner_identifitacion_type_code(self):
        return self.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code

    def get_partner_identifitacion_type_code_canceled_invoice(self):
        if self.l10n_latam_document_type_id.code == '01':
            identification_type_code = '0'
        else:
            identification_type_code = ''
        return identification_type_code

    l10n_pe_ple_partner_vat = fields.Char(
        string='N° Identificación', compute='get_partner_vat')

    def get_partner_vat(self):
        if self.partner_id.vat:
            partner_vat = self.partner_id.vat
        else:
            if self.get_partner_identifitacion_type_code() == '6':
                partner_vat = 'No se encontró # de RUC'
            else:
                partner_vat = '00000000'
        return partner_vat

    def get_invoice_code(self):
        invoice_code = self.l10n_latam_document_type_id.code or '00'
        return str(invoice_code)

    def get_table_11_code(self):
        table_11_code = self.dv_l10n_pe_edi_table_11_code
        if not table_11_code:
            table_11_code = ''
        return table_11_code
    
    def convert_date_to_string(self, field):
        if field:
            field_format = field.strftime('%d/%m/%Y')
        else:
            field_format = ''
        return field_format
    
    def get_account_move_period(self):
        period_date = datetime.strptime(str(self.date), '%Y-%m-%d')
        period_year = period_date.strftime('%Y')
        period_month = period_date.strftime('%m')
        self_period = f"{period_year}{period_month}00"
        return self_period
    # Notas de credito

    def get_reversed_entry_emission_date(self):
        if self.l10n_latam_document_type_id.code in ['07', '08']:
            origin_invoice_id = False
            if self.reversed_entry_id:
                origin_invoice_id = self.reversed_entry_id
            if self.debit_origin_id:
                origin_invoice_id = self.debit_origin_id
            if origin_invoice_id:
                reversed_entry_emission_date = origin_invoice_id.get_emission_date()
            else:
                reversed_entry_emission_date = self.l10n_pe_edi_reversal_date.strftime('%d/%m/%Y')
        else:
            reversed_entry_emission_date = ''
        return str(reversed_entry_emission_date)

    def get_reversed_entry_invoice_type(self):
        origin_invoice_id = False
        if self.reversed_entry_id:
            origin_invoice_id = self.reversed_entry_id
        if self.debit_origin_id:
            origin_invoice_id = self.debit_origin_id
        if origin_invoice_id:
            reversed_entry_invoice_type = origin_invoice_id.get_invoice_code()
        else:
            reversed_entry_invoice_type = ''
        return str(reversed_entry_invoice_type)

    def get_reversed_entry_invoice_serial(self):
        if self.l10n_latam_document_type_id.code in ['07', '08']:
            origin_invoice_id = False
            if self.reversed_entry_id:
                origin_invoice_id = self.reversed_entry_id
            if self.debit_origin_id:
                origin_invoice_id = self.debit_origin_id
            if origin_invoice_id:
                reversed_entry_invoice_serial = origin_invoice_id.l10n_pe_edi_serie.zfill(
                    4)
            else:
                reversed_entry_invoice_serial = self.l10n_pe_edi_reversal_serie
        else:
            reversed_entry_invoice_serial = ''
        return str(reversed_entry_invoice_serial)

    def get_reversed_entry_invoice_number(self):
        if self.l10n_latam_document_type_id.code in ['07', '08']:
            origin_invoice_id = False
            if self.reversed_entry_id:
                origin_invoice_id = self.reversed_entry_id
            if self.debit_origin_id:
                origin_invoice_id = self.debit_origin_id
            if origin_invoice_id:
                reversed_entry_invoice_number = origin_invoice_id.l10n_pe_edi_number.zfill(
                    8)
            else:
                reversed_entry_invoice_number = self.l10n_pe_edi_reversal_number
        else:
            reversed_entry_invoice_number = ''
        return str(reversed_entry_invoice_number)

    def get_signed_amount(self, amount):
        amount = round(amount, 2)
        if self.move_type in ['out_refund', 'in_refund'] and amount != 0:
            signed_amount = "{:.2f}".format(-1*amount *
                                            float(self.invoice_date_currency_rate))
        else:
            signed_amount = "{:.2f}".format(
                amount*float(self.invoice_date_currency_rate))
        return signed_amount