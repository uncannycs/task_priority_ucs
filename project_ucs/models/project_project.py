from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectUCS(models.Model):
    _inherit = "project.project"

    project_short_code = fields.Char(string="Project Code", compute="_compute_project_short_code",inverse="_inverse_project_short_code",store=True,copy=False)
    project_version_id = fields.Many2one("project.version", string="Project Version")
    team_leader_id = fields.Many2one("res.users", string="Team Leader")
    git_url = fields.Char(string="Github URL")
    sequence_id = fields.Many2one('ir.sequence')
    is_billable = fields.Boolean("Is Billable")
    production_branch = fields.Char('Production Branch')
    staging_branch = fields.Char('Staging Branch')

    _sql_constraints = [
        ('code_company_uniq', 'unique (project_short_code,company_id)', 'The code of the project must be unique per company !')
    ]

    @api.depends('name')
    def _compute_project_short_code(self):
        for prj in self:
            if prj.name:
                project_name = prj.name.split(' - ')
                if len(project_name)>1:
                    project_name = project_name[1]
                else:
                    project_name = project_name[0]
                prj.project_short_code = project_name[:3].upper()

    def _inverse_project_short_code(self):
        pass

    @api.constrains('team_leader_id')
    def check_team_leader_id(self):
        for rec in self:
            if rec.team_leader_id and rec.team_leader_id.partner_id:
                mail_follower_id = self.env['mail.followers'].search([('res_model', '=', self._name), ('res_id', '=', rec.id), ('partner_id', '=', rec.team_leader_id.partner_id.id)])

                if not mail_follower_id:
                    self.env['mail.followers'].create({
                        'res_model': self._name,
                        'res_id': rec.id,
                        'partner_id': rec.team_leader_id.partner_id.id
                    })
                # else:
                #     raise ValidationError(
                #         _("The Team Leader or their associated partner is missing. Please ensure both are set."))

    @api.model_create_multi
    def create(self, vals):
        res = super(ProjectUCS, self).create(vals)

        seq_id = self.env['ir.sequence'].sudo().create({
            'name': f"{res.name} sequence",
            'code': res.project_short_code,
            'implementation': 'standard',
            'padding': 3,
            'prefix': f"{res.project_short_code}-",
            'number_increment': 1,
            'number_next_actual': 1,
            'active': True
        })
        res.sequence_id = seq_id.id
        return res

    def write(self,vals):
        res = super(ProjectUCS, self).write(vals)
        for record in self:
            if record.project_short_code:
                if record.sequence_id:
                    record.sequence_id.write({
                        'name':f"{record.name} sequence",
                        'code': record.project_short_code,
                        'prefix': f"{record.project_short_code}-",
                    })
                else:
                    seq_id = self.env['ir.sequence'].sudo().create({
                        'name': f"{record.name} sequence",
                        'code': record.project_short_code,
                        'implementation': 'standard',
                        'padding': 3,
                        'prefix': f"{record.project_short_code}-",
                        'number_increment': 1,
                        'number_next_actual': 1,
                        'active': True
                    })
                    record.sequence_id = seq_id.id
        return res

    # def get_task(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Task',
    #         'view_mode': 'tree,form',
    #         'res_model': 'project.task',
    #         # 'domain': [('display_project_id', '=', True)],
    #         'context': "{'create': False}"
    #     }
