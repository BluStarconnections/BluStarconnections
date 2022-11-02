from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    areacode_ids = fields.Many2many('area.code', 'employee_areacode_rel', 'areacode_id', 'employee_id',
                                    string='Area Codes')


class AreaCodes(models.Model):
    _name = 'area.code'

    name = fields.Char(string='Area code')
