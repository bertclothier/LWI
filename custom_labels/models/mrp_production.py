# -*- coding: utf-8 -*-

from odoo import fields, models, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    sale_line_id = fields.Many2one(comodel_name='sale.order.line', string='Sale Line ID', compute='_get_sale_order_info')
    sale_id = fields.Many2one(comodel_name='sale.order', string='Sale Order ID' ,compute='_get_sale_order_info')
    customer_po = fields.Char(string='Customer PO', compute='_set_caps')
    product_description = fields.Char(string='Product Description', compute='_set_caps')
    qty_manuf = fields.Float(string='Quantity Manufactured', compute='_compute_qty_manuf')
    
    @api.depends('sale_line_id.qty_manuf')
    def _compute_qty_manuf(self):
        for production in self:
            production.qty_manuf = production.sale_line_id.qty_manuf

    def button_mark_done(self):
        self.ensure_one()
        if not self.env.context.get('button_mark_done_production_ids'):
            self = self.with_context(button_mark_done_production_ids=self.ids)
        res = self._pre_button_mark_done()
        if res is not True:
            return res

        for production in self:
            if production.state in ('progress', 'to_close'):
                production.sale_line_id.qty_manuf += production.qty_producing

        return super(MrpProduction, self).button_mark_done()

    @api.depends('sale_line_id')
    def _set_caps(self):
        self.ensure_one()
        self.customer_po = self.sale_id.customer_po.upper()
        self.product_description = self.sale_line_id.name.upper()

    @api.model
    def _get_sale_order_info(self):
        for production in self:
            if production.backorder_sequence <= 1:
                production.sale_line_id = production.move_dest_ids.sale_line_id
            else:
                original_prod = self.env['mrp.production'].search([('name', '=', self.name.split('-')[0] + '-001')])
                production.sale_line_id = original_prod.sale_line_id
            production.sale_id = production.sale_line_id.order_id

    def print_labels(self):
        return self.env.ref('mrp.label_manufacture_template').report_action(self)



class MrpProductionBackorder(models.TransientModel):
    _inherit = 'mrp.production.backorder'

    def action_backorder(self):
        super(MrpProductionBackorder, self).action_backorder()
        return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'mrp.production',
                    'views': [[self.env.ref('mrp.mrp_production_form_view').id, 'form']],
                    'res_id': self.mrp_production_ids[0].id,
                    'target': 'main',
                }
