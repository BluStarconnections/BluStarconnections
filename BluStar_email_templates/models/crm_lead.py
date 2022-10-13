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



    # def send_email(self):
    #     external_mail = self.env.ref('BluStar_email_templates.appointment_email_externals')
    #     external_mail.send_mail(self.id, force_send=True)
    #     external_mail = self.env.ref('BluStar_email_templates.appointment_email_externals')
    #     internal_mail.send_mail(self.id, force_send=True)
