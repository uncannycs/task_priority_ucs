
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CreateInternalProject(models.TransientModel):
    _name = "create.internal.project"
    _description = "Create Internal Project"

    def create_internal_project(self):
        project = self.env['project.project'].sudo()
        project_ids = project.browse(self.env.context.get('active_ids'))
        project_list = []
        for main_project_id in project_ids:
            existing_child_project_id = project.search([
                ('client_project_id', '=', main_project_id.id),
                ('is_child_project', '=', True)
            ], limit=1)

            if existing_child_project_id:
                raise ValidationError(
                    f"A child project already exists for the project '{main_project_id.name}' (Child Project: {existing_child_project_id.name}).")

            project_id = project.create({
                'name': '%s : %s' % ('UCS', main_project_id.name),
                'client_project_id': main_project_id.id,
                'is_child_project': True,
                'is_internal': False,
                'project_short_code': '%s-%s' % ('UCS', main_project_id.project_short_code),
                'user_id': main_project_id.user_id.id,
                'partner_id': main_project_id.partner_id.id,
                'project_version_id': main_project_id.project_version_id.id,
                'git_url': main_project_id.git_url,
                'production_branch': main_project_id.production_branch,
                'staging_branch': main_project_id.production_branch,
                'team_leader_id': main_project_id.team_leader_id.id,
                'tag_ids': main_project_id.tag_ids,
                'privacy_visibility': 'followers',
                'allocated_hours': main_project_id.allocated_hours,
                'date_start': main_project_id.date_start,
                'date': main_project_id.date
            })
            project_list.append(project_id.id)
            main_project_id.write({
                'is_parent_project': True,
                'is_internal': False
            })

            if main_project_id.task_ids:
                for task in main_project_id.task_ids:
                    child_task_id = task.copy({'project_id': project_id.id,
                               'client_task_id': task.id,
                               'name': task.name,
                               })
                    task.with_context(no_create_task=True).child_task_id = child_task_id.id
                    child_task_id.buffer_cal_task(client_task_id=task)

                    message_ids = self.env['mail.message'].search(
                        [('res_id', '=', task.id), ('model', '=', 'project.task')])
                    for message in message_ids:
                        message.copy({
                            'res_id': child_task_id.id,
                            'model': 'project.task'
                        })

        if len(project_list) == 1:
            return {
                'name': 'Project',
                'type': 'ir.actions.act_window',
                'res_model': 'project.project',
                'view_mode': 'form',
                'res_id': project_list[0],
                'target': 'current',
            }
        else:
            return {
                'name': 'Project',
                'type': 'ir.actions.act_window',
                'res_model': 'project.project',
                'view_mode': 'tree',
                'target': 'new',
            }
