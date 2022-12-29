import requests
import logging
from odoo.exceptions import ValidationError
from odoo import fields, models, _, api

_logger = logging.getLogger(__name__)


class CRMLeads(models.Model):
    _inherit = 'crm.lead'
    rpt_id = fields.Char(string="RPT ID")
    parrner_ids = fields.One2many('res.partner', 'lead_id', string="Partner Data")

    def import_leads_from_rpt_to_odoo(self, configuration_id=False, rpt_user_id=False):
        if configuration_id.rpt_updated_date:
            api_url = "{0}projects?offset=1&limit=25&fields=id,title,roles,updated_at&filter=user_id%3Ain%3A%5B{1}%5D%2Cuser_project_status_id%3Ain%3A%5B2%5D%2Cupdated_at%3Agte%3A{2}&cards=1".format(
                configuration_id.rpt_smart_api_url, rpt_user_id, configuration_id.rpt_updated_date.strftime('%Y-%m-%d'))
        else:
            api_url = "{0}projects?offset=1&limit=50&fields=id,title,roles,updated_at&filter=user_id%3Ain%3A%5B{1}%5D%2Cuser_project_status_id%3Ain%3A%5B2%5D&cards=1".format(
                configuration_id.rpt_smart_api_url, rpt_user_id)
        headers = {'accept': 'application/json', 'Authorization': '%s' % (configuration_id.rpt_token)}
        try:
            response_data = requests.request("GET", api_url, headers=headers)
            if response_data.status_code in [200, 201]:
                response_data = response_data.json()
                if response_data.get('result'):
                    for data in response_data.get('result').get('data'):
                        lead_id = self.search([('rpt_id', '=', data.get('id'))])
                        stage_id = self.env['crm.stage'].search([], limit=1)
                        if not lead_id:
                            lead_id = self.create({'name': data.get('title') or "",
                                                   'partner_name': "",
                                                   'street': "",
                                                   'description': "",
                                                   'street2': "",
                                                   'city': "",
                                                   'zip': "",
                                                   'state_id': "",
                                                   'country_id': "",
                                                   'phone': "",
                                                   'website': "",
                                                   'stage_id': stage_id.id,
                                                   'type': 'lead',
                                                   'rpt_id': data.get('id')})
                            self._cr.commit()
                            for user_data in data.get('roles'):
                                phone_data = ""
                                email_data = ""
                                for communication in user_data.get('company_card').get('communications'):
                                    if communication.get('communication_type_id') == 1:
                                        phone_data = communication.get('value')
                                    if communication.get('communication_type_id') == 4:
                                        email_data = communication.get('value')
                                if not self.env['res.partner'].search([('rpt_company_id','=',user_data.get('company_id'))]):
                                    self.env['res.partner'].create({
                                        'name': "%s" % (user_data.get('company_card').get('name')),
                                        'phone': phone_data,
                                        'email': email_data,
                                        'rpt_company_id': user_data.get('company_id'),
                                        'lead_id': lead_id and lead_id.id,
                                        'company_role_name': user_data.get('company_role_card').get('name')
                                    })
                            lead_id.convert_opportunity(lead_id.partner_id.id, user_ids=False, team_id=False)
                        else:
                            lead_id.write({'rpt_id': data.get('id'), 'stage_id': stage_id.id})
            else:
                raise ValidationError(response_data.content)
        except Exception as error:
            raise ValidationError(_(error))
