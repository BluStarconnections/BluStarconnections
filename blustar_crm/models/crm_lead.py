# -*- coding: utf-8 -*-

from odoo import fields, models


class PosOrder(models.Model):
    _inherit = 'crm.lead'

    name = fields.Char('Name')

    partner_name = fields.Char(
        'Company Name', tracking=20, index=True,
        compute='_compute_partner_name', readonly=False, store=True,
        help='The name of the future partner company that will be created while converting the lead into opportunity')

    contact_first_name = fields.Char('Prim. First Name', readonly=False, store=True, required=True)
    contact_last_name = fields.Char('Prim. Last Name', readonly=False, store=True, required=True)
    phonetic_spelling = fields.Char('Phonetic/Pronouns')
    function = fields.Char('Title')
    contact_phone = fields.Char('Primary Phone')

    primary_email = fields.Char('Primary Email')

    primary_phone_type = fields.Selection([
        ('Mobile', 'Mobile'),
        ('Direct Dial', 'Direct Dial'), ('Main Line', 'Main Line')], string='Prim Phone Type', store=True)

    secondary_phone_type = fields.Selection([
        ('Mobile', 'Mobile'),
        ('Direct Dial', 'Direct Dial'), ('Main Line', 'Main Line')], string='Sec. Phone Type', store=True)

    secondary_first_name = fields.Char('Sec. First Name')
    secondary_last_name = fields.Char('Sec. Last Name')
    sec_title = fields.Char('Sec. Title')

    secondary_contact_phone = fields.Char('Secondary Phone')
    secondary_email = fields.Char('Secondary Email')

    appt_status = fields.Selection([
        ('Opened', 'Opened'),
        ('Yes', 'Yes'), ('Assigned', 'Assigned'), ('Pending', 'Pending'), ('Reschedule', 'Reschedule'),
        ('Confirm', 'Confirm'), ('Cancel', 'Cancel'), ('Credit', 'Credit'), ('Paid out', 'Paid out'), ('No', 'No')],
        string='Appt Status', store=True, required=True)

    next_appointment = fields.Datetime('Next Appointment')

    appointment_type = fields.Selection([
        ('F2F', 'F2F'),
        ('Webinar', 'Webinar'), ('Phone', 'Phone')],
        string='Appointment Type', store=True, required=True)

    ein = fields.Char('EIN')
    ein_date = fields.Date('EIN Date')
    assets = fields.Float('Assets')
    number_of_participants = fields.Float('Number of Participants')
    fund_manager = fields.Char('Fund Manager', required=True)
    tpa = fields.Char('TPA')

    has_advisor = fields.Char('Has Advisor:')
    area_of_concern = fields.Char('Area of concern')
    surveyor = fields.Char('Last contracted by')
    result_code = fields.Char('Result code')
    financial_advisor = fields.Many2one('res.partner', string='Assigned Advisor')

    date_of_stage_change = fields.Datetime(string='Date of Stage change')
    # check_email = fields.Boolean(string="Check email")
    # check_date = fields.Boolean(string="Check date")
    # check_areacode = fields.Boolean(string="Check area code")
    appt_type_chosen = fields.Boolean(string='Appt type chosen')
    salesperson_changed_to_yourself = fields.Boolean(string='Salesperson changed to yourself')
    info_all_updated = fields.Boolean(string='5500 info all updated')
    area_of_concern_notes = fields.Boolean('Notes added to area of concern')
    notes_logged = fields.Boolean('Notes logged? Notes added to log notes')
    appt_date_time = fields.Boolean('Appt date and time added to calendar')
    appointment_date_time = fields.Boolean('Appointment date and time set')
    address_check = fields.Boolean('Address confirmed')
    first_last_name_check = fields.Boolean('First and Last name in correct fields and grammatically, correct')
    email_check = fields.Boolean('Email confirmed and in email and primary email field')
    change_app_status_scheduled_awaiting = fields.Boolean(
        'Change appt status to yes and move to scheduled awaiting assignment')

    extension = fields.Char(string="Extension")
    area_code = fields.Char(string='Area Code')
    fund_manager_tenure = fields.Char(string='Fund Manager Tenure')
    tpa_tenure = fields.Char(string='TPA Tenure')
    last_note = fields.Char(string='Last note')
