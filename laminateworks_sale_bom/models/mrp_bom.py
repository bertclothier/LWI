# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    total_weight = fields.Float(string='Total Weight', compute='_compute_total_weight')
    bom_sale_id = fields.One2many(comodel_name='sale.order.line', inverse_name='sale_bom', string='Bom Sale Order Line ID')
    total_bom_cost = fields.Float(string='Total Bom Cost',
                                 compute='_compute_total_cost',
                                 readonly=True)
    
    @api.depends('bom_line_ids.product_id')
    def _compute_total_cost(self):
        for bom in self:
            total_cost = 0
            for line in bom.bom_line_ids:
                if bom.bom_line_ids:
                    total_cost += line.product_id.standard_price * line.product_qty
            bom.total_bom_cost = total_cost

    @api.depends('product_qty')
    def _compute_total_weight(self):
        for rec in self:
            quantity = rec.product_qty
            bom_weight = 0
            if rec.bom_line_ids:
                for bom_line in rec.bom_line_ids:
                    bom_weight += bom_line.product_qty * bom_line.weight
            rec.total_weight = quantity * bom_weight

    def laminated_process(self, vals_list):
        values = []
        laminated_group = ['Face', 'Back', 'Core']
        for i in range(len(vals_list['bom_line_ids'])):
            for j in range(len(vals_list['bom_line_ids'][i])):
                if isinstance(vals_list['bom_line_ids'][i][j],dict):
                    values.append(vals_list['bom_line_ids'][i][j]['group'])
        if not all(item in values for item in laminated_group):
            raise ValidationError(_('Must select face, back, and core groups'))

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if 'product_tmpl_id' in vals:
                product_tmpl_id = self.env['product.template'].browse(vals_list['product_tmpl_id'])
                if product_tmpl_id.sale_bom_process == 'Laminated Face':
                    self.laminated_process(vals_list)
        return super(MrpBom, self).create(vals_list)

    @api.model
    def action_cron_archive_bom(self):
        bom_mrp_ids = [rec.bom_id for rec in self.env['mrp.production'].search([('state', '!=', 'done')])]
        for record in self.search([]):
            sale_order = record.env['sale.order'].browse(id.bom_sale_id for id in record)
            if record.code and sale_order and record not in bom_mrp_ids:
                for line in sale_order.id:
                    if (line.qty_delivered == line.product_uom_qty == line.qty_invoiced):
                        record.write({'active': False})
                        break


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    group = fields.Selection([('Face', 'Face'), ('Back', 'Back'),
                            ('Core', 'Core'), ('Pack', 'Pack')],
                            string='Group')
    family = fields.Char(related='product_tmpl_id.family.name',string='Family', readonly=True)
    weight = fields.Float(string='Weight', readonly=True, related='product_tmpl_id.weight')
    uom = fields.Char(string='UoM', readonly=True, related='product_tmpl_id.weight_uom_name')
    mrp_product_bom = fields.Selection(related="bom_id.product_tmpl_id.sale_bom_process",
                                      string="Mrp BoM Process",
                                      store=False)
    