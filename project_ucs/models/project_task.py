from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    @property
    def _rec_names_search(self):
        return ['name', 'task_code']

    team_leader_id = fields.Many2one("res.users", string="Team Leader", related='project_id.team_leader_id', readonly=False)
    project_version_id = fields.Many2one(related='project_id.project_version_id')
    git_url = fields.Char(string="Github URL", related='project_id.git_url')
    task_code = fields.Char(string="Sequence",readonly=True,copy=False)
    sequence_id = fields.Many2one(related='project_id.sequence_id')
    is_billable = fields.Boolean(related='project_id.is_billable')
    is_planned_hours = fields.Boolean('Is Allocated Hours')
    production_branch = fields.Char(related='project_id.production_branch')
    staging_branch = fields.Char(related='project_id.staging_branch')

    @api.constrains('allocated_hours')
    def _check_values(self):
        for rec in self:
            if rec.is_planned_hours and rec.allocated_hours == 0.0:
                raise ValidationError(_('Allocated Hours should not be zero.'))

    @api.model_create_multi
    def create(self, vals):
        res = super(ProjectTask, self).create(vals)
        res.task_code = self.env['ir.sequence'].sudo().next_by_code(res.sequence_id.code) or _('New')
        return res

    @api.constrains('stage_id')
    def _check_stage_id(self):
        for rec in self:
            if rec.stage_id.is_deadline and not rec.date_deadline:
                raise ValidationError(_('You need to input the Deadline for the project!!'))

    # @api.model
    # def default_get(self, fields):
    #     res = super(ProjectTask, self).default_get(fields)
    #     res.update({
    #         'description': "<p>Project Version:</p>"
    #         "<p>Github URL:</p>"
    #         "<p>Custom Module Name:</p>"
    #         "<p>Branch Name:</p>"
    #     })
