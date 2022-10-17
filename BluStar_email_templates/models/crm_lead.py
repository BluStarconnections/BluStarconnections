from datetime import datetime

from odoo import models, api, _
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def get_stage_id(self, name):
        stage_id = self.env['crm.stage'].sudo().search([('name', '=', name)])
        return stage_id

    @api.model
    def create(self, vals_list):
        res = super(CrmLead, self).create(vals_list)
        external_mail = self.env.ref('BluStar_email_templates.appointment_email_externals')
        internal_mail = self.env.ref('BluStar_email_templates.appointment_email_internal')
        external_mail.send_mail(res.id, force_send=True)
        internal_mail.send_mail(res.id, force_send=True)
        return res

    def write(self, vals):
        if 'stage_id' in vals:
            vals['date_of_stage_change'] = datetime.now()
        return super().write(vals)

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.check_email is False or self.check_date is False or self.check_areacode is False:
            raise ValidationError(_("Perform checklist!"))
        else:
            if self.stage_id.name.lower() in ('appointment needed', 'scheduled'):
                stage_id = self.stage_id.id
                external_mail = self.env.ref('BluStar_email_templates.appointment_email_externals')
                internal_mail = self.env.ref('BluStar_email_templates.appointment_email_internal')
                external_mail.send_mail(self._origin.id, force_send=True)
                internal_mail.send_mail(self._origin.id, force_send=True)
                self.stage_id = stage_id

    def check_lead_duration_in_stage(self):
        rec_ids = self.env['crm.lead'].sudo().search(
            [('stage_id.name', 'in', ('Voicemail left', 'Cancel list', 'Waiting to be rescheduled'))])
        user_id = self.env['res.users'].sudo().search([('name', '=', 'csalmon')])
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
