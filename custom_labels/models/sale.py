# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_po = fields.Char(string='Customer PO', required=True)
   

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_manuf = fields.Float(string='Quantity Manufactured', store=True, default=0)