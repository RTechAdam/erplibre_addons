from odoo import _, api, fields, models


class DemoDefi(models.Model):
    _name = "demo.defi"
    _inherit = ["mail.activity.mixin", "mail.thread"]
    _description = "demo_defi"

    name = fields.Char()
