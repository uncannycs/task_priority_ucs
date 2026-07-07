from odoo import models, fields, api

class ProjectVersion(models.Model):
    _name = 'project.version'

    name = fields.Char('Name')
    edition = fields.Selection([('CE', 'Community'), ('EE', 'Enterprise')], string='Edition')

    def name_get(self):
        res = []
        for rec in self:
            if rec.edition == 'CE':
                name = rec.name + ' ' + 'Community'
            if rec.edition == 'EE':
                name = rec.name + ' ' + 'Enterprise'
            res += [(rec.id, name)]
        return res
