# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_create_internal_project = fields.Boolean(string="Create Internal Project")


    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        icpSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            is_create_internal_project=icpSudo.get_param('project_task_syncup_ucs.is_create_internal_project'),
        )
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        icpSudo = self.env['ir.config_parameter'].sudo()
        icpSudo.set_param("project_task_syncup_ucs.is_create_internal_project", self.is_create_internal_project)
        return res
