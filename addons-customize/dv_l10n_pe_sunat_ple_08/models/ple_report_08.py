# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from ...dv_l10n_pe_sunat_ple.models.ple_report import get_last_day
from ...dv_l10n_pe_sunat_ple.models.ple_report import fill_name_data
from ...dv_l10n_pe_sunat_ple.models.ple_report import number_to_ascii_chr
from .ple_headers import PLE_8_1_HEADERS, PLE_8_2_HEADERS, PLE_8_3_HEADERS
#import base64
from base64 import b64decode, b64encode
import datetime
from io import StringIO, BytesIO
#import pandas
import logging
_logger = logging.getLogger(__name__)


class PLEReport08(models.Model):
    _name = 'ple.report.08'
    _description = 'PLE 08 - Estructura del Registro de Compras'
    _inherit = 'ple.report.templ'

    year = fields.Integer(required=True)
    month = fields.Selection(selection_add=[], required=True)

    bill_ids = fields.Many2many(
        comodel_name='account.move', string='Compras', readonly=True)

    # Normal
    ple_txt_01 = fields.Text(string='Contenido del TXT 8.1')
    ple_txt_01_binary = fields.Binary(string='TXT 8.1')
    ple_txt_01_filename = fields.Char(string='Nombre del TXT 8.1')
    ple_xls_01_binary = fields.Binary(string='Excel 8.1')
    ple_xls_01_filename = fields.Char(string='Nombre del Excel 8.1')

    # No domiciliado
    ple_txt_02 = fields.Text(string='Contenido del TXT 8.2')
    ple_txt_02_binary = fields.Binary(string='TXT 8.2', readonly=True)
    ple_txt_02_filename = fields.Char(string='Nombre del TXT 8.2')
    ple_xls_02_binary = fields.Binary(string='Excel 8.2', readonly=True)
    ple_xls_02_filename = fields.Char(string='Nombre del Excel 8.2')

    # Simplicado
    ple_txt_03 = fields.Text(string='Contenido del TXT 8.3')
    ple_txt_03_binary = fields.Binary(string='TXT 8.3', readonly=True)
    ple_txt_03_filename = fields.Char(string='Nombre del TXT 8.3')
    ple_xls_03_binary = fields.Binary(string='Excel 8.3', readonly=True)
    ple_xls_03_filename = fields.Char(string='Nombre del Excel 8.3')

    documento_compra_ids = fields.Many2many('l10n_latam.document.type', 'ple_report_l10n_latam_id', 'report_id',
                                            'doc_id', string='Documentos a incluir', required=False, domain="[('sub_type', 'in', ['purchase'])]")

    def get_default_filename(self, ple_id='080100', tiene_datos=False):
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
        #current_offset = fields.Datetime.context_timestamp(self, fields.Datetime.now()).utcoffset()
        #start = start - current_offset
        #end = end - current_offset
        doc_type_ids = []
        for reg in self.documento_compra_ids:
            doc_type_ids.append(reg.id)

        bills = self.env.ref('base.pe').id
        bills = [
            ('company_id', '=', self.company_id.id),
            ('company_id.partner_id.country_id', '=', bills),
            ('move_type', 'in', ['in_invoice', 'in_refund']),
            ('state', '=', 'posted'),
            ('l10n_latam_document_type_id.code',
             'not in', ['02', '91', '97', '98']),
            ('date', '>=', str(start)),
            ('date', '<=', str(end)),
        ]
        if self.documento_compra_ids:
            bills.append(('l10n_latam_document_type_id', 'in', doc_type_ids))
        bills = self.env[self.bill_ids._name].search(
            bills, order='date asc, ref asc')
        self.bill_ids = bills
        return res

    def generate_report(self):
        res = super().generate_report()
        lines_to_write_01 = []
        lines_to_write_02 = []
        lines_to_write_03 = []
        bills = self.bill_ids.sudo()
        peru = self.env.ref('base.pe')
        for move in bills:
            m_01 = move.ple_8_1_fields()
            try:
                if move.partner_id.country_id == peru:
                    lines_to_write_01.append('|'.join(m_01))
            except:
                raise UserError(
                    'Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_01))

            m_02 = move.ple_8_2_fields()
            try:
                if move.partner_id.country_id != peru:
                    lines_to_write_02.append('|'.join(m_02))
            except:
                raise UserError(
                    'Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_02))

            m_03 = move.ple_8_3_fields()
            try:
                if move.partner_id.country_id == peru:
                    lines_to_write_03.append('|'.join(m_03))
            except:
                raise UserError(
                    'Error: Datos no cumplen con los parámetros establecidos por SUNAT'+str(m_03))

        name_01 = self.get_default_filename(
            ple_id='080100', tiene_datos=bool(lines_to_write_01))
        lines_to_write_01.append('')
        txt_string_01 = '\r\n'.join(lines_to_write_01)
        dict_to_write = dict()
        if txt_string_01:
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(
                lines_to_write_01, name_01[2:], headers=PLE_8_1_HEADERS)
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

        name_02 = self.get_default_filename(
            ple_id='080200', tiene_datos=bool(lines_to_write_02))
        lines_to_write_02.append('')
        txt_string_02 = '\r\n'.join(lines_to_write_02)
        if txt_string_02:
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(
                lines_to_write_02, name_02[2:], headers=PLE_8_2_HEADERS)
            dict_to_write.update({
                'ple_txt_02': txt_string_02,
                'ple_txt_02_binary': b64encode(txt_string_02.encode()),
                'ple_txt_02_filename': name_02 + '.txt',
                'ple_xls_02_binary': xlsx_file_base_64.encode(),
                'ple_xls_02_filename': name_02 + '.xlsx',
            })
        else:
            txt_string_02 = " "
            dict_to_write.update({
                'ple_txt_02': txt_string_02,
                'ple_txt_02_binary': b64encode(txt_string_02.encode()),
                'ple_txt_02_filename': name_02 + '.txt',
                'ple_xls_02_binary': False,
                'ple_xls_02_filename': False,
            })

        name_03 = self.get_default_filename(
            ple_id='080300', tiene_datos=bool(lines_to_write_03))
        lines_to_write_03.append('')
        txt_string_03 = '\r\n'.join(lines_to_write_03)
        if txt_string_03:
            xlsx_file_base_64 = self._generate_xlsx_base64_bytes(
                lines_to_write_03, name_03[2:], headers=PLE_8_3_HEADERS)
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
        dict_to_write.update({
            'date_generated': str(fields.Datetime.now()),
        })
        res = self.write(dict_to_write)
        return res
