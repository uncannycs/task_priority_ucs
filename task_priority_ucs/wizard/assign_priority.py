from odoo import api, fields, models


class AssignPriority(models.TransientModel):
    _name = "assign.priority"
    _description = "Assign Priority"

    task_ids = fields.Many2many('project.task', string='Task')
    index = fields.Integer(string='Index',store=True)
    client_priority_bool = fields.Boolean(string="Client Priority")
    developer_priority_bool = fields.Boolean(string="Developer Priority")

    @api.model
    def default_get(self, fields):
        res = super(AssignPriority, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', [])
        task_values = []
        for index, task_id in enumerate(active_ids, start=1):
            task_values.append((4, task_id, {'index': index}))
            task = self.env['project.task'].browse(task_id)
            task.wizard_index = index
        res['task_ids'] = task_values

        return res

    @api.onchange('client_priority_bool')
    def _onchange_client_bool(self):
        tasks = self.env['project.task'].search([])
        for task in tasks:
            task.client_pr = self.client_priority_bool


    @api.onchange('developer_priority_bool')
    def _onchange_developer_bool(self):
        tasks = self.env['project.task'].search([])
        for task in tasks:
            task.developer_pr = self.developer_priority_bool

    def action_assign_priority(self):
        pass

