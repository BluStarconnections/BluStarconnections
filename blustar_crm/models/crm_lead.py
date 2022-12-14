# -*- coding: utf-8 -*-

from odoo import api, fields, models



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
    surveyor = fields.Char('Las contracted by')
    result_code = fields.Char('Result code')
    financial_advisor = fields.Char('Assigned Advisor')


