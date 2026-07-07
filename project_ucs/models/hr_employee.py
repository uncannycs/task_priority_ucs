from odoo import api, fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    github = fields.Char(string='Github')

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'
    
    github = fields.Char(related='employee_id.github', string='Github')
