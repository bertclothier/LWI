# -*- coding: utf-8 -*-

from odoo import models

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_procurement_values(self):
        self.ensure_one()
        values = super(StockMove, self)._prepare_procurement_values()
        values['sale_line_id'] = self.sale_line_id.id if self.sale_line_id else False
        return values