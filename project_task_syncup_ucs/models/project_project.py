# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError


class ProjectProject(models.Model):
    _inherit = 'project.project'


    client_project_id = fields.Many2one('project.project', string='Client Project', readonly=True, store=True)
    is_child_project = fields.Boolean('Is Child Project', readonly=True, store=True)
    is_parent_project = fields.Boolean('Is Parent Project', readonly=True, store=True)
    is_internal = fields.Boolean('Is Internal Project', default=True, readonly=True, store=True)
    buffer_percentage = fields.Float(string="Buffer Hours", widget="percentage", digits=[3, 2], default=300.00)
    buffer_operator = fields.Selection([
        ('add', 'Increase'),
        ('subtract', 'Decrease')
    ], default='add')

    def _get_unique_suffix(self, sequence_code, company_id):
        existing_count = self.env['project.project'].search_count([
            ('project_short_code', 'like', f'{sequence_code}-%'),
            ('company_id', '=', company_id)
        ])
        return str(existing_count + 1)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('project_short_code', _('New')) == _('New'):
                sequence_code = self.env['ir.sequence'].next_by_code('project.project')

                company_id = vals.get('company_id')
                if company_id:
                    project_short_code = f"{sequence_code}-{company_id}"
                else:
                    project_short_code = sequence_code
                existing_project = self.env['project.project'].search([
                    ('project_short_code', '=', project_short_code),
                    ('company_id', '=', company_id)
                ], limit=1)

                if existing_project:
                    suffix = self._get_unique_suffix(sequence_code, company_id)
                    project_short_code = f"{sequence_code}-{company_id}-{suffix}"

                vals['project_short_code'] = project_short_code

        return super(ProjectProject, self).create(vals_list)

    def create_internal_project(self):
        if not self.env.user.has_group('project_task_syncup_ucs.group_internal_project_admin'):
            raise UserError("You do not have permission to access this wizard.")

        return {
            'name': 'Project',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            "view_type": "form",
            'res_model': 'create.internal.project',
            'target': 'new',
            'view_id': self.env.ref('project_task_syncup_ucs.project_create_internal_wizard_view_form').id,
            'context': {'active_id': self.id},
        }