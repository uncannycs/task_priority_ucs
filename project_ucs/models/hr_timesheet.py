from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    is_billable = fields.Boolean(related="task_id.is_billable")
