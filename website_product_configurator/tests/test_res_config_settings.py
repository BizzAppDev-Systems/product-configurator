from odoo.tests.common import TransactionCase


class TestResConfigSettings(TransactionCase):
    def test_res_config_settings(self):
        ResConfigObj = self.env["res.config.settings"]
        res_config = ResConfigObj.create(
            {
                "website_tmpl_id": self.env.ref(
                    "website_product_configurator.config_form_base"
                ).id,
            }
        )
        self.assertTrue(
            res_config,
            "Failed to create ResConfigSettings with the website template.",
        )
        self.assertEqual(
            res_config.website_tmpl_id,
            self.env.ref("website_product_configurator.config_form_base"),
        )
        res_config_select = ResConfigObj.create(
            {
                "website_tmpl_id": self.env.ref(
                    "website_product_configurator.config_form_select"
                ).id,
            }
        )
        self.assertTrue(
            res_config_select,
            "Failed to create ResConfigSettings with the website template.",
        )
        self.assertEqual(
            res_config_select.website_tmpl_id,
            self.env.ref("website_product_configurator.config_form_select"),
        )
