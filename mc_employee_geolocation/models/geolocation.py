import logging

import requests as requests

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HrEmplpoyee(models.Model):
    _inherit = 'hr.employee'

    track_location = fields.Boolean('Track Location?')


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    geo_location_check_in = fields.Char('Check In Location')
    geo_location_check_out = fields.Char('Check Out Location')

    def get_geolocation(self):
        try:
            api_key = '4d51404c56a643868e9bf4d1b4079d52'
            response = requests.get('https://ipgeolocation.abstractapi.com/v1/?api_key=%s' % api_key)
            if response.status_code == 200:
                data = response.json()
                _logger.warning(data)
                location_data = {
                    "current_location": data.get("city", '') + ',' + ' ' + data.get(
                        "region", '') + ',' + ' ' + data.get(
                        "country_name", '') + ',' + ' ' + 'lat' + ' ' + str(
                        data.get("latitude", '0.0')) + ',' + ' ' + 'long' + ' ' + str(data.get("longitude", '0.0'))
                }
                return location_data.get('current_location')
            else:
                return 'Api failed to get geo location'
        except:
            return 'Api Error'

    @api.model
    def create(self, vals_list):
        location = self.get_geolocation()
        vals_list['geo_location_check_in'] = location
        return super(HrAttendance, self).create(vals_list)

    def write(self, vals):
        location = self.get_geolocation()
        vals['geo_location_check_out'] = location
        return super(HrAttendance, self).write(vals)
