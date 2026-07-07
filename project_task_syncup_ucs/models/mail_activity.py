from odoo import models, fields, _
from datetime import datetime, timedelta


class MailActivity(models.Model):
    _name = 'mail.activity'
    _inherit = 'mail.activity'

    user_id = fields.Many2one('res.users', string='Assigned to')
    estimated_hours = fields.Float("Estimated Hours", tracking=True)
    date_deadline = fields.Date(string='Deadline', default=lambda self: (datetime.now() + timedelta(days=1)).date())
