from odoo import api, fields, models


class TambahSukucadang(models.TransientModel):
    _name = 'benlok.tambahsukucadang'

    sukucadang_id = fields.Many2one(comodel_name='benlok.sukucadang', string='Suku Cadang', required=True)
    jumlah = fields.Integer(string='Jumlah', required=True)

    def button_tambah_stok(self):
        for record in self:
            self.env['benlok.sukucadang'].search([('id','=',record.sukucadang_id.id)]).write({'stok':record.sukucadang_id.stok+record.jumlah})
