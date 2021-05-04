# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('converted', 'Converted'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    bom_ids = fields.Many2many('sale.order', compute='_compute_bom_ids')

    @api.depends('order_line.sale_bom')
    def _compute_bom_ids(self):
        for record in self:
            record.bom_ids = record.mapped('order_line.sale_bom.id')
    
    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        for line in res.order_line:
            if line.sale_bom:
                line.sale_bom.code = '{}-{}'.format(res.name, line.number)
        return res

    def write(self, values):
        res = super(SaleOrder, self).write(values)
        for line in self.order_line:
            if line.sale_bom:
                line.sale_bom.code = '{}-{}'.format(self.name, line.number)
        return res

    @api.onchange('order_line')
    def _recompute_order_line(self):
        for line in self.order_line:
            line._compute_get_number()
           
    def related_bom_order(self):
        return {
                'name': _("Bill of Materials"),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'mrp.bom',
                'domain': [('id', 'in', self.bom_ids.ids)],
            }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sale_bom = fields.Many2one('mrp.bom', string='Bill of Material')
    sale_product_bom = fields.Selection(related="product_id.sale_bom_process",
                                        string="Sale BoM Process",
                                        store=False)
    number = fields.Integer(compute='_compute_get_number', store=True)
   
    @api.depends('price_subtotal', 'sale_bom')
    def _compute_margin(self):
        for line in self:
            if line.sale_bom:
                line.margin = line.price_subtotal - (line.sale_bom.total_bom_cost)
                line.margin_percent = line.price_subtotal and line.margin/line.price_subtotal
            else:
                super(SaleOrderLine, line)._compute_margin()

    @api.depends('order_id')
    def _compute_get_number(self):
        for order in self.order_id:
            number = 1
            for line in order.order_line:
                line.number = number
                number += 1

    @api.onchange('sale_bom')
    def _onchange_sale_bom(self):
        for line in self:
            if line.sale_bom:
                string = ''
                for bom_line in line.sale_bom.bom_line_ids:
                    if bom_line.group in ['Face', 'Back', 'Core'] and bom_line.group not in string and bom_line.family:
                        string += bom_line.group + ": " + bom_line.family + "\n"
                if string and string in line.name:
                    continue
                if string:
                    line.name = line.name + "\n" + string
                else:
                    line.name = line.get_sale_order_line_multiline_description_sale(line.product_id)
