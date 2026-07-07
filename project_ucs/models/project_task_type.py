from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    is_deadline = fields.Boolean()
