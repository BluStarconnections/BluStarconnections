from datetime import datetime

from pytz import timezone

from odoo import models, api, _
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    #  get stage_id from stage name
    def get_stage_id(self, name):
        stage_id = self.env['crm.stage'].sudo().search([('name', '=', name)])
        return stage_id

    # @api.model
    # def create(self, vals_list):
    #     res = super(CrmLead, self).create(vals_list)
    #     external_mail = self.env.ref('BluStar_email_templates.appointment_email_externals')
    #     internal_mail = self.env.ref('BluStar_email_templates.appointment_email_internal')
    #     external_mail.send_mail(res.id, force_send=True)
    #     internal_mail.send_mail(res.id, force_send=True)
    #     return res

    def write(self, vals):
        if 'stage_id' in vals:
            vals['date_of_stage_change'] = datetime.now()
        return super().write(vals)

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.create_uid:
            stage_id = self.stage_id.id
            appointment_remainder_mail = self.env.ref('BluStar_email_templates.appointment_remainder_email_template')
            external_mail = self.env.ref('BluStar_email_templates.appointment_email_externals')
            internal_mail = self.env.ref('BluStar_email_templates.appointment_email_internal')
            if self.stage_id.name.lower() == 'scheduled/waiting to be assigned':
                if self.appt_type_chosen is False \
                        or self.salesperson_changed_to_yourself is False \
                        or self.info_all_updated is False \
                        or self.area_of_concern_notes is False \
                        or self.notes_logged is False \
                        or self.appt_date_time is False \
                        or self.appointment_date_time is False \
                        or self.address_check is False \
                        or self.first_last_name_check is False \
                        or self.email_check is False \
                        or self.change_app_status_scheduled_awaiting is False:
                    raise ValidationError(_("Perform checklist!"))
                else:
                    external_mail.send_mail(self._origin.id, force_send=True)
                    internal_mail.send_mail(self._origin.id, force_send=True)
                    self.stage_id = stage_id
            elif self.stage_id.name.lower() in ('needs confirmed est', 'needs confirmed cst',
                                                'needs confirmed mst', 'needs confirmed pst'):
                appointment_remainder_mail.send_mail(self._origin.id, force_send=True)
                self.stage_id = stage_id

    # cron job method to check lead duration in a certain stage
    # move rec to "appointment needed" stage, if
    # >> it is in stage "voicemail left" from 7 days
    # >> it is in stage "cancel list" or "waiting to be rescheduled" from 60 days
    def check_lead_duration_in_stage(self):
        rec_ids = self.env['crm.lead'].sudo().search(
            [('stage_id.name', 'in', ('Voicemail left', 'Cancel list', 'Waiting to be rescheduled'))])
        user_id = self.env['res.users'].sudo().search([('login', '=', 'csalmon@blustarconnections.com')])
        appointment_stage = self.get_stage_id(name='Appointment Needed')
        for rec in rec_ids:
            if rec.check_email is False or rec.check_date is False or rec.check_areacode is False:
                pass
            elif rec.date_of_stage_change:
                duration = datetime.now() - rec.date_of_stage_change
                if duration.days >= 7:
                    if rec.stage_id.name.lower() == 'voicemail left':
                        rec.stage_id = appointment_stage
                        rec.user_id = user_id if user_id else rec.user_id
                if duration.days >= 60:
                    if rec.stage_id.name.lower() in ('cancel list', 'waiting to be rescheduled'):
                        rec.stage_id = appointment_stage
                        rec.user_id = user_id if user_id else rec.user_id

    # cron job method to check "primary phone" once in a week
    # move records to cancel that does not have "primary contact"
    def check_area_code(self):
        cancel_stage = self.get_stage_id(name='Cancel list')
        rec_ids = self.env['crm.lead'].sudo().search(
            [('stage_id.name', '!=', 'Cancel list'), ('contact_phone', '=', False)])
        for rec in rec_ids:
            if rec.check_email is False or rec.check_date is False or rec.check_areacode is False:
                pass
            else:
                rec.stage_id = cancel_stage

    # convert time to user timezone
    # to use in email templates
    def to_user_timezone(self, my_date_time):
        if my_date_time:
            user_tz = self.env.user.tz or 'utc'
            time_in_user_tz = my_date_time.astimezone(timezone(user_tz)).strftime("%Y-%m-%d %I:%M:%S %p")
            return time_in_user_tz

    # Move "Shadow Records" to "Appointment Needed"
    def move_shadow_records(self):
        stage_id = self.get_stage_id(name='Appointment Needed')
        self.env['crm.lead'].sudo().search([('stage_id.name', '=', 'Shadow Records')]).write({'stage_id': stage_id.id})
