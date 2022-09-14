from odoo import api, fields, models


class Person(models.Model):
    _name = 'benlok.person'
    _description = 'Person'

    foto = fields.Image('Foto')
    name = fields.Char(string='Name', required=True)
    alamat = fields.Text('Alamat', required=True)
    no_telp = fields.Char(string='Nomor Telepon', required=True)


class Konsumen(models.Model):
    _name = 'benlok.konsumen'
    _inherit = 'benlok.person'

    kendaraan_ids = fields.Many2many(comodel_name='benlok.kendaraan', string='Kendaraan')


class Pegawai(models.Model):
    _name = 'benlok.pegawai'
    _inherit = 'benlok.person'

    tgl_masuk = fields.Date(string='Tanggal Masuk')
    jabatan = fields.Selection(
        string='Jabatan', 
        selection=[
            ('mekanik', 'Mekanik'), 
            ('kasir', 'Kasir'),])
    exp = fields.Integer(string='Experience')
    pendapatan = fields.Integer(string='Pendapatan')
