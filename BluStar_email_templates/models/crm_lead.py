from odoo import models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def create(self, vals_list):
        res = super(CrmLead, self).create(vals_list)

        external_mail = self.env.ref('BluStar_email_templates.appointment_email_externals')
        internal_mail = self.env.ref('BluStar_email_templates.appointment_email_internal')
        external_mail.send_mail(res.id, force_send=True)
        internal_mail.send_mail(res.id, force_send=True)

        return res

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.stage_id.name.lower() in ('appointment needed', 'scheduled'):
            stage_id = self.stage_id.id
            external_mail = self.env.ref('BluStar_email_templates.appointment_email_externals')
            internal_mail = self.env.ref('BluStar_email_templates.appointment_email_internal')
            external_mail.send_mail(self._origin.id, force_send=True)
            internal_mail.send_mail(self._origin.id, force_send=True)
            self.stage_id = stage_id
