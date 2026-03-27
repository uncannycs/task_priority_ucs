from odoo import models, fields, api
from datetime import datetime, date,timedelta


class ProjectProject(models.Model):
    _inherit = 'project.project'


    def _update_task_order_developer_pr(self):
        sorted_tasks = self.env['project.task'].search([], order='developer_priority desc')
        order_developer = 0
        for task in sorted_tasks:
            order_developer += 1
            task.sequence_developer = order_developer

    def _update_task_order_client_pr(self):
        sorted_tasks = self.env['project.task'].search([], order='client_priority desc')
        order_client = 0
        for task in sorted_tasks:
            order_client += 1
            task.sequence_client = order_client

