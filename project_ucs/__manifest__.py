# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Uncanny Consulting Services LLP <www.uncannycs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
{
    'name': "Project Custom",
    'author': 'Uncanny Consulting Services LLP',
    'category': 'Project Management',
    'summary': """Project Customization""",
    'license': 'AGPL-3',
    'website': 'http://www.uncannycs.com',
    'description': """
    """,
    'version': '18.0.0.1.0',
    'depends': ['base', 'hr', 'hr_timesheet', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_view.xml',
        'views/project_project_view.xml',
        'views/project_version.xml',
        'views/hr_employee_view.xml',
        'views/project_task_type.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}