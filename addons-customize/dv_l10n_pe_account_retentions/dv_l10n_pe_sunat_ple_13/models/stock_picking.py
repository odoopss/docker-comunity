from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _get_default_operation_type(self):
        return self.env['l10n_pe_edi.table.12'].search([('code', '=', '01')])

    l10n_table_12_operation_type_id = fields.Many2one('l10n_pe_edi.table.12', string='Tipo de Operación', compute='_compute_l10n_table_12_operation_type_id')
    def _compute_l10n_table_12_operation_type_id(self):
        for record in self:
            origin_id = False
            if record.sale_id:
                origin_id = record.sale_id
            elif record.purchase_id:
                origin_id = record.purchase_id
                
            if origin_id:
                l10n_table_12_operation_type_id == self.env['l10n_pe_edi.table.12'].search([('code', '=', '01')])
            elif record.location_dest_id.usage == 'internal': # Entrada
                l10n_table_12_operation_type_id = self.env['l10n_pe_edi.table.12'].search([('code', '=', '21')])
            else: # Salida
                l10n_table_12_operation_type_id = self.env['l10n_pe_edi.table.12'].search([('code', '=', '11')])
            record.l10n_table_12_operation_type_id = l10n_table_12_operation_type_id
            
    def get_account_move_id(self):    
        account_move_id = False
        origin_id = False
        if self.sale_id:
            origin_id = self.sale_id
        elif self.purchase_id:
            origin_id = self.purchase_id
        
        if origin_id and origin_id.invoice_ids:
            account_move_id = self.sale_id.invoice_ids[0]
        return account_move_id

    def get_document_type_code(self):
        if self.l10n_table_12_operation_type_id.code == '01':
            document_type_code = False
            account_move_id = self.get_account_move_id()
            if account_move_id:
                document_type_code = account_move_id.l10n_latam_document_type_id.code
            
        else:
            document_type_code = '00'
        return document_type_code

    def get_account_move_serie(self):
        if self.l10n_table_12_operation_type_id.code == '01':
            account_move_serie = False
            account_move_id = self.get_account_move_id()
            if account_move_id:
                if self.sale_id:
                    account_move_serie = account_move_id.l10n_pe_edi_serie
                if self.purchase_id:
                    account_move_serie = account_move_id.l10n_pe_in_edi_serie
        else:
            account_move_serie = '0'
        return account_move_serie

    def get_account_move_number(self):
        if self.l10n_table_12_operation_type_id.code == '01':
            account_move_number = False
            account_move_id = self.get_account_move_id()
            if account_move_id:
                if self.sale_id:
                    account_move_number = account_move_id.l10n_pe_edi_number

                if self.purchase_id:
                    account_move_number = account_move_id.l10n_pe_in_edi_number
        else:
            account_move_number = '0'
        return account_move_number
