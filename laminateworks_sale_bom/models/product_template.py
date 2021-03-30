# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    family = fields.Many2one('product.family', string='Family')
    sale_bom_process = fields.Selection([('Laminated Face', 'Laminated Face'), 
                                        ('Part', 'Part')], 
                                        string='Sales BoM Process', store=True)