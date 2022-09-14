from odoo import api, fields, models


class TransaksiXLSX(models.Model):
    _name = 'report.benlok.report_transaksi_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, barang):
        
        total_pemasukan = 0
        sheet = workbook.add_worksheet("Daftar Transaksi")
        for i in range (0,7):
            sheet.set_column(i, i, 20)
        bold = workbook.add_format({'bold': True})
        for obj in barang:
            report_name = obj.name
            # One sheet by partner
            r = 1
            c = 0
            sheet.write(0,0,"No. Transaksi", bold)
            sheet.write(0,1,"Tanggal Transaksi", bold)
            sheet.write(0,2,"Konsumen", bold)
            sheet.write(0,3,"Kendaraan", bold)
            sheet.write(0,4,"Mekanik", bold)
            sheet.write(0,5,"Kasir", bold)
            sheet.write(0,6,"Total Pembayaran", bold)
            for obj in barang:
                sheet.write(r, c, obj.name)
                sheet.write(r, c+1, str(obj.tanggal))
                sheet.write(r, c+2, obj.konsumen_id.name)
                sheet.write(r, c+3, obj.nama_kendaraan)
                sheet.write(r, c+4, obj.mekanik_id.name)
                sheet.write(r, c+5, obj.kasir_id.name)
                sheet.write(r, c+6, f'Rp. {obj.total_bayar:,}')
                r+=1
                total_pemasukan += obj.total_bayar
            sheet.write(r,0, f"Total Pemasukan: Rp. {total_pemasukan:,}", bold)
