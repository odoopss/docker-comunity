# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from ...dv_l10n_pe_sunat_ple.models.ple_report import get_last_day
from ...dv_l10n_pe_sunat_ple.models.ple_report import fill_name_data
from ...dv_l10n_pe_sunat_ple.models.ple_report import number_to_ascii_chr
from .ple_headers import PLE_14_1_HEADER, PLE_14_2_HEADER

from base64 import b64decode, b64encode
import datetime
from io import StringIO, BytesIO
import logging
_logging = logging.getLogger(__name__)

class PLEReport14(models.Model) :
	_name = 'ple.report.14'
	_description = 'PLE 14 - Estructura del Registro de Ventas'
	_inherit = 'ple.report.templ'
	
	year = fields.Integer(required=True)
	month = fields.Selection(selection_add=[], required=True)
	
	invoice_ids = fields.Many2many(comodel_name='account.move', string='Ventas', readonly=True)
	
	ple_txt_01 = fields.Text(string='Contenido del TXT 14.1')
	ple_txt_01_binary = fields.Binary(string='TXT 14.1')
	ple_txt_01_filename = fields.Char(string='Nombre del TXT 14.1')
	ple_xls_01_binary = fields.Binary(string='Excel 14.1')
	ple_xls_01_filename = fields.Char(string='Nombre del Excel 14.1')
	ple_txt_02 = fields.Text(string='Contenido del TXT 14.2')
	ple_txt_02_binary = fields.Binary(string='TXT 14.2', readonly=True)
	ple_txt_02_filename = fields.Char(string='Nombre del TXT 14.2')
	ple_xls_02_binary = fields.Binary(string='Excel 14.2', readonly=True)
	ple_xls_02_filename = fields.Char(string='Nombre del Excel 14.2')
	
	def get_default_filename(self, ple_id='140100', tiene_datos=False) :
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
		invoices = self.env.ref('base.pe').id
		invoices = [
			('company_id','=',self.company_id.id),
			('company_id.partner_id.country_id','=',invoices),
			('move_type','in',['out_invoice','out_refund']),
			('state','=','posted'),
			('invoice_date','>=',str(start)),
			('invoice_date','<=',str(end)),
		]
		invoices = self.env[self.invoice_ids._name].search(invoices, order='invoice_date asc, name asc')
		self.invoice_ids = invoices
		return res
	
	def generate_report(self) :
		res = super().generate_report()
		lines_to_write_1 = []
		lines_to_write_2 = []
		invoices = self.invoice_ids.sudo()
		for move in invoices:
			m_1 = move.ple_14_1_fields()
			try :
				lines_to_write_1.append('|'.join(m_1))
			except :
				raise UserError('Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_1))
				
			m_2 = move.ple_14_2_fields()
			try :
				lines_to_write_2.append('|'.join(m_2))
			except :
				raise UserError('Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_2))
		
		name_01 = self.get_default_filename(ple_id='140100', tiene_datos=bool(lines_to_write_1))
		lines_to_write_1.append('')
		txt_string_01 = '\r\n'.join(lines_to_write_1)
		dict_to_write = dict()
		if txt_string_01 :
			xlsx_file_base_64 = self._generate_xlsx_base64_bytes(lines_to_write_1, name_01[2:], headers= PLE_14_1_HEADER)
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
		name_02 = self.get_default_filename(ple_id='140200', tiene_datos=bool(lines_to_write_2))
		lines_to_write_2.append('')
		txt_string_02 = '\r\n'.join(lines_to_write_2)
		if txt_string_02 :
			xlsx_file_base_64 = self._generate_xlsx_base64_bytes(lines_to_write_2, name_02[2:], headers= PLE_14_2_HEADER)
   		
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
