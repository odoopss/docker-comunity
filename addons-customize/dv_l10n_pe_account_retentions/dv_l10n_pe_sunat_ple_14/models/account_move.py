from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_pe_out_annotation_opportunity_status = fields.Selection(string='Estado PLE', selection=[
        ('0', 'La operación (anotación optativa sin efecto en el IGV) corresponde al periodo.'),
        ('1', 'La operación (ventas gravadas, exoneradas, inafectas y/o exportaciones) corresponde al periodo, así como a las Notas de Crédito y Débito emitidas en el periodo.'),
        ('2', 'El documento ha sido inutilizado durante el periodo previamente a ser entregado, emitido o durante su emisión.'),
        ('8', 'La operación (ventas gravadas, exoneradas, inafectas y/o exportaciones) corresponde a un periodo anterior y NO ha sido anotada en dicho periodo.'),
        ('9', 'La operación (ventas gravadas, exoneradas, inafectas y/o exportaciones) corresponde a un periodo anterior y SI ha sido anotada en dicho periodo.')],
        default='1',
        help='Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.')

    def ple_14_1_fields(self):
        return [
            # 1 Periodo
            self.get_account_move_period(),
            # 2 CUO
            self.seat_number or '',
            # 3 Tipo de asiento correlativo M...
            self.get_correlative_move(),
            # 4 Fecha de emision
            self.get_emission_date(),
            # 5 Fecha de vencimiento de pago
            self.get_invoice_date_due(),
            # 6 Tipo Tabla 10 Codigo de Boleta o Factura
            self.get_invoice_code(),
            # 7 Serie
            self.l10n_pe_edi_serie,
            # 8 Numero correlativo del comprobante
            self.l10n_pe_edi_number,
            # 9 Numero de ticket
            '',
            # 10 Tipo de documento de identidad
            self.get_partner_identifitacion_type_code(),
            # 11 Numero de documento de identidad
            self.get_partner_vat(),
            # 12 Razon social
            self.partner_id.name,
            # 13 Valor facturado de la exportación
            '',
            # 14 Base imponible de la operación gravada
            self.get_signed_amount(
                self.l10n_pe_edi_amount_base),
            # 15 Descuento de la base imponible
            '',
            # 16 IGV
            self.get_signed_amount(
                self.l10n_pe_edi_amount_igv),
            # 17 Descuento del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal
            '',
            # 18 Importe total de la operación exonerada
            self.get_signed_amount(
                self.l10n_pe_edi_amount_exonerated_with_discount),
            # self.get_signed_amount(self.l10n_pe_edi_amount_exonerated),
            # 19 Importe total de la operación inafecta
            # self.get_signed_amount(
            #    self.l10n_pe_edi_amount_unaffected_with_discount),
            self.get_signed_amount(
                self.l10n_pe_edi_amount_unaffected),
            # self.get_signed_amount(self.l10n_pe_edi_amount_unaffected),
            # 20 ISC
            self.get_signed_amount(
                self.l10n_pe_edi_amount_isc),
            # 21 Base imponible de la operación gravada con el Impuesto a las Ventas del Arroz Pilado
            '',
            # 22 IVAP
            self.get_signed_amount(
                self.l10n_pe_edi_amount_ivap),
            # 23 ICBPER
            self.get_signed_amount(
                self.l10n_pe_edi_amount_icbper),
            # 24 Otros conceptos, tributos y cargos que no forman parte de la base imponible
            self.get_signed_amount(
                self.l10n_pe_edi_amount_others),
            # 25 Importe total del comprobante de pago
            self.get_signed_amount(
                self.amount_total),
            # 26 Código  de la Moneda (Tabla 4)
            self.currency_id.name,
            # 27 Tipo de cambio (5)
            self.invoice_date_currency_rate,
            # 28 Fecha de emisión del comprobante de pago o documento original que se modifica (6) o documento referencial al documento que sustenta el crédito fiscal
            self.get_reversed_entry_emission_date(),
            # 29 Tipo del comprobante de pago que se modifica (6)
            self.get_reversed_entry_invoice_type(),
            # 30 Número de serie del comprobante de pago que se modifica (6) o Código de la Dependencia Aduanera
            self.get_reversed_entry_invoice_serial(),
            # 31 Número del comprobante de pago que se modifica (6) o Número de la DUA, de corresponder
            self.get_reversed_entry_invoice_number(),
            # 32 Identificación del Contrato o del proyecto en el caso de los Operadores de las sociedades irregulares, consorcios, joint ventures u otras formas de contratos de colaboración empresarial, que no lleven contabilidad independiente.
            '',
            # 33 Error tipo 1: inconsistencia en el tipo de cambio
            self.l10n_pe_error_type_1_code,
            # 34 Indicador de Comprobantes de pago cancelados con medios de pago
            self.l10n_pe_payment_indicator,
            # 35 Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a alguna de las situaciones previstas en el inciso e) del artículo 8° de la Resolución de Superintendencia N.° 286-2009/SUNAT
            self.l10n_pe_out_annotation_opportunity_status,
            # 36 Campos de libre utilización.
            ''
        ]

    def ple_14_2_fields(self):
        return [
            # 1 Periodo
            self.get_account_move_period(),
            # 2 CUO
            self.seat_number or '',
            # 3 Tipo de asiento correlativo M...
            self.get_correlative_move(),
            # 4 Fecha de emision
            self.get_emission_date(),
            # 5 Fecha de vencimiento de pago
            self.get_invoice_date_due(),
            # 6 Tipo Tabla 10 Codigo de Boleta o Factura
            self.get_invoice_code(),
            # 7 Serie
            self.l10n_pe_edi_serie,
            # 8 Numero correlativo del comprobante
            self.l10n_pe_edi_number,
            # 9 Numero de ticket
            '',
            # 10 Tipo de documento de identidad
            self.get_partner_identifitacion_type_code(),
            # 11 Numero de documento de identidad
            self.get_partner_vat(),
            # 12 Razon social
            self.partner_id.name,
            # 13 Base imponible de la operación gravada
            self.get_signed_amount(self.l10n_pe_edi_amount_unaffected),
            # 14 IGV
            self.get_signed_amount(self.l10n_pe_edi_amount_igv),
            # 15 ICBPER
            self.get_signed_amount(self.l10n_pe_edi_amount_icbper),
            # 16 Otros conceptos, tributos y cargos que no forman parte de la base imponible
            self.get_signed_amount(self.l10n_pe_edi_amount_others),
            # 17 Importe total del comprobante de pago
            self.get_signed_amount(self.amount_total),
            # 18 Código  de la Moneda (Tabla 4)
            self.currency_id.name,
            # 19 Tipo de cambio (5)
            self.invoice_date_currency_rate,
            # 20 Fecha de emisión del comprobante de pago o documento original que se modifica (6) o documento referencial al documento que sustenta el crédito fiscal
            self.get_reversed_entry_emission_date(),
            # 21 Tipo del comprobante de pago que se modifica (6)
            self.get_reversed_entry_invoice_type(),
            # 22 Número de serie del comprobante de pago que se modifica (6) o Código de la Dependencia Aduanera
            self.get_reversed_entry_invoice_serial(),
            # 23 Número del comprobante de pago que se modifica (6) o Número de la DUA, de corresponder
            self.get_reversed_entry_invoice_number(),
            # 24 Error tipo 1: inconsistencia en el tipo de cambio
            self.l10n_pe_error_type_1_code,
            # 25 Indicador de Comprobantes de pago cancelados con medios de pago
            self.l10n_pe_payment_indicator,
            # 26 Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a alguna de las situaciones previstas en el inciso e) del artículo 8° de la Resolución de Superintendencia N.° 286-2009/SUNAT
            self.l10n_pe_out_annotation_opportunity_status,
            # 27 Campos de libre utilización.
            '',
        ]
