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
    "name": "Project Task Sync-up UCS",
    'version': '18.0.0.1.0',
    "website": "https://uncannycs.com",
    "author": "Uncanny Consulting Services LLP",
    "maintainers": "Uncanny Consulting Services LLP",
    "license": "Other proprietary",
    "category": "Services/Project",
    "summary": "Project Task Sync-up UCS",
    "description": """This module is designed to sync a project with its child projects. It can automatically create tasks in a child project from the parent project. """,
    "depends": [
        'project',
        'project_ucs',
        'mail',
    ],
    "data": [
        "security/internal_security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/res_config_setting_inherit_view.xml",
        "wizard/create_internal_project_view.xml",
        "views/project_task_inherit_view.xml",
        "views/project_project_view.xml",
    ],

    "application": False,
    "installable": True,
    "auto_install": False,
    "images": ["static/description/banner.gif"],
}
