from odoo import http, fields
from datetime import datetime, time, timedelta
from odoo.http import request, Response
import json

class MedicalAppointmentController(http.Controller):
    
    @http.route('/api/antrian_umum', type='http', auth='public', methods=['GET'], csrf=False)
    def get_antrian_umum(self, **kwargs):
        try:
            request.env.cr.dbname = 'db_odoo16'
            now = datetime.now() + timedelta(hours=0)

            today_start = fields.Datetime.to_string(datetime.combine(now.date(), datetime.min.time()))
            today_end = fields.Datetime.to_string(datetime.combine(now.date(), datetime.max.time()))


            pemeriksaan_records = request.env['medical.pemeriksaan.perawat.rajal'].sudo().search([
                ('date', '>=', today_start),
                ('date', '<=', today_end),
                ('state', 'in', ['draft', 'panggil_pasien']),
                ('jenis_pasien', '=', 'umum'),
            ], limit=1) 

            pemeriksaan_data = []
            for pemeriksaan in pemeriksaan_records:
                pemeriksaan_data.append({
                    'name': pemeriksaan.name,
                    'patient_name': pemeriksaan.patient_id.name,
                    'sex': pemeriksaan.sex,
                    'no_mr': pemeriksaan.no_mr,
                    'umur': pemeriksaan.umur,
                    'jenis_pasien': pemeriksaan.jenis_pasien,
                    'date': fields.Datetime.to_string(pemeriksaan.date), 
                    'anamnesa': pemeriksaan.anamnesa,
                    'penyakit_pasien': pemeriksaan.penyakit_pasien,
                    'riw_penyakit': pemeriksaan.riw_penyakit,
                    'appointment_id': pemeriksaan.appointment_id.id,
                    'no_appointment': pemeriksaan.appointment_id.slot_waktu.no_seq,
                    'poli': pemeriksaan.poli_id.nama_poli,
                    'state' : pemeriksaan.state
                })

            response = Response(
                json.dumps({
                    'tes_hari_sekarang': str(now),
                    'tes_tanggal_mulai': today_start,
                    'tes_tanggal_selesai': today_end,
                    'status': 'success',
                    'data': pemeriksaan_data
                }),
                content_type='application/json',
                status=200
            )
            response.headers['Access-Control-Allow-Origin'] = 'http://103.31.39.53:8080'
            response.headers['Access-Control-Allow-Methods'] = 'GET'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

        except Exception as e:
            return Response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

    
    @http.route('/api/antrian_jaminan', type='http', auth='public', methods=['GET'], csrf=False)
    def get_antrian_jaminan(self, **kwargs):
        try:
            now = datetime.now() + timedelta(hours=0)

            today_start = fields.Datetime.to_string(datetime.combine(now.date(), datetime.min.time()))
            today_end = fields.Datetime.to_string(datetime.combine(now.date(), datetime.max.time()))

            pemeriksaan_records = request.env['medical.pemeriksaan.perawat.rajal'].sudo().search([
                ('date', '>=', today_start),
                ('date', '<=', today_end),
                ('state', 'in', ['draft', 'panggil_pasien']),
                ('jenis_pasien', '=', 'jaminan'),
            ], limit=1)

            pemeriksaan_data = []
            for pemeriksaan in pemeriksaan_records:
                pemeriksaan_data.append({
                    'name': pemeriksaan.name,
                    'patient_name': pemeriksaan.patient_id.name,
                    'sex': pemeriksaan.sex,
                    'no_mr': pemeriksaan.no_mr,
                    'umur': pemeriksaan.umur,
                    'jenis_pasien': pemeriksaan.jenis_pasien,
                    'date': fields.Datetime.to_string(pemeriksaan.date), 
                    'anamnesa': pemeriksaan.anamnesa,
                    'penyakit_pasien': pemeriksaan.penyakit_pasien,
                    'riw_penyakit': pemeriksaan.riw_penyakit,
                    'appointment_id': pemeriksaan.appointment_id.id,
                    'no_appointment': pemeriksaan.appointment_id.slot_waktu_bpjs.no_seq_bpjs,
                    'poli': pemeriksaan.poli_id.nama_poli,
                    'state' : pemeriksaan.state
                })

            response = Response(
                json.dumps({
                    'tes_hari_sekarang': str(now),
                    'tes_tanggal_mulai': today_start,
                    'tes_tanggal_selesai': today_end,
                    'status': 'success',
                    'data': pemeriksaan_data
                }),
                content_type='application/json',
                status=200
            )
            response.headers['Access-Control-Allow-Origin'] = 'http://103.31.39.53:8080'
            response.headers['Access-Control-Allow-Methods'] = 'GET'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

        except Exception as e:
            return Response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                content_type='application/json',
                status=500
            )

