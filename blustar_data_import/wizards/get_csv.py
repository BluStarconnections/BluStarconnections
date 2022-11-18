import base64
import datetime
import math
import os

import pandas as pd

from odoo import fields, models


class WizardGetFile(models.TransientModel):
    _name = "blustar.import.csv.wizard"
    _description = 'wizard to import csv data'

    model_choices = [('crm', 'CRM')]
    csv_file = fields.Binary('Upload CSV', required=True)
    model_name = fields.Selection(model_choices, 'Model Name')

    # On click of import button on wizard
    # and import the csv file in that model
    def import_csv(self):
        file = base64.b64decode(self.csv_file)
        file_string = file.decode('unicode_escape')
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(cur_dir, "demofile2.csv")

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(file_string)

        df = pd.read_csv(file_name, error_bad_lines=False)
        for date, row in df.T.iteritems():
            if self.model_name == 'crm':
                self.import_blustar_crm_data(row)
            else:
                pass

    def check_is_nan(self, val):
        try:
            math.isnan(val)
            return True
        except:
            return False

    def get_date_obj_from_string(self, val):
        try:
            return datetime.datetime.strptime(val, '%m/%d/%Y')
        except:
            return None

    def import_blustar_crm_data(self, row):
        opportunity_name = row['Company'] if 'Company' in row and self.check_is_nan(row['Company']) is False else ''
        existing_rec = self.env['crm.lead'].sudo().search([('name', '=', opportunity_name)])
        email = row['Email'] if 'Email' in row and self.check_is_nan(row['Email']) is False else None
        phone = row['Phone'] if 'Phone' in row and self.check_is_nan(row['Phone']) is False else None

        contact_name = row['Contact'] if 'Contact' in row and self.check_is_nan(row['Contact']) is False else None
        if contact_name is not None:
            name_list = contact_name.split()
            if len(name_list) == 2:
                firstname = name_list[0]
                lastname = name_list[1]
            elif len(name_list) == 3:
                firstname = str(name_list[0]) + '' + str(name_list[1])
                lastname = name_list[2]
            else:
                firstname = contact_name
                lastname = existing_rec[0].contact_last_name if existing_rec else ''
        else:
            firstname = existing_rec[0].contact_first_name if existing_rec else ''
            lastname = existing_rec[0].contact_last_name if existing_rec else ''

        appt_date = row['Date of Appt'] if 'Date of Appt' in row and self.check_is_nan(
            row['Date of Appt']) is False else ''

        caller_name = row['Caller'] if 'Caller' in row and self.check_is_nan(row['Caller']) is False else None
        if caller_name is not None:
            caller_id = self.env['res.users'].sudo().search([('name', '=', caller_name)])
            if caller_id:
                user_id = caller_id[0].id
            else:
                user_id = existing_rec[0].user_id.id if existing_rec else None
        else:
            user_id = existing_rec[0].user_id.id if existing_rec else None

        state_code = row['State'] if 'State' in row and self.check_is_nan(row['State']) is False else None
        if state_code is not None:
            state = self.env['res.country.state'].sudo().search([('code', '=', state_code)])
            if state:
                state_id = state[0].id
            else:
                state_id = None
        else:
            state_id = None

        reason = row['Reason'] if 'Reason' in row and self.check_is_nan(row['Reason']) is False else None
        result = row['Result'] if 'Result' in row and self.check_is_nan(row['Result']) is False else None

        data_dict = {
            'name': opportunity_name,
            'contact_first_name': firstname,
            'contact_last_name': lastname,
            'primary_email': email,
            'contact_phone': phone,
            'next_appointment': self.get_date_obj_from_string(appt_date),
            'user_id': user_id,
            'state_id': state_id,
            'description': reason,
            'result_code': result,
            'fund_manager': existing_rec[0].fund_manager if existing_rec else '',
        }

        if existing_rec:
            existing_rec[0].write(data_dict)
        else:
            self.env['crm.lead'].sudo().create(data_dict)
