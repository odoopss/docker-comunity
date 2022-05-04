# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from ...dv_l10n_pe_sunat_ple.models.ple_report import get_last_day
from ...dv_l10n_pe_sunat_ple.models.ple_report import fill_name_data
from ...dv_l10n_pe_sunat_ple.models.ple_report import number_to_ascii_chr
from .ple_headers import PLE_5_1_HEADER, PLE_5_2_HEADER, PLE_5_3_HEADER, PLE_5_4_HEADER
#import base64
from base64 import b64decode, b64encode
import datetime
from io import StringIO, BytesIO
import logging
_logging = logging.getLogger(__name__)


class PLEReport05(models.Model):
    _name = 'ple.report.05'
    _description = 'PLE 05 - Estructura del Libro Diario'
    _inherit = 'ple.report.templ'

    year = fields.Integer(required=True)
    month = fields.Selection(selection_add=[], required=True)

    line_ids = fields.Many2many(
        comodel_name='account.move.line', string='Movimientos', readonly=True)
    account_ids = fields.Many2many(
        comodel_name='account.account', string='Cuentas', required=True)

    ple_txt_01 = fields.Text(string='Contenido del TXT 5.1')
    ple_txt_01_binary = fields.Binary(string='TXT 5.1', readonly=True)
    ple_txt_01_filename = fields.Char(string='Nombre del TXT 5.1')
    ple_xls_01_binary = fields.Binary(string='Excel 5.1', readonly=True)
    ple_xls_01_filename = fields.Char(string='Nombre del Excel 5.1')
    ple_txt_02 = fields.Text(string='Contenido del TXT 5.2')
    ple_txt_02_binary = fields.Binary(string='TXT 5.2', readonly=True)
    ple_txt_02_filename = fields.Char(string='Nombre del TXT 5.2')
    ple_xls_02_binary = fields.Binary(string='Excel 5.2', readonly=True)
    ple_xls_02_filename = fields.Char(string='Nombre del Excel 5.2')
    ple_txt_03 = fields.Text(string='Contenido del TXT 5.3')
    ple_txt_03_binary = fields.Binary(string='TXT 5.3', readonly=True)
    ple_txt_03_filename = fields.Char(string='Nombre del TXT 5.3')
    ple_xls_03_binary = fields.Binary(string='Excel 5.3', readonly=True)
    ple_xls_03_filename = fields.Char(string='Nombre del Excel 5.3')
    ple_txt_04 = fields.Text(string='Contenido del TXT 5.4')
    ple_txt_04_binary = fields.Binary(string='TXT 5.4', readonly=True)
    ple_txt_04_filename = fields.Char(string='Nombre del TXT 5.4')
    ple_xls_04_binary = fields.Binary(string='Excel 5.4', readonly=True)
    ple_xls_04_filename = fields.Char(string='Nombre del Excel 5.4')

    def get_default_filename(self, ple_id='050100', tiene_datos=False):
        name = super().get_default_filename()
        name_dict = {
            'month': str(self.month).rjust(2, '0'),
            'ple_id': ple_id,
        }
        if not tiene_datos:
            name_dict.update({
                'contenido': '0',
            })
        fill_name_data(name_dict)
        name = name % name_dict
        return name

    def update_report(self):
        res = super().update_report()
        start = datetime.date(self.year, int(self.month), 1)
        end = get_last_day(start)
        lines = self.env.ref('base.pe').id
        lines = [
            ('company_id', '=', self.company_id.id),
            ('company_id.partner_id.country_id', '=', lines),
            ('move_id.state', '=', 'posted'),
            ('date', '>=', str(start)),
            ('date', '<=', str(end)),
        ]
        accounts = [
			('company_id', '=', self.company_id.id),
			('deprecated', '=', False),
		]
        lines = self.env[self.line_ids._name].search(lines, order='date asc')
        accounts = self.env['account.account'].search(accounts, order='code asc')
        self.line_ids = lines
        self.account_ids = accounts
        return res

    def generate_report(self):
        res = super().generate_report()
        lines_to_write_1 = []
        lines_to_write_2 = []
        lines_to_write_3 = []
        lines_to_write_4 = []
        for account in self.account_ids.filtered(lambda x: len(x.code) > 2):
            period = f"{self.year}{str(self.month).rjust(2, '0')}01" #Se coloca el dia
            m_3 = account.ple_5_3_fields(period)
            m_4 = account.ple_5_4_fields(period)
            try:
                lines_to_write_3.append('|'.join(m_3))
            except:
                raise UserError(
                    'Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_3))

            try:
                lines_to_write_4.append('|'.join(m_4))
            except:
                raise UserError(
                    'Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_4))

        for move in self.line_ids.sudo():
            m_1 = move.ple_5_1_fields()
            m_2 = move.ple_5_2_fields(m_1)
            try:
                lines_to_write_1.append('|'.join(m_1))
            except:
                raise UserError(
                    'Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_1))
            try:
                lines_to_write_2.append('|'.join(m_2))
            except:
                raise UserError(
                    'Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_1))
                
        name_01 = self.get_default_filename(
            ple_id='050100', tiene_datos=bool(lines_to_write_1))
        lines_to_write_1.append('')
        txt_string_01 = '\r\n'.join(lines_to_write_1)
        dict_to_write = dict()
        if txt_string_01:
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(
                lines_to_write_1, name_01[2:], headers=PLE_5_1_HEADER)
            dict_to_write.update({
                'ple_txt_01': txt_string_01,
                'ple_txt_01_binary': b64encode(txt_string_01.encode()),
                'ple_txt_01_filename': name_01 + '.txt',
                'ple_xls_01_binary': xlsx_file_base_64.encode(),
                'ple_xls_01_filename': name_01 + '.xlsx',
            })
        else:
            dict_to_write.update({
                'ple_txt_01': False,
                'ple_txt_01_binary': False,
                'ple_txt_01_filename': False,
                'ple_xls_01_binary': False,
                'ple_xls_01_filename': False,
            })
        name_03 = self.get_default_filename(
            ple_id='050300', tiene_datos=bool(lines_to_write_3))
        lines_to_write_3.append('')
        txt_string_03 = '\r\n'.join(lines_to_write_3)
        if txt_string_03:
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(
                lines_to_write_3, name_03[2:], headers=PLE_5_3_HEADER)
            dict_to_write.update({
                'ple_txt_03': txt_string_03,
                'ple_txt_03_binary': b64encode(txt_string_03.encode()),
                'ple_txt_03_filename': name_03 + '.txt',
                'ple_xls_03_binary': xlsx_file_base_64.encode(),
                'ple_xls_03_filename': name_03 + '.xlsx',
            })
        else:
            dict_to_write.update({
                'ple_txt_03': False,
                'ple_txt_03_binary': False,
                'ple_txt_03_filename': False,
                'ple_xls_03_binary': False,
                'ple_xls_03_filename': False,
            })
        name_02 = self.get_default_filename(
            ple_id='050200', tiene_datos=bool(lines_to_write_2))
        lines_to_write_2.append('')
        txt_string_02 = '\r\n'.join(lines_to_write_2)
        if txt_string_02:
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(
                lines_to_write_2, name_02[2:], headers=PLE_5_2_HEADER)
            dict_to_write.update({
                'ple_txt_02': txt_string_02,
                'ple_txt_02_binary': b64encode(txt_string_02.encode()),
                'ple_txt_02_filename': name_02 + '.txt',
                'ple_xls_02_binary': xlsx_file_base_64.encode(),
                'ple_xls_02_filename': name_02 + '.xlsx',
            })
        else:
            dict_to_write.update({
                'ple_txt_02': False,
                'ple_txt_02_binary': False,
                'ple_txt_02_filename': False,
                'ple_xls_02_binary': False,
                'ple_xls_02_filename': False,
            })
        name_04 = self.get_default_filename(
            ple_id='050400', tiene_datos=bool(lines_to_write_4))
        lines_to_write_4.append('')
        txt_string_04 = '\r\n'.join(lines_to_write_4)
        if txt_string_04:
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(lines_to_write_4, name_04[2:], headers=PLE_5_4_HEADER)
            dict_to_write.update({
                'ple_txt_04': txt_string_04,
                'ple_txt_04_binary': b64encode(txt_string_04.encode()),
                'ple_txt_04_filename': name_04 + '.txt',
                'ple_xls_04_binary': xlsx_file_base_64.encode(),
                'ple_xls_04_filename': name_04 + '.xlsx',
            })
        else:
            dict_to_write.update({
                'ple_txt_04': False,
                'ple_txt_04_binary': False,
                'ple_txt_04_filename': False,
                'ple_xls_04_binary': False,
                'ple_xls_04_filename': False,
            })
        dict_to_write.update({
            'date_generated': str(fields.Datetime.now()),
        })
        res = self.write(dict_to_write)
        return res
