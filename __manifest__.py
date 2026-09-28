{
    'name': "App Onee",
    'author': "Ibrahem Issa",
    'category': "Uncategorized",
    'version': '19.0.0.1.0',
    'depends': ['base','account','sale','mail','contacts'],
    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/baes_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'views/property_history_view.xml',
        'views/account_view.xml',
        'wizard/change_state_wizard_view.xml',
        'reports/property_report.xml',

    ],
    'assets':{
        'web.report_assets_common':['app_onee/static/crs/fonts.css'],

    },

    'application': True,
    'installable': True,
}