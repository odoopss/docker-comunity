from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    l10n_pe_edi_table_13_id = fields.Many2one('l10n_pe_edi.table.13', string='Código catálogo de existencias')
    
    @api.model
    def _get_codigo_osce(self):
        return self.env['pe.datas'].get_selection("PE.CPE.CATALOG25")
    
    pe_code_osce = fields.Selection('_get_codigo_osce', 'Código existencia OSCE')