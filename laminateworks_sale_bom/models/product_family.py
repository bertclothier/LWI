# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductFamily(models.Model):
    _name = 'product.family'
    _description = "Product Family"
    _order = 'sequence asc, id asc'

    name = fields.Char(string='Name')
    sequence = fields.Integer(string='Sequence')
