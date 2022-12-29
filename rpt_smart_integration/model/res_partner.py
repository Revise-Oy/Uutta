import logging
from odoo import fields, models, _, api

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    rpt_company_id = fields.Char(string="Company ID")
    company_role_name = fields.Char(string="Company Role Name")
    lead_id = fields.Many2one('crm.lead', string='Lead ID')