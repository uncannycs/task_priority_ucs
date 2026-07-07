# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


class ProjectTask(models.Model):
    _inherit = 'project.task'

    client_task_id = fields.Many2one('project.task', string='Parent Task')
    is_created = fields.Boolean(default=False)
    child_task_id = fields.Many2one('project.task', store=True, string='Child Task')
    allocated_hours = fields.Float("Initially Planned Hours", tracking=True)

    @property
    def SELF_WRITABLE_FIELDS(self):
        res = super().SELF_WRITABLE_FIELDS
        res.update({'description', 'client_task_id'})
        return res

    def buffer_cal_task(self, client_task_id=False):
        if not client_task_id:
            return False
        if client_task_id.project_id.buffer_percentage :
            child_estimated_hours = (client_task_id.allocated_hours * client_task_id.project_id.buffer_percentage) / 100.00
            allocated_hours = client_task_id.allocated_hours + child_estimated_hours * (client_task_id.project_id.buffer_operator == 'add' and 1 or -1)
            return allocated_hours
        return client_task_id.allocated_hours

    @api.model
    def create(self, values):
        res = super(ProjectTask, self.with_context(no_create_task=True)).create(values)
        for rec in res.sudo().filtered(lambda x: x.project_id.client_project_id):
            rec.allocated_hours = rec.buffer_cal_task()

        if res:
            if res.project_id.user_id:
                res.user_ids = [(4, res.project_id.user_id.id)]
            if not res.is_created:
                for rec in res.filtered(lambda x: not x.project_id.client_project_id):
                    child_project_ids = self.env['project.project'].sudo().search([
                        ('client_project_id', '=', rec.project_id.id),
                        ('is_child_project', '=', True)
                    ])

                    ucs_task_id = self.env['project.task']
                    if rec.parent_id:
                        ucs_task_id = self.env['project.task'].search([('client_task_id', '=', rec.parent_id.id)])

                    if ucs_task_id and res.parent_id:
                        for child_project in child_project_ids:
                            child_task_id = rec.copy({
                                'project_id': child_project.id,
                                'client_task_id': rec.id,
                                'name': f"{rec.name} [{rec.task_code}]",
                                'parent_id': ucs_task_id.id
                            })
                            res.with_context(no_create_task=True).child_task_id = child_task_id.id
                            child_task_id.buffer_cal_task(client_task_id=rec)
                    elif child_project_ids:
                        for child_project in child_project_ids:
                            child_task_id = rec.copy({
                                'project_id': child_project.id,
                                'client_task_id': rec.id,
                                'name': f"{rec.name} [{rec.task_code}]",
                            })
                            res.with_context(no_create_task=True).child_task_id = child_task_id.id
                            child_task_id.allocated_hours = self.buffer_cal_task(client_task_id=rec)
                res.is_created = True

            for task in res:
                for assignee in task.user_ids:
                    activity_vals = {
                        'res_id': task.id,
                        'res_model_id': self.env.ref('project.model_project_task').id,
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'summary': f"Task '{task.name}' assigned to {assignee.name} - Estimated Hours: {task.allocated_hours}",
                        'user_id': assignee.id,
                        'estimated_hours': task.allocated_hours
                    }
                    self.env['mail.activity'].create(activity_vals)
        return res

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        if not self.env.context.get('no_create_task'):
            data_dict = vals.copy()
            [data_dict.pop(key, False) for key in
             ['project_id', 'sequence_developer', 'sequence_client', 'timesheet_ids', 'sale_line_id', 'child_ids']]

            if self.child_task_id:
                if 'description' in vals:
                    task_ids = self.child_task_id + self
                else:
                    task_ids = self.child_task_id
                if 'allocated_hours' in data_dict:
                    data_dict['allocated_hours'] = self.buffer_cal_task(client_task_id=self)

                task_ids.sudo().with_context(no_create_task=True).write(data_dict)


            if 'description' in vals:
                for rec in self.sudo():
                    clean_description = self._clean_html_tags(vals.get('description'))
                    rec.sudo().message_post(body=clean_description)

            if 'user_ids' in vals:
                for res in self.sudo():
                    if len(res.user_ids) > 0:
                        for user in res.user_ids:
                            activity_exists = self.env['mail.activity'].search(
                                [('res_id', '=', res.id), ('user_id', '=', user.id)], limit=1)
                            if not activity_exists:
                                activity = self.env['mail.activity'].create({
                                    'res_id': res.id,
                                    'res_model_id': self.env.ref('project.model_project_task').id,
                                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                                    'summary': f"Task '{res.name}' assigned to {user.name} - Estimated Hours: {res.allocated_hours}",
                                    'user_id': user.id,
                                    'estimated_hours': res.allocated_hours
                                })
        return res

    def _clean_html_tags(self, html_text):
        clean_text = re.sub('<[^<]+?>', '', html_text)
        return clean_text

    def unlink(self):
        for record in self:
            if record.child_task_id:
                record.child_task_id.unlink()
        return super(ProjectTask, self).unlink()

    def action_update_stage(self):
        for rec in self:
            if rec.client_task_id:
                rec.client_task_id.stage_id = rec.stage_id
        return {
            'effect': {
                'fadeout': 'medium',
                'message': 'Stage updated successfully!',
                'type': 'rainbow_man',
            }
        }