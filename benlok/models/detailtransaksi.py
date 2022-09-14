from odoo import api, fields, models
from odoo.exceptions import ValidationError

class DetailTransaksi(models.Model):
    _name = 'benlok.detailtransaksi'
    _description = 'Detail Transaksi'

    name = fields.Char(string='Nama')
    deskripsi = fields.Char(string='Deskripsi')
    id_transaksi = fields.Many2one(comodel_name='benlok.transaksi', string='Detail Penjualan', ondelete='cascade')
    qty = fields.Integer(string='Kuantitas')
    id_sukucadang = fields.Many2one(comodel_name='benlok.sukucadang', string='List Suku Cadang')
    harga_satuan = fields.Integer(string='Harga Satuan')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')

    @api.model
    def create(self,vals):
        record = super(DetailTransaksi,self).create(vals)
        if record.qty:
            record.id_sukucadang.stok = record.id_sukucadang.stok - record.qty 
        return record

    @api.depends('qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.id_sukucadang.harga

    @api.onchange('id_sukucadang')
    def _onchange_id_sukucadang(self):
        if(self.id_sukucadang.harga):
            self.harga_satuan = self.id_sukucadang.harga
            self.deskripsi = self.id_sukucadang.deskripsi

    @api.model
    def create(self,vals):
        record = super(DetailTransaksi,self).create(vals)
        if record.qty:
            record.id_sukucadang.stok = record.id_sukucadang.stok - record.qty
        return record

    @api.constrains('qty')
    def _check_available_stock(self):
        for record in self:
            if record.qty <= 0:
                raise ValidationError(f"Jumlah barang harus lebih dari nol!")
            if record.qty > record.id_sukucadang.stok:
                raise ValidationError(f"Stok {record.id_sukucadang.name} hanya tersedia {record.id_sukucadang.stok}")
        
    @api.constrains('id_sukucadang')
    def _part_incompatible(self):
        if self.id_transaksi.kendaraan_id not in self.id_sukucadang.kendaraan_ids:
            raise ValidationError("Suku cadang ini tidak bisa digunakan untuk kendaraan ini!")