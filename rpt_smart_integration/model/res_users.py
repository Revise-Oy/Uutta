import requests
import logging
from odoo.exceptions import ValidationError
from odoo import fields, models, _, api
from odoo import Command
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    rpt_id = fields.Char(string="RPT ID")

    def import_customers_from_rpt_to_odoo(self, configuration_id=False):
        api_url = "%susers?offset=1&limit=50" % (configuration_id.rpt_smart_api_url)
        headers = {'accept': 'application/json', 'Authorization': '%s'%(configuration_id.rpt_token)}
        try:
            response_data = requests.request("GET", api_url, headers=headers)
            if response_data.status_code in [200, 201]:
                response_data = response_data.json()
                if response_data.get('result'):
                    for data in response_data.get('result').get('data'):
                        partner_id = self.env['res.users'].search([('email', '=', data.get('email'))])
                        if not partner_id:
                            self.create({'name': data.get('name'),
                                         'email': data.get('email'),
                                         'password': data.get('email'),
                                         'login': data.get('email'),
                                         'rpt_id': data.get('id'),
                                         'groups_id': [Command.set(
                                             [self.env.ref('base.group_user').id,
                                              self.env.ref('base.group_partner_manager').id])],
                                         })
                        else:
                            partner_id.write({'rpt_id': data.get('id')})
            else:
                raise ValidationError(response_data.content)
        except Exception as error:
            raise ValidationError(_(error))
        return True
