from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    tipe_nakes_id = fields.Many2one('tipe.nakes', string='Tipe Nakes')
