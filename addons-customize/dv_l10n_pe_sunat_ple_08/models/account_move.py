from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_reversed_entry_table_11_code(self):
        origin_invoice_id = False
        if self.reversed_entry_id:
            origin_invoice_id = self.reversed_entry_id
        if self.debit_origin_id:
            origin_invoice_id = self.debit_origin_id
        if origin_invoice_id:
            table_11_code = origin_invoice_id.get_table_11_code()
        else:
            table_11_code = ''
        return table_11_code
    
    # ERRORES PLE
    l10n_pe_error_type_1 = fields.Boolean(
        string='Inconsistencia en el tipo de cambio', help='Error tipo 1')
    l10n_pe_error_type_1_code = fields.Char(
        string='Codigo Error tipo 1', compute='_compute_error_type_1_code', store=True)
    l10n_pe_error_type_2 = fields.Boolean(
        string='Inconsistencia por proveedores no habidos', help='Error tipo 2')
    l10n_pe_error_type_2_code = fields.Char(
        string='Codigo Error tipo 2', compute='_compute_error_type_2_code', store=True)
    l10n_pe_error_type_3 = fields.Boolean(
        string='Inconsistencia por proveedores que renunciaron a la exoneración del Apéndice I del IGV', help='Error tipo 3')
    l10n_pe_error_type_3_code = fields.Char(
        string='Codigo Error tipo 3', compute='_compute_error_type_3_code', store=True)
    l10n_pe_error_type_4 = fields.Boolean(
        string='Inconsistencia por DNIs que fueron utilizados en las Liquidaciones de Compra y que ya cuentan con RUC', help='Error tipo 4')
    l10n_pe_error_type_4_code = fields.Char(
        string='Codigo Error tipo 4', compute='_compute_error_type_4_code', store=True)
    
    l10n_pe_project_identification = fields.Char(string='Identificación del Contrato o del proyecto',
                                                 default='',
                                                 help='Identificación del Contrato o del proyecto en el caso de los Operadores de las sociedades irregulares, consorcios, joint ventures u otras formas de contratos de colaboración empresarial, que no lleven contabilidad independiente.')
    @api.depends('l10n_pe_error_type_1')
    def _compute_error_type_1_code(self):
        for record in self:
            if record.l10n_pe_error_type_1:
                record.l10n_pe_error_type_1_code = '1'
            else:
                record.l10n_pe_error_type_1_code = ''

    @api.depends('l10n_pe_error_type_2')
    def _compute_error_type_2_code(self):
        for record in self:
            if record.l10n_pe_error_type_2:
                record.l10n_pe_error_type_2_code = '1'
            else:
                record.l10n_pe_error_type_2_code = ''

    @api.depends('l10n_pe_error_type_3')
    def _compute_error_type_3_code(self):
        for record in self:
            if record.l10n_pe_error_type_3:
                record.l10n_pe_error_type_3_code = '1'
            else:
                record.l10n_pe_error_type_3_code = ''

    @api.depends('l10n_pe_error_type_4')
    def _compute_error_type_4_code(self):
        for record in self:
            if record.l10n_pe_error_type_4:
                record.l10n_pe_error_type_4_code = '1'
            else:
                record.l10n_pe_error_type_4_code = ''
                
    l10n_pe_proof_detraction_deposit_date = fields.Date(
        string='Fecha de emisión de la Constancia de Depósito de Detracción (5)')
    l10n_pe_proof_detraction_deposit_number = fields.Char(
        string='Número de la Constancia de Depósito de Detracción (5)')
    
    l10n_pe_is_subject_to_withholding = fields.Boolean(
        string='Sujeto a Retención')
    l10n_pe_subject_to_withholding_code = fields.Char(
        string='Código de sujeto a retención', compute='_compute_subject_to_withholding_code', store=True)
    @api.depends('l10n_pe_is_subject_to_withholding')
    def _compute_subject_to_withholding_code(self):
        for record in self:
            if record.l10n_pe_error_type_1:
                record.l10n_pe_subject_to_withholding_code = '1'
            else:
                record.l10n_pe_subject_to_withholding_code = ''
                
    l10n_pe_operation_type = fields.Selection([
        ('1', 'INTERNAL SALE'),
        ('2', 'EXPORTATION'),
        ('3', 'NON-DOMICILED'),
        ('4', 'INTERNAL SALE - ADVANCES'),
        ('5', 'ITINERANT SALE'),
        ('6', 'GUIDE INVOICE'),
        ('7', 'SALE PILADO RICE'),
        ('8', 'INVOICE - PROOF OF PERCEPTION'),
        ('10', 'INVOICE - SENDING GUIDE'),
        ('11', 'INVOICE - CARRIER GUIDE'),
        ('12', 'SALES TICKET - PROOF OF PERCEPTION'),
        ('13', 'NATURAL PERSON DEDUCTIBLE EXPENSE'),
    ], string='Transaction type', help='Default 1, the others are for very special types of operations, do not hesitate to consult with us for more information', default='1')
    
    l10n_pe_adquisition_type = fields.Selection(string='Tipo de adquisicion', selection=[('grav', 'Adquisiciones Gravadas Destinadas a Ventas Gravadas y/o Exportaciones'),
                                                                                         ('grav_and_nograv', 'Adquisiciones gravadas Destinadas a Ventas Gravadas y/o Exportaciones y a Ventas no Gravadas'),
                                                                                         ('grav_to_nograv', 'Adquisiciones Gravadas Destinadas a Ventas no Gravadas'),
                                                                                         ('nograv', 'Adquisiciones no Gravadas')], default='grav')
    l10n_pe_edi_amount_exportation = fields.Float(
        string='Valor facturado de la exportación', compute='_compute_tax_base_type')
    l10n_pe_tax_base_grav_amount = fields.Float(
        string='Base imponible tipo 1', help='Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a favor por exportación, destinadas exclusivamente a operaciones gravadas y/o de exportación', compute='_compute_tax_base_type')
    l10n_pe_tax_base_grav_and_nograv_amount = fields.Float(
        string='Base imponible tipo 2', help='Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a favor por exportación, destinadas a operaciones gravadas y/o de exportación y a operaciones no gravadas', compute='_compute_tax_base_type')
    l10n_pe_tax_base_grav_to_nograv_amount = fields.Float(
        string='Base imponible tipo 3', help='Base imponible de las adquisiciones gravadas que no dan derecho a crédito fiscal y/o saldo a favor por exportación, por no estar destinadas a operaciones gravadas y/o de exportación.', compute='_compute_tax_base_type')
    l10n_pe_nograv_amount = fields.Float(
        string='Valor no gravado', help='Valor de las adquisiciones no gravadas', compute='_compute_l10n_pe_nograv_amount')

    def _compute_l10n_pe_nograv_amount(self):
        for record in self:
            l10n_pe_nograv_amount = record.l10n_pe_edi_amount_exonerated + \
                record.l10n_pe_edi_amount_unaffected
            record.l10n_pe_nograv_amount = l10n_pe_nograv_amount

    l10n_pe_igv_type_1_amount = fields.Float(
        string='Valor no gravado', help='Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal del Campo 14.', compute='_compute_tax_base_type')
    l10n_pe_igv_type_2_amount = fields.Float(
        string='Valor no gravado', help='Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal del Campo 16.', compute='_compute_tax_base_type')
    l10n_pe_igv_type_3_amount = fields.Float(
        string='Valor no gravado', help='Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal del Campo 18.', compute='_compute_tax_base_type')

    l10n_pe_nograv_amount = fields.Float(
        string='Valor no gravado', help='Valor de las adquisiciones no gravadas', compute='_compute_tax_base_type')

    l10n_pe_igv_type_1_amount = fields.Float(
        string='Valor no gravado', help='Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal del Campo 14.', compute='_compute_tax_base_type')
    l10n_pe_igv_type_2_amount = fields.Float(
        string='Valor no gravado', help='Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal del Campo 16.', compute='_compute_tax_base_type')
    l10n_pe_igv_type_3_amount = fields.Float(
        string='Valor no gravado', help='Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal del Campo 18.', compute='_compute_tax_base_type')

    def _compute_tax_base_type(self):
        for record in self:
            l10n_pe_tax_base_grav_amount = False
            l10n_pe_tax_base_grav_and_nograv_amount = False
            l10n_pe_tax_base_grav_to_nograv_amount = False
            l10n_pe_edi_amount_exportation = False
            l10n_pe_nograv_amount = False
            l10n_pe_igv_type_1_amount = False
            l10n_pe_igv_type_2_amount = False
            l10n_pe_igv_type_3_amount = False
            if record.l10n_pe_operation_type == '2':  # EXPORTACIONES
                l10n_pe_edi_amount_exportation = record.l10n_pe_edi_amount_base
            else:
                if record.l10n_pe_adquisition_type == 'grav':
                    l10n_pe_tax_base_grav_amount = record.l10n_pe_edi_amount_base
                    l10n_pe_igv_type_1_amount = record.l10n_pe_edi_amount_igv
                elif record.l10n_pe_adquisition_type == 'grav_and_nograv':
                    l10n_pe_tax_base_grav_and_nograv_amount = record.l10n_pe_edi_amount_base
                    l10n_pe_igv_type_2_amount = record.l10n_pe_edi_amount_igv
                elif record.l10n_pe_adquisition_type == 'grav_to_nograv':
                    l10n_pe_tax_base_grav_to_nograv_amount = record.l10n_pe_edi_amount_base
                    l10n_pe_igv_type_3_amount = record.l10n_pe_edi_amount_igv
                l10n_pe_nograv_amount = record.l10n_pe_edi_amount_exonerated + \
                    record.l10n_pe_edi_amount_unaffected
            record.write({
                'l10n_pe_edi_amount_exportation': l10n_pe_edi_amount_exportation,
                'l10n_pe_tax_base_grav_amount': l10n_pe_tax_base_grav_amount,
                'l10n_pe_tax_base_grav_and_nograv_amount': l10n_pe_tax_base_grav_and_nograv_amount,
                'l10n_pe_tax_base_grav_to_nograv_amount': l10n_pe_tax_base_grav_to_nograv_amount,
                'l10n_pe_nograv_amount': l10n_pe_nograv_amount,
                'l10n_pe_igv_type_1_amount': l10n_pe_igv_type_1_amount,
                'l10n_pe_igv_type_2_amount': l10n_pe_igv_type_2_amount,
                'l10n_pe_igv_type_3_amount': l10n_pe_igv_type_3_amount,
            })
    
    l10n_pe_in_annotation_opportunity_status = fields.Selection(string='Estado PLE Compras', selection=[
        ('0', 'Base imponible adquisiciones gravadas que no dan derecho a crédito fiscal, destinadas a operaciones no gravadas(campo 18)  >0'),
        ('1', 'Si fecha de emisión o fecha de pago de impuesto, por operaciones que dan derecho a crédito fiscal, corresponde al período de declaración.(campo 14 o campo 16 mayores a cero)'),
        ('6', 'Si fecha de emisión o fecha de pago de impuesto, por operaciones que dan derecho a crédito fiscal,  es anterior al periodo de declaración y dentro los doce meses siguientes a la emisión o pago del impuesto.(campo 14 o campo 16 mayores a cero)'),
        ('7', 'Si fecha de emisión o fecha de pago de impuesto, por operaciones que no dan derecho a crédito fiscal,  es anterior al periodo de declaración y dentro los doce meses siguientes a la emisión o pago del impuesto.(campo 14 o campo 16 mayores a cero)'),
        ('9', 'Si se realiza un ajuste o rectificación en la información de una operación registrada en un periodo anterior.')],
        default='1',
        help='Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.',
        compute='_compute_in_annotation_opportunity_status', readonly=False)

    def _compute_in_annotation_opportunity_status(self):
        for record in self:
            if record.l10n_latam_document_type_id.code == '03':
                l10n_pe_in_annotation_opportunity_status = '0'
            elif record.invoice_date and record.date:
                previous_month = int(record.invoice_date.strftime(
                    '%m')) < int(record.date.strftime('%m'))
                previous_year = int(record.invoice_date.strftime(
                    '%Y')) < int(record.date.strftime('%Y'))
                if previous_month or previous_year:
                    l10n_pe_in_annotation_opportunity_status = '6'
                else:
                    l10n_pe_in_annotation_opportunity_status = '1'
            else:
                l10n_pe_in_annotation_opportunity_status = False
            record.l10n_pe_in_annotation_opportunity_status = l10n_pe_in_annotation_opportunity_status
            
    def ple_8_1_fields(self):
        m_01 = []
        #1-4
        #m_01.extend([periodo.strftime('%Y%m00'), str(number), ('A'+str(number).rjust(9,'0')), invoice.invoice_date.strftime('%d/%m/%Y')])
        m_01.extend([
            # 1 REQUIRED: Periodo
            self.get_account_move_period(),
            # 2 REQUIRED: CUO
            self.seat_number or '',
            # 3 REQUIRED: Tipo de asiento correlativo M...
            self.get_correlative_move(),
            # 4 REQUIRED: Fecha de emision
            self.get_emission_date(),
            # 5 Fecha de vencimiento de pago
            self.get_invoice_date_due(),
            # 6 REQUIRED: Tipo de Comprobante de Pago o Documento
            self.get_invoice_code(),
            # 7 Serie
            self.l10n_pe_in_edi_serie.zfill(4),
            # 8 Año de emisión de la DUA o DSI
            self.l10n_pe_dua_emission_year or '',
            # 9 REQUIRED: Numero correlativo del comprobante
            self.l10n_pe_in_edi_number.zfill(8),
            # 10 En caso de optar por anotar el importe total de las operaciones diarias que no otorguen derecho a crédito fiscal en forma consolidada, registrar el número final (2).
            '',
            # 11 Tipo de documento de identidad
            self.get_partner_identifitacion_type_code(),
            # 12 Numero de documento de identidad
            self.get_partner_vat(),
            # 13 Razon social
            self.partner_id.name,
            # 14 Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a favor por exportación, destinadas exclusivamente a operaciones gravadas y/o de exportación
            self.get_signed_amount(self.l10n_pe_tax_base_grav_amount),
            # 15 Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal
            self.get_signed_amount(self.l10n_pe_igv_type_1_amount),
            # 16 Base imponible de las adquisiciones gravadas que dan derecho a crédito fiscal y/o saldo a favor por exportación, destinadas a operaciones gravadas y/o de exportación y a operaciones no gravadas
            self.get_signed_amount(
                self.l10n_pe_tax_base_grav_and_nograv_amount),
            # 17 Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal
            self.get_signed_amount(self.l10n_pe_igv_type_2_amount),
            # 18 Base imponible de las adquisiciones gravadas que no dan derecho a crédito fiscal y/o saldo a favor por exportación, por no estar destinadas a operaciones gravadas y/o de exportación.
            self.get_signed_amount(
                self.l10n_pe_tax_base_grav_to_nograv_amount),
            # 19 Monto del Impuesto General a las Ventas y/o Impuesto de Promoción Municipal
            self.get_signed_amount(self.l10n_pe_igv_type_3_amount),
            # 20 Valor de las adquisiciones no gravadas
            self.get_signed_amount(self.l10n_pe_nograv_amount),
            # 21 ISC
            self.get_signed_amount(self.l10n_pe_edi_amount_isc),
            # 22 Impuesto al Consumo de las Bolsas de Plástico.
            self.get_signed_amount(self.l10n_pe_edi_amount_icbper),
            # 23 Otros conceptos, tributos y cargos que no formen parte de la base imponible.
            self.get_signed_amount(self.l10n_pe_edi_amount_others),
            # 24 REQUIRED: Importe total de las adquisiciones registradas según comprobante de pago.
            self.get_signed_amount(self.amount_total),
            # 25 Código  de la Moneda (Tabla 4)
            self.currency_id.name,
            # 26 Tipo de cambio (5)
            self.invoice_date_currency_rate,
            # 27 Fecha de emisión del comprobante de pago que se modifica (4).
            self.get_reversed_entry_emission_date(),
            # 28 Tipo de comprobante de pago que se modifica (4).
            self.get_reversed_entry_invoice_type(),
            # 29 Número de serie del comprobante de pago que se modifica (4).
            self.get_reversed_entry_invoice_serial(),
            # 30 Código de la dependencia Aduanera de la Declaración Única de Aduanas (DUA) o de la Declaración Simplificada de Importación (DSI) .
            self.get_reversed_entry_table_11_code(),
            # 31 Número del comprobante de pago que se modifica (4).
            self.get_reversed_entry_invoice_number(),
            # 32 Fecha de emisión de la Constancia de Depósito de Detracción (6)
            self.convert_date_to_string(
                self.l10n_pe_proof_detraction_deposit_date),
            # 33 Número de la Constancia de Depósito de Detracción (6)
            self.l10n_pe_proof_detraction_deposit_number or '',
            # 34 Marca del comprobante de pago sujeto a retención
            self.l10n_pe_subject_to_withholding_code or '',
            # 35 Clasificación de los bienes y servicios adquiridos (Tabla 30) - mayor a 1 500 UIT
            self.l10n_pe_edi_table_30_code or '',
            # 36 Identificación del Contrato o del proyecto en el caso de los Operadores de las sociedades irregulares, consorcios, joint ventures u otras formas de contratos de colaboración empresarial, que no lleven contabilidad independiente.
            self.l10n_pe_project_identification or '',
            # 37 Error tipo 1: inconsistencia en el tipo de cambio
            self.l10n_pe_error_type_1_code,
            # 38 Error tipo 2: inconsistencia por proveedores no habidos
            self.l10n_pe_error_type_2_code,
            # 39 Error tipo 3: inconsistencia por proveedores que renunciaron a la exoneración del Apéndice I del IGV
            self.l10n_pe_error_type_3_code,
            # 40 Error tipo 4: inconsistencia por DNIs que fueron utilizados en las Liquidaciones de Compra y que ya cuentan con RUC
            self.l10n_pe_error_type_4_code,
            # 41 Indicador de Comprobantes de pago cancelados con medios de pago
            self.l10n_pe_payment_indicator,
            # 42 REQUIRED: Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.
            self.l10n_pe_in_annotation_opportunity_status,
            # 43 Campos de libre utilización.
            ''
        ])
        
        return m_01
    
    def ple_8_2_fields(self):
        m_01 = self.ple_8_1_fields()
        m_02 = []
        # 1-4
        m_02.extend(m_01[0:5])
        # 5-7
        m_02.extend(m_01[6:9]),
        # 8-10
        m_02.extend([m_01[23],'',m_01[23]]),
        # 11-15
        m_02.extend([
            # 11 Tipo de Comprobante de Pago o Documento que sustenta el crédito fiscal
            self.l10n_pe_non_domic_sustent_document_type_id.code or '',
            # 12 Serie del comprobante de pago o documento que sustenta el crédito fiscal. En los casos de la Declaración Única de Aduanas (DUA) o de la Declaración Simplificada de Importación (DSI) se consignará el código de la dependencia Aduanera.
            self.l10n_pe_non_domic_sustent_serie or '',
            # 13 Año de emisión de la DUA o DSI que sustenta el crédito fiscal
            self.l10n_pe_non_domic_sustent_dua_emission_year or '',
            # 14 Número del comprobante de pago o documento o número de orden del formulario físico o virtual donde conste el pago del impuesto, tratándose de la utilización de servicios prestados por no domiciliados u otros, número de la DUA o de la DSI, que sustente el crédito fiscal.
            self.l10n_pe_non_domic_sustent_number or '',
            # 15 Monto de retención del IGV
            str(self.l10n_pe_non_domic_igv_withholding_amount),
        ])
        # 16-24
        m_02.extend([
                # 16 REQUIRED: Código  de la Moneda (Tabla 4)
                self.currency_id.name,
                # 17 Tipo de cambio (5)
                self.invoice_date_currency_rate or '',
                # 18 REQUIRED: Pais de la residencia del sujeto no domiciliado
                self.l10n_pe_partner_country_name or '',
                # 19 REQUIRED: Apellidos y nombres, denominación o razón social  del sujeto no domiciliado. En caso de personas naturales se debe consignar los datos en el siguiente orden: apellido paterno, apellido materno y nombre completo.
                self.l10n_pe_partner_name or '',
                # 20 Domicilio en el extranjero del sujeto no domiciliado
                self.l10n_pe_partner_street or '',
                # 21 REQUIRED: Número de identificación del sujeto no domiciliado
                self.l10n_pe_partner_vat or '',
                # 22 Número de identificación fiscal del beneficiario efectivo de los pagos
                '',
                # 23 Apellidos y nombres, denominación o razón social  del beneficiario efectivo de los pagos. En caso de personas naturales se debe consignar los datos en el siguiente orden: apellido paterno, apellido materno y nombre completo.
                '',
                # 24 Pais de la residencia del beneficiario efectivo de los pagos
                '',
        ])
        # 25-36
        m_02.extend([
            # 25 Vínculo entre el contribuyente y el residente en el extranjero
            self.l10n_pe_non_domic_vinculation_id.code or '',
            # 26 Renta Bruta
            str(self.l10n_pe_non_domic_brute_rent_amount),
            # 27 Deducción / Costo de Enajenación de bienes de capital
            str(self.l10n_pe_non_domic_disposal_capital_assets_cost),
            # 28 Renta Neta
            str(self.l10n_pe_non_domic_net_rent_amount),
            # 29 Tasa de retención
            str(self.l10n_pe_non_domic_withholding_rate),
            # 30 Impuesto retenido
            str(self.l10n_pe_non_domic_withheld_tax),
            # 31 REQUIRED: Convenios para evitar la doble imposición Tabla 25
            self.l10n_pe_non_domic_agreement_id.code or '',
            # 32 Exoneración aplicada
            self.l10n_pe_non_domic_applied_exemption_id.code or '',
            # 33 REQUIRED: Tipo de Renta
            self.l10n_pe_non_domic_rent_type_id.code or '',
            # 34 Modalidad del servicio prestado por el no domiciliado
            self.l10n_pe_non_domic_service_type_id.code or '',
            # 35 Aplicación del penultimo parrafo del Art. 76° de la Ley del Impuesto a la Renta
            self.l10n_pe_non_domic_tax_rent_code or '',
            # 36 REQUIRED: Estado que identifica la oportunidad de la anotación o indicación si ésta corresponde a un ajuste.
            self.l10n_pe_no_domic_annotation_opportunity_status or '',
            # 37 Campos de libre utilización
            ''
        ])
        return m_02
    
    def ple_8_3_fields(self):
        m_01 = self.ple_8_1_fields()
        m_03 = []
        m_03.extend(m_01[0:4])
        m_03.append(m_01[4])
        m_03.extend([
            m_01[5],
            m_01[6],
            m_01[8],
        ])
        m_03.extend(m_01[10:13])
        m_03.extend(m_01[13:15])
        m_03.append(m_01[21]) #ICBP
        m_03.extend(m_01[22:26])
        m_03.extend([
            m_01[26],
            m_01[27],
            m_01[28],
            m_01[30],
        ])
        m_03.extend(m_01[31:35]+m_01[36:39]+m_01[40:])
        return m_03