from odoo import api, fields, models
import re
from odoo.exceptions import ValidationError

class Supplier(models.Model):
    _name = 'benlok.supplier'
    _description = 'Supplier Suku Cadang'

    name = fields.Char(string='Name', required=True)
    alamat = fields.Text('Alamat', required=True)
    email = fields.Char(string='Email', required=True)
    tipe_supplier = fields.Selection(
        string='Tipe Supplier', 
        selection=[
            ('engine', 'Engine'), 
            ('electrical', 'Electrical'),
            ('transmission','Transmission'),
            ('suspension','Suspension'),
            ('body','Body')])
    
    sukucadang_ids = fields.One2many(comodel_name='benlok.sukucadang', inverse_name='supplier_id', string='Parts')

    @api.onchange('email')
    def validate_mail(self):
       if self.email:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
        if match == None:
            raise ValidationError('Not a valid Email')