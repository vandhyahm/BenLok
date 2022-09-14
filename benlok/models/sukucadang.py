from odoo import api, fields, models


class SukuCadang(models.Model):
    _name = 'benlok.sukucadang'
    _description = 'Suku Cadang'

    name = fields.Char(string='Nomor Part', required=True)
    deskripsi = fields.Char(string='Dekripsi')
    harga = fields.Integer(string='Harga', required=True)
    stok = fields.Integer(string='Stok')
    
    kendaraan_ids = fields.Many2many(
        string='Kendaraan',
        comodel_name='benlok.kendaraan'
    )
    supplier_id = fields.Many2one(comodel_name='benlok.supplier', string='Supplier')

    
