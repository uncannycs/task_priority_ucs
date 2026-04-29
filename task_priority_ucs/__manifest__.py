# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Uncanny Consulting Services LLP
#    Copyright (C) 2023 Uncanny Consulting Services LLP (<https://uncannycs.com>).
#
##############################################################################
{
    "name": "Task Priority UCS",
    'version': '18.0.0.1.1',
    "website": "https://uncannycs.com",
    "author": "Uncanny Consulting Services LLP",
    "maintainers": "Uncanny Consulting Services LLP",
    "license": "Other proprietary",
    "category": "Services/Project",
    "summary": "Task Priority UCS",
    "description": """This module is designed to assign task priority""",
    "depends": [
        'project',
        'project_task_syncup_ucs',
        'mail',
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task_inherit_view.xml",
        "views/task_priority_view.xml",
        "wizard/assign_priority.xml",
    ],

    "application": False,
    "installable": True,
    "auto_install": False,
    "images": ["static/description/banner.png"],
    "price":10.00,
    "currency":'USD',
}
