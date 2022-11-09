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
            response = requests.get('https://api64.ipify.org?format=json')
            if response.status_code == 200:
                response_data = response.json()
                _logger.warning(response_data)
                ip_address = response_data["ip"]
                _logger.warning(ip_address)
                ip_response = requests.get(f'https://ipapi.co/{ip_address}/json/')
                if ip_response.status_code == 200:
                    data = ip_response.json()
                    _logger.warning(data)
                    location_data = {
                        "current_location": data.get("city", '') + ',' + ' ' + data.get(
                            "region", '') + ',' + ' ' + data.get(
                            "country_name", '') + ',' + ' ' + 'lat' + ' ' + str(
                            data.get("latitude", '0.0')) + ',' + ' ' + 'long' + ' ' + str(data.get("longitude", '0.0'))
                    }
                    return location_data.get('current_location')
                else:
                    return 'IP address failed to get geo location'
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
