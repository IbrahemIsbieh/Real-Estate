{
    'name': "App Onee",
    'author': "Ibrahem Issa",
    'category': "Uncategorized",
    'version': '19.0.0.1.0',
    'depends': ['base','account','sale','mail','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/baes_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',


    ],

    'application': True,
    'installable': True,
}