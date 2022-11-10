import base64
import datetime

from odoo import models, fields


class TrackStageChanges(models.Model):
    _name = 'track.stage.change'
    _description = 'Track record of changing stages in CRM'

    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user.id)
    lead_id = fields.Many2one('crm.lead', 'Lead id', invisible=1)
    prev_stage = fields.Many2one('crm.stage', 'Previous stage')
    new_stage = fields.Many2one('crm.stage', 'New stage')
    date_today = fields.Date('Date', default=datetime.datetime.today())


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    stage_change_ids = fields.One2many(comodel_name='track.stage.change', inverse_name='lead_id',
                                       string='Stage Changes')

    def write(self, vals):
        if 'stage_id' in vals:
            new_stage_id = self.env['crm.stage'].sudo().search([('id', '=', vals.get('stage_id'))])
            data_dict = {
                'prev_stage': self.stage_id.id,
                'new_stage': new_stage_id.id,
                'lead_id': self.id,
            }
            self.env['track.stage.change'].sudo().create(data_dict)
        return super(CrmLeadInherit, self).write(vals)

    # get stage tracking data for report
    def get_report_vals(self):
        date_today = datetime.datetime.today()
        stages_data = self.env['track.stage.change'].sudo().search([('date_today', '=', date_today)], order='lead_id')
        data_dict = {}
        for rec in stages_data:
            if rec.user_id.name not in data_dict:
                data_dict[rec.user_id.name] = [{
                    'lead': rec.lead_id.name,
                    'prev_stage': rec.prev_stage.name,
                    'new_stage': rec.new_stage.name,
                }]
            else:
                data_dict[rec.user_id.name].append({
                    'lead': rec.lead_id.name,
                    'prev_stage': rec.prev_stage.name,
                    'new_stage': rec.new_stage.name,
                })

        data = {
            'data_dict': data_dict,
        }
        return data

    def send_crm_stage_tracking_email(self):
        # get report values
        data = self.get_report_vals()
        obj = self.env['crm.lead'].sudo().search([], limit=1)

        # now sending email with report attached
        report_content = self.env.ref('BluStar_email_templates.action_report_stage_tracking').sudo()._render_qweb_pdf(
            res_ids=obj.id, data=data)
        base64pdf = base64.b64encode(report_content[0])
        ir_values = {
            'name': 'Stage Tracking Report',
            'type': 'binary',
            'datas': base64pdf,
            'store_fname': base64pdf,
            'mimetype': 'application/pdf',
            'res_model': 'crm.lead',
            'res_id': self.id
        }
        report_attachment = self.env['ir.attachment'].sudo().create(ir_values)
        email_template = self.env.ref('BluStar_email_templates.crm_stage_tracking_mail')
        if email_template:
            email_template.attachment_ids = [(4, report_attachment.id)]
            email_template.send_mail(self.id, force_send=True)
            email_template.attachment_ids = [(5, 0, 0)]
        return True
