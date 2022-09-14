from odoo import api, fields, models


class Kendaraan(models.Model):
    _name = 'benlok.kendaraan'
    _description = 'Model sebuah kendaraan'

    name = fields.Char(string='Kode Chassis', required=True)
    jenis = fields.Selection(string='Jenis', 
            selection=[
                ('sedan', 'Sedan'), 
                ('suv', 'SUV'),
                ('mpv','MPV'),
                ('smol','City Car'),
                ('sport','Sport'),])
    merk = fields.Char(string='Merk', required=True)
    tipe = fields.Char(string='Tipe', required=True)
    sukucadang_ids = fields.Many2many(comodel_name='benlok.sukucadang', string='Suku Cadang')
    konsumen_ids = fields.Many2many(comodel_name='benlok.konsumen', string='Pemilik')

    def get_years(): 
        year_list = [] 
        for i in range(1900, 2022): 
            year_list.append(((str(i)),(str(i)))) 
        return year_list
    tahun = fields.Selection(selection=get_years(), string='Tahun')

    
    
    
