# -*- coding: utf-8 -*-
{
    'name': "academy",
    'description': "Description app academy",
    'application': True,
    'sequence':0,
    'depends': ['base','board'],
    'demo': ['demo/demo.xml', ],
    'data': ['views/menu.xml',
             'views/course_view.xml',
             'views/session_view.xml',
             'views/partner_view.xml',
             'security/ir.model.access.csv',
             'security/academy_groups.xml',
             'security/rules_courses.xml',
             'wizard/creat_attendes_wizard_views.xml',
             'reports/session_report.xml',
             'views/dashboard_view.xml',
            ],
}
