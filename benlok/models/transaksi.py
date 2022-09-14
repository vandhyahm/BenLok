from datetime import date
from email.policy import default
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Transaksi(models.Model):
    _name = 'benlok.transaksi'
    _description = 'Transaksi dalam bengkel'

    def _default_nota_transaksi(self):
        count = len(self.env['benlok.transaksi'].search([]))
        return f'INV{count:05d}'
    
    name = fields.Char(string='Nomor Transaksi', default=_default_nota_transaksi)
    tanggal = fields.Date('Tanggal Transaksi', default=date.today(), required=True)
    konsumen_id = fields.Many2one(comodel_name='benlok.konsumen', string='Konsumen')
    kendaraan_id = fields.Many2one(
        comodel_name='benlok.kendaraan', 
        string='Kendaraan', 
        domain="[('konsumen_ids','=',konsumen_id)]"
    )
    nama_kendaraan = fields.Char(compute='_compute_nama_kendaraan_id', string='Nama Kendaraan', default='')
    mekanik_id = fields.Many2one(comodel_name='benlok.pegawai', string='Mekanik', domain="[('jabatan','=','mekanik')]")
    kasir_id = fields.Many2one(comodel_name='benlok.pegawai', string='Kasir', domain="[('jabatan','=','kasir')]")
    biaya_jasa = fields.Integer(string='Biaya Jasa')
    total_bayar = fields.Integer(compute='_compute_total_bayar',string='Total Pembayaran')
    detail_transaksi_ids = fields.One2many(
        comodel_name='benlok.detailtransaksi', 
        inverse_name='id_transaksi', 
        string='Detail Transaksi') 
    
    state = fields.Selection(
        string='Status', 
        selection=[
            ('create','Creating'),
            ('draft', 'Draft'), 
            ('confirmed', 'Confirmed'),
            ('repair','On Repair'),
            ('done','Done'),
            ('cancel','Cancelled')],
            default = 'create')

    @api.model
    def create(self,vals):
        record = super(Transaksi,self).create(vals)
        record.state = 'draft'
        return record

    def write(self,vals):
        for inst in self:
            a = self.env['benlok.detailtransaksi'].search([('id_transaksi','=',inst.id)])
            print(a)
            for data in a:
                print(f'{str(data.id_sukucadang.name)} qty: {str(data.qty)} stok: {str(data.id_sukucadang.stok)}')
                data.id_sukucadang.stok += data.qty
        record = super(Transaksi,self).write(vals)
        for inst in self:
            b = self.env['benlok.detailtransaksi'].search([('id_transaksi','=',inst.id)])
            print(b)
            for new_data in b:
                if new_data in a:
                    print(f'{str(new_data.id_sukucadang.name)} qty: {str(new_data.qty)} stok: {str(new_data.id_sukucadang.stok)}')
                    new_data.id_sukucadang.stok -= new_data.qty
        return record

    def action_confirm(self):
        self.write({'state':'confirmed'})
    
    def action_repair(self):
        self.write({'state':'repair'})

    def action_done(self):
        self.write({'state':'done'})
        self.env['benlok.pegawai'].search([('id','=',self.mekanik_id.id)]).write({'exp' : self.mekanik_id.exp + 1})
        self.env['benlok.pegawai'].search([('id','=',self.kasir_id.id)]).write({'exp' : self.kasir_id.exp + 1})
        if self.mekanik_id.exp == 10000:
            self.mekanik_id.pendapatan += 1000000
        if self.mekanik_id.exp == 20000:
            self.mekanik_id.pendapatan += 1500000
        if self.mekanik_id.exp == 30000:
            self.mekanik_id.pendapatan += 2000000

        if self.kasir_id.exp == 10000:
            self.kasir_id.pendapatan += 1000000
        if self.kasir_id.exp == 20000:
            self.kasir_id.pendapatan += 1500000
        if self.kasir_id.exp == 30000:
            self.kasir_id.pendapatan += 2000000
    
    def action_cancel(self):
        self.write({'state':'cancel'})

    @api.depends('detail_transaksi_ids')
    def _compute_total_bayar(self):
        for rec in self:
            a = self.env['benlok.detailtransaksi'].search([('id_transaksi','=',rec.id)]).mapped('subtotal')
            rec.total_bayar = sum(a) + rec.biaya_jasa

    @api.depends('kendaraan_id')
    def _compute_nama_kendaraan_id(self):
        for rec in self:
            rec.nama_kendaraan = f'{rec.kendaraan_id.merk} {rec.kendaraan_id.tipe} {rec.kendaraan_id.tahun}'

    @api.ondelete(at_uninstall=False)
    def __ondelete_transaksi(self):
        sales = []
        if self.detail_transaksi_ids:
            for line in self:
                sales = self.env['benlok.detailtransaksi'].search([('id_transaksi','=',line.id)])
        for ob in sales:
            ob.id_sukucadang.stok += ob.qty

    @api.constrains('name')
    def _unique_name(self):
        name_counts = self.search_count([('name', '=', self.name), ('id', '!=', self.id)])
        print(name_counts)
        if name_counts > 0:
            raise ValidationError("Nomor transaksi harus unik!")
        
