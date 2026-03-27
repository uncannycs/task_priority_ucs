from odoo import models, fields, api, _
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup
from collections import defaultdict
from odoo import models, api, exceptions
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'
    _description = 'Project Task'

    client_priority = fields.Integer(string='Client Priority', default=10)
    developer_priority = fields.Integer(string='Developer Priority', default=10,)
    wizard_index = fields.Integer(string="index")
    client_priority_bool = fields.Boolean()
    developer_priority_bool = fields.Boolean()
    client_pr = fields.Boolean()
    developer_pr = fields.Boolean()
    sequence_developer = fields.Integer(string="Developer Sequence" ,store =True)
    sequence_client = fields.Integer(string="Client Sequence",store =True)
    dev_priority_readonly = fields.Boolean(compute='_compute_boolean_field',default=False)


    def _compute_boolean_field(self):
        for grp in self:
            if self.env.user.has_group('project_task_syncup_ucs.group_internal_project_admin') or self.env.user.has_group('project_task_syncup_ucs.group_internal_project_lead'):
                grp.dev_priority_readonly = False
            else:
                grp.dev_priority_readonly = True

    @api.onchange('wizard_index')
    def _onchange_developer_index(self):
        for task in self:
            if task.developer_pr:
                task.developer_priority = 110 - (task.wizard_index * 10)
            if task.client_pr:
                task.client_priority = 110 - (task.wizard_index * 10)

    @api.model
    def create(self, values):
        res = super(ProjectTask, self.with_context(no_create_task=True)).create(values)
        if res:
            if values.get('developer_priority') or values.get('client_priority'):
                if values.get('developer_priority'):
                    res.project_id._update_task_order_developer_pr()
                if values.get('client_priority'):
                    res.project_id._update_task_order_client_pr()
            return res

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        if 'developer_priority' in vals or 'client_priority' in vals:
            if 'developer_priority' in vals:
                self.project_id._update_task_order_developer_pr()
            if 'client_priority' in vals:
                self.project_id._update_task_order_client_pr()
        return res
