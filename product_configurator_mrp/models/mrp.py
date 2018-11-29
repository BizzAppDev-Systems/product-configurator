from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def action_config_start(self):
        """Return action to start configuration wizard"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.configurator.mrp',
            'name': "Product Configurator",
            'view_mode': 'form',
            'target': 'new',
            'context': dict(
                self.env.context,
                default_order_id=self.id,
                wizard_model='product.configurator.mrp',
            ),
        }


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    config_ok = fields.Boolean(
        related='product_tmpl_id.config_ok',
    )


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    def _skip_bom_line(self, product):
        """ Control if a BoM line should be produce, can be inherited for add
        custom control. It currently checks that all variant values are in the
        product. """
        if not self.bom_id.config_ok:
            return super(MrpBomLine, self)._skip_bom_line(product=product)

        product_value_ids = set(product.attribute_value_ids.ids)

        for config in self.configuration_ids:
            if set(config.value_ids.ids) <= product_value_ids:
                return True
        return False

    configuration_ids = fields.Many2many(
        comodel_name="mrp.bom.line.configuration",
        inverse_name="bom_line_id",
        string="Configurations"
    )


class MrpBomLineConfiguration(models.Model):
    _name = 'mrp.bom.line.configuration'

    @api.depends('value_ids')
    def _get_configuration_string(self):
        self.name = ' '.join(self.value_ids.mapped('name'))

    name = fields.Char(
        string="Configuration",
        compute="_get_configuration_string",
        store="True"
    )
    bom_line_id = fields.Many2one(
        comodel_name="mrp.bom.line",
        string="Bom Line ID",
        required=True
    )
    product_tmpl_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        compute='_compute_product_attribute_value_ids',
        related='bom_line_id.bom_id.product_tmpl_id.attribute_line_val_ids'
    )
    value_ids = fields.Many2many(
        string='Configuration',
        comodel_name='product.attribute.value',
        domain="[('id', 'in', product_tmpl_value_ids)]"
    )

    @api.constrains('value_ids')
    def validate_configuration(self):
        product_tmpl_id = self.bom_line_id.bom_id.product_tmpl_id.id
        valid = self.env['product.config.session'].validate_configuration(
            value_ids=self.value_ids.ids, product_tmpl_id=product_tmpl_id
        )

        if not valid:
            raise ValidationError(_('Invalid configuration'))
