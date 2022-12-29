# -*- coding: utf-8 -*-
{
    'name': 'RPT Smart Integration',
    'category': 'Website',
    'author': "Vraja Technologies",
    'version': '16.2.29.12.2022',
    'summary': """""",
    'description': """""",
    'depends': ['crm'],
    'data': ['security/ir.model.access.csv',
             'views/smart_rpt_configuration.xml',
             'views/res_users.xml',
             'views/crm_lead.xml',
             'views/res_partner.xml'
             ],
    'maintainer': 'Vraja Technologies',
    'website': 'https://www.vrajatechnologies.com',
    'images': [],
    'demo': [],
    'installable': True,
    'live_test_url': 'https://www.vrajatechnologies.com/contactus',
    'application': True,
    'auto_install': False,
    'price': '249',
    'currency': 'EUR',
    'license': 'OPL-1'
}

# version changelog
# 27-Dec-2022 Fix Manifest issues
# 29-Dec-2022 Add fetures for generating customer data and record
