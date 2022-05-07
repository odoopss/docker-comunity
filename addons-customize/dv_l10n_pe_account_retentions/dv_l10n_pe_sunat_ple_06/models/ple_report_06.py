# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from ...dv_l10n_pe_sunat_ple.models.ple_report import get_last_day
from ...dv_l10n_pe_sunat_ple.models.ple_report import fill_name_data
from ...dv_l10n_pe_sunat_ple.models.ple_report import number_to_ascii_chr

#import base64
from base64 import b64decode, b64encode
import datetime
from io import StringIO, BytesIO
import logging
_logging = logging.getLogger(__name__)

class PLEReport06(models.Model) :
	_name = 'ple.report.06'
	_description = 'PLE 06 - Estructura del Libro Mayor'
	_inherit = 'ple.report.templ'
	
	year = fields.Integer(required=True)
	month = fields.Selection(selection_add=[], required=True)
	
	line_ids = fields.Many2many(comodel_name='account.move.line', string='Movimientos', readonly=True)
	
	ple_txt_01 = fields.Text(string='Contenido del TXT 6.1')
	ple_txt_01_binary = fields.Binary(string='TXT 6.1')
	ple_txt_01_filename = fields.Char(string='Nombre del TXT 6.1')
	ple_xls_01_binary = fields.Binary(string='Excel 6.1')
	ple_xls_01_filename = fields.Char(string='Nombre del Excel 6.1')
	
	sql_constraints = [
		('ple_report_06_unique', 'UNIQUE(year, month, company_id)', 'Esta estructura ya está registrada para este periodo.'),
	]
	
	def get_default_filename(self, ple_id='060100', tiene_datos=False) :
		name = super().get_default_filename()
		name_dict = {
			'month': str(self.month).rjust(2,'0'),
			'ple_id': ple_id,
		}
		if not tiene_datos :
			name_dict.update({
				'contenido': '0',
			})
		fill_name_data(name_dict)
		name = name % name_dict
		return name
	
	def update_report(self) :
		res = super().update_report()
		start = datetime.date(self.year, int(self.month), 1)
		end = get_last_day(start)
		#current_offset = fields.Datetime.context_timestamp(self, fields.Datetime.now()).utcoffset()
		#start = start - current_offset
		#end = end - current_offset
		lines = self.env.ref('base.pe').id
		lines = [
			('company_id','=',self.company_id.id),
			('company_id.partner_id.country_id','=',lines),
			('move_id.state','=','posted'),
			('date','>=',str(start)),
			('date','<=',str(end)),
		]
		lines = self.env[self.line_ids._name].search(lines, order='date asc')
		self.line_ids = lines
		return res
	
	def generate_report(self) :
		res = super().generate_report()
		lines_to_write_01 = []
		lines = self.line_ids.sudo()
		for move in lines :
			m_01 = []
			
			sunat_number = move.move_id.get_sunat_number()
			sunat_partner_code = move.move_id.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code
			sunat_partner_vat = move.move_id.partner_id.vat
			move_id = move.id
			move_name = move.name
			if move_name :
				move_name = move_name.replace('\r', ' ').replace('\n', ' ').split()
				move_name = ' '.join(move_name)
			if not move_name :
				move_name = 'Movimiento'
			move_name = move_name[:200].strip()
			date = move.date
			#1-4
			m_01.extend([
				date.strftime('%Y%m00'),
				f"{move.move_id.seat_number}-{move.id}",
				('M'+str(move_id).rjust(9,'0')),
				move.account_id.code.rstrip('0'),
			])
			#5-6
			m_01.extend(['', 
			#self.move.analytic_account_id.code,
			''])
			#7
			#m_01.append(move.always_set_currency_id.name)
			m_01.append(move.currency_id.name)
			#8-9
			if sunat_partner_code and sunat_partner_vat :
				m_01.extend([
					sunat_partner_code,
					sunat_partner_vat,
				])
			else :
				m_01.extend(['', ''])
			#10
			m_01.append((move.move_id.l10n_latam_document_type_code or '00'))
			#11-12
			m_01.extend(sunat_number)
			#13-14
			m_01.extend(['', ''])
			#15
			m_01.append(date.strftime('%d/%m/%Y'))
			#16-17
			m_01.extend([
				move_name,
				'',
			])
			#18-20
			m_01.extend([format(move.debit, '.2f'), format(move.credit, '.2f'), ''])
			#21-22
			m_01.extend(['1', ''])
			
			if m_01 :
				lines_to_write_01.append('|'.join(m_01))
		name_01 = self.get_default_filename(ple_id='060100', tiene_datos=bool(lines_to_write_01))
		lines_to_write_01.append('')
		txt_string_01 = '\r\n'.join(lines_to_write_01)
		dict_to_write = dict()
		if txt_string_01 :
			xlsx_file_base_64 = self._generate_xlsx_base64_bytes(lines_to_write_01, name_01[2:], headers=[
				'Periodo',
				'Código Único de la Operación (CUO)',
				'Número correlativo del asiento contable',
				'Código de la cuenta contable desagregado en subcuentas al nivel máximo de dígitos utilizado',
				'Código de la Unidad de Operación, de la Unidad Económica Administrativa, de la Unidad de Negocio, de la Unidad de Producción, de la Línea, de la Concesión, del Local o del Lote',
				'Código del Centro de Costos, Centro de Utilidades o Centro de Inversión',
				'Tipo de Moneda de origen',
				'Tipo de documento de identidad del emisor',
				'Número de documento de identidad del emisor',
				'Tipo de Comprobante de Pago o Documento asociada a la operación',
				'Número de serie del comprobante de pago o documento asociada a la operación',
				'Número del comprobante de pago o documento asociada a la operación',
				'Fecha contable',
				'Fecha de vencimiento',
				'Fecha de la operación o emisión',
				'Glosa o descripción de la naturaleza de la operación registrada',
				'Glosa referencial',
				'Movimientos del Debe',
				'Movimientos del Haber',
				'Código del libro, campo 1, campo 2 y campo 3 del Registro de Ventas e Ingresos o del Registro de Compras',
				'Indica el estado de la operación',
			])
			dict_to_write.update({
				'ple_txt_01': txt_string_01,
				'ple_txt_01_binary': b64encode(txt_string_01.encode()),
				'ple_txt_01_filename': name_01 + '.txt',
				'ple_xls_01_binary': xlsx_file_base_64.encode(),
				'ple_xls_01_filename': name_01 + '.xls',
			})
		else :
			dict_to_write.update({
				'ple_txt_01': False,
				'ple_txt_01_binary': False,
				'ple_txt_01_filename': False,
				'ple_xls_01_binary': False,
				'ple_xls_01_filename': False,
			})
		dict_to_write.update({
			'date_generated': str(fields.Datetime.now()),
		})
		res = self.write(dict_to_write)
		return res
