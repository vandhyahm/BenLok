# -*- coding: utf-8 -*-
{
    'name': "BenLok",

    'summary': """
        BenLok (Bengkel Lokal) merupakan suatu sistem Enterprise Resource Planning untuk usaha 
        bengkel lokal.""",

    'description': """
        Long description of module's purpose
    """,

    'sequence': 0,

    'author': "Arllivandhya Dani",
    'website': "https://github.com/vandhyahm",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'ERP',
    'application': True,
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/kendaraan_view.xml',
        'wizardo/tambah_sukucadang_wizard_view.xml',
        'views/sukucadang_view.xml',
        'views/person_view.xml',
        'views/konsumen_view.xml',
        'views/pegawai_view.xml',
        'views/supplier_view.xml',
        'views/transaksi_view.xml',
        'report/report.xml',
        'report/print_nota_transaksi.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
