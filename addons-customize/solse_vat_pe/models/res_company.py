# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
	_inherit = 'res.company'

	busqueda_ruc = fields.Selection([('directa', 'Directa'), ('selenium', 'Selenium'), ('apiperu', 'APIPERU')], default="selenium", required=True)
	busqueda_dni = fields.Selection([('directa', 'Directa'), ('selenium', 'Selenium'), ('apiperu', 'APIPERU')], default="selenium", required=True)
	token_apiperu = fields.Char('Token APIPERU', default='')