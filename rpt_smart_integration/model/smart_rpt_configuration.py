import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from requests import request


class RPTSmartConfiguration(models.Model):
    _name = "rpt.smart.configuration"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Name", required=True, help="configuration")
    rpt_smart_api_url = fields.Char(string='RPT API URL', default="https://api.smart.rpt.fi/v1/client/")
    rpt_client_id = fields.Char(string="RPT Client ID", copy=False)
    rpt_client_secret = fields.Char(string="RPT Client Secret", copy=False)
    rpt_token = fields.Char(string='Token', default="Bearer")
    rpt_user_id = fields.Many2one('res.users', string="User")
    rpt_updated_date = fields.Datetime(string="RPT Updated Date")

    def import_customers_from_rpt_to_odoo(self):
        self.env['res.users'].import_customers_from_rpt_to_odoo(self)
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Yeah! Users imported successfully!!",
                'img_url': '/web/static/img/smile.svg',
                'type': 'rainbow_man',
            }
        }

    def import_leads_from_rpt_to_odoo(self):
        if not self.rpt_user_id and self.rpt_user_id.rpt_id:
            raise ValidationError("Please select proper User!!")
        self.env['crm.lead'].import_leads_from_rpt_to_odoo(self, self.rpt_user_id.rpt_id)
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Yeah! Lead data imported successfully.",
                'img_url': '/web/static/img/smile.svg',
                'type': 'rainbow_man',
            }
        }

    def fetch_rpt_token(self):
        api_url = "https://api.smart.byggfakta.se/v1/auth"
        requests_data = {
            "client_id": "%s" % (self.rpt_client_id),
            "client_secret": "%s" % (self.rpt_client_secret),
        }
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        try:
            response_data = request("POST", api_url, headers=headers, data=json.dumps(requests_data))
            if response_data.status_code in [200, 201]:
                response_data = response_data.json()
                if response_data.get('result'):
                    self.rpt_token = "Bearer %s"%(response_data.get('result') and response_data.get('result').get('opid'))
                    return {
                        'effect': {
                            'fadeout': 'slow',
                            'message': "Yeah! Token imported successfully.",
                            'img_url': '/web/static/img/smile.svg',
                            'type': 'rainbow_man',
                        }
                    }
            else:
                raise ValidationError(response_data.content)
        except Exception as error:
            raise ValidationError(_(error))


    def action_redirect_to_users(self):
        action = self.env.ref('base.action_res_users').read()[0]
        action['domain'] = [('rpt_id', '!=', False)]
        return action

    def action_redirect_to_leads(self):
        action = self.env.ref('crm.crm_lead_action_pipeline').read()[0]
        action['domain'] = [('rpt_id', '!=', False)]
        return action
