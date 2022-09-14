# -*- coding: utf-8 -*-
from odoo import http, models, fields
from odoo.http import request, route
import json



class Benlok(http.Controller):
    @http.route('/benlok/transaksi', auth='public', method=['GET'])
    def getTransaksi(self, **kw):
        transactions = request.env['benlok.transaksi'].search([])
        trs = []
        for obj in transactions:
            suku=[]
            for i in obj.detail_transaksi_ids:
                suku.append({
                    'kode': i.id_sukucadang.name,
                    'kuantitas' : i.qty,
                    'harga' : i.harga_satuan,
                    'subtotal' : i.subtotal,})
            trs.append({
                'no_transaksi' : obj.name,
                'tanggal' : str(obj.tanggal),
                'konsumen_id' : obj.konsumen_id.name,
                'mekanik_id' : obj.mekanik_id.name,
                'kendaraan_id' : obj.nama_kendaraan,
                'detail_transaksi': suku,
                'total_bayar' : obj.total_bayar
            })
        return json.dumps(trs)

    @route('/illmart/getsupplier', type='http', auth='none')
    def getSupplier(self, **kw):
        suppliers = request.env['illmart.supplier'].search([])
        supplier_json = []
        for supplier in suppliers:
            supplier_json.append({
                'name_perusahaan': supplier.name,
                'alamat':supplier.alamat,
                'no_telp': supplier.no_telp,
            })
        return json.dumps(supplier_json)
    

    @http.route('/benlok/benlok', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/benlok/benlok/objects', auth='public')
    def list(self, **kw):
        return http.request.render('benlok.listing', {
            'root': '/benlok/benlok',
            'objects': http.request.env['benlok.benlok'].search([]),
        })

    @http.route('/benlok/benlok/objects/<model("benlok.benlok"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('benlok.object', {
            'object': obj
        })
