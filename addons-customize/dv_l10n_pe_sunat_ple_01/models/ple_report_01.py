# -*- coding: utf-8 -*-

from .ple_headers import PLE_1_1_HEADER, PLE_1_2_HEADER
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning

from ...dv_l10n_pe_sunat_ple.models.ple_report import get_last_day
from ...dv_l10n_pe_sunat_ple.models.ple_report import fill_name_data
from ...dv_l10n_pe_sunat_ple.models.ple_report import number_to_ascii_chr

from base64 import b64decode, b64encode
import datetime
import logging
_logging = logging.getLogger(__name__)

class PLEReport01(models.Model) :
	_name = 'ple.report.01'
	_description = 'PLE 01 - Estructura del Libro Caja y Bancos'
	_inherit = 'ple.report.templ'
	
	year = fields.Integer(required=True)
	month = fields.Selection(selection_add=[], required=True)
	
	cash_line_ids = fields.Many2many('account.move.line', 'cash_accounts_rel', string='Movimientos de efectivo', readonly=True)
	bank_line_ids = fields.Many2many('account.move.line', 'bank_accounts_rel', string='Movimientos de banco', readonly=True)	
 
	ple_txt_01 = fields.Text(string='Contenido del TXT 1.1')
	ple_txt_01_binary = fields.Binary(string='TXT 1.1')
	ple_txt_01_filename = fields.Char(string='Nombre del TXT 1.1')
	ple_xls_01_binary = fields.Binary(string='Excel 1.1')
	ple_xls_01_filename = fields.Char(string='Nombre del Excel 1.1')
	ple_txt_02 = fields.Text(string='Contenido del TXT 1.2')
	ple_txt_02_binary = fields.Binary(string='TXT 1.2', readonly=True)
	ple_txt_02_filename = fields.Char(string='Nombre del TXT 1.2')
	ple_xls_02_binary = fields.Binary(string='Excel 1.2', readonly=True)
	ple_xls_02_filename = fields.Char(string='Nombre del Excel 1.2')
	
	def get_default_filename(self, ple_id='010100', tiene_datos=False) :
		name = super().get_default_filename()
		name_dict = {
			'month': str(self.month).rjust(2,'0'),
			'ple_id': ple_id,
		}
		if not tiene_datos:
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
		lines = [
			('company_id','=',self.company_id.id),
			('company_id.partner_id.country_id','=',self.env.ref('base.pe').id), # TODO no domiciliados?
			('date','>=',str(start)),
			('date','<=',str(end)),
			('parent_state','=','posted'),
			('display_type','not in',['line_section','line_note']),
		]
		cash_domain = lines + [('account_id.is_cash_account','=',True)]
		bank_domain = lines + [('account_id.is_bank_account','=',True)]
  
		cash_line_ids = self.env['account.move.line'].search(cash_domain, order='date asc')
		bank_line_ids = self.env['account.move.line'].search(bank_domain, order='date asc')
		self.cash_line_ids = cash_line_ids
		self.bank_line_ids = bank_line_ids
		return res
	
	def generate_report(self) :
		res = super().generate_report()
		lines_to_write_01 = []
		lines_to_write_02 = []
		for move in self.cash_line_ids.sudo():
			m_01 = move.ple_1_1_fields()
			try :
				lines_to_write_01.append('|'.join(m_01))
			except :
				raise UserError('Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_01))
		for move in self.bank_line_ids.sudo():
			m_02 = move.ple_1_2_fields()
			try :
				lines_to_write_02.append('|'.join(m_02))
			except :
				raise UserError('Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_02))
		name_01 = self.get_default_filename(ple_id='010100', tiene_datos=bool(lines_to_write_01))
		lines_to_write_01.append('')
		txt_string_01 = '\r\n'.join(lines_to_write_01)
		dict_to_write = dict()
		if txt_string_01 :
			xlsx_file_base_64 = self._generate_xlsx_base64_bytes(lines_to_write_01, name_01[2:], headers=PLE_1_1_HEADER)
			dict_to_write.update({
				'ple_txt_01': txt_string_01,
				'ple_txt_01_binary': b64encode(txt_string_01.encode()),
				'ple_txt_01_filename': name_01 + '.txt',
				'ple_xls_01_binary': xlsx_file_base_64.encode(),
				'ple_xls_01_filename': name_01 + '.xlsx',
			})
		else :
			dict_to_write.update({
				'ple_txt_01': False,
				'ple_txt_01_binary': False,
				'ple_txt_01_filename': False,
				'ple_xls_01_binary': False,
				'ple_xls_01_filename': False,
			})
		name_02 = self.get_default_filename(ple_id='010200', tiene_datos=bool(lines_to_write_02))
		lines_to_write_02.append('')
		txt_string_02 = '\r\n'.join(lines_to_write_02)
		if txt_string_02 :
			xlsx_file_base_64 = self._generate_xlsx_base64_bytes(lines_to_write_02, name_02[2:], headers=PLE_1_2_HEADER)
			dict_to_write.update({
				'ple_txt_02': txt_string_02,
				'ple_txt_02_binary': b64encode(txt_string_02.encode()),
				'ple_txt_02_filename': name_02 + '.txt',
				'ple_xls_02_binary': xlsx_file_base_64.encode(),
				'ple_xls_02_filename': name_02 + '.xlsx',
			})
		else :
			dict_to_write.update({
				'ple_txt_02': False,
				'ple_txt_02_binary': False,
				'ple_txt_02_filename': False,
				'ple_xls_02_binary': False,
				'ple_xls_02_filename': False,
			})
		dict_to_write.update({
			'date_generated': str(fields.Datetime.now()),
		})
		res = self.write(dict_to_write)
		return res
