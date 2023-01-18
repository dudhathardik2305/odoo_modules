from odoo import models, fields, api
import requests
import json
from functools import partial

class PosOrder(models.Model):
     _inherit = 'pos.order'

     links = fields.Char(string="Link")  #we need this field to displayed on the receipt 
     

     @api.model
     def _order_fields(self, ui_order):
         order_fields = super()._order_fields(ui_order)
         process_line = partial(self.env['pos.order.line']._order_line_fields, session_id=ui_order['pos_session_id'])

         context = self._context

         current_uid = context.get('uid')

         uset = self.env['res.users'].browse(current_uid)
         current_company = uset.company_id.phone

         a = float(ui_order["amount_total"])
         b = float(ui_order['amount_total'] - ui_order['amount_tax'])
         c = float(ui_order['amount_tax'])
         d = str(ui_order['creation_date'])
         e = str(ui_order['name'])
         url = "http://154.72.68.222:9010/api/sign?invoice+1"
         payload = json.dumps({
             "invoice_date": f"{d}",
             "invoice_number": "6435",
             "invoice_tin": f"{current_company}",
             "customer_name": "SIMON",
             "customer_tin": "111-111-111",
             "customer_phone": "",
             "customer_vrn": "",
             "passport_id": "",
             "driving_lic": "",
             "customer_nid": "",
             "vat_amount": f"{c}",
             "gross_amount": f"{b}",
             "grand_total": f"{a}"
         })

         headers = {
             'Cache-Control': 'no-cache',
             'Authorization': 'Basic ZxZoaZMUQbUJDljA7kTExQ==',
             'Content-Type': 'application/json'
         }

         response = requests.request("POST", url, headers=headers, data=payload)
         # print("test", response.text)
         print("Invoice Date", ui_order['creation_date'])
         print("Invoice Number", ui_order['sequence_number'])
         print("Invoice Tin", current_company)
         print("Customer Number", ui_order['user_id'])
         print("Tax%", ui_order['amount_tax'])
         print("Total untaxed", (ui_order['amount_total'] - ui_order['amount_tax']))
         print("Grand Total", ui_order['amount_total'])
         ui_order['links'] = response.text
         print('\n\nlink',ui_order['links'],'\n\n')
         order_fields['user_id'] = ui_order['user_id'] or False
         order_fields['session_id'] = ui_order['pos_session_id']
         order_fields['lines'] = [process_line(l) for l in ui_order['lines']] if ui_order['lines'] else False
         order_fields['pos_reference'] = ui_order['links']
         order_fields['sequence_number'] = ui_order['sequence_number']
         order_fields['partner_id'] = ui_order['partner_id'] or False
         order_fields['date_order'] = ui_order['creation_date'].replace('T', ' ')[:19]
         order_fields['fiscal_position_id'] = ui_order['fiscal_position_id']
         order_fields['pricelist_id'] = ui_order['pricelist_id']
         order_fields['amount_paid'] = ui_order['amount_paid']
         order_fields['amount_total'] = ui_order['amount_total']
         order_fields['amount_tax'] = ui_order['amount_tax']
         order_fields['amount_return'] = ui_order['amount_return']
         order_fields['company_id'] = self.env['pos.session'].browse(ui_order['pos_session_id']).company_id.id
         order_fields['to_invoice'] = ui_order['to_invoice'] if "to_invoice" in ui_order else False
         order_fields['to_ship'] = ui_order['to_ship'] if "to_ship" in ui_order else False
         order_fields['is_tipped'] = ui_order.get('is_tipped', False)
         order_fields['tip_amount'] = ui_order.get('tip_amount', 0)
         order_fields['access_token'] = ui_order.get('access_token', '')
         order_fields['links'] = ui_order['links']

         return order_fields

     def _export_for_ui(self, order):
        result = super(PosOrder, self)._export_for_ui(order)
        result.update({
            'links': order.links,
        })
        return result


class resuser_tinnum(models.Model):
    _inherit = "res.company"

    Tin_number = fields.Char(string="Tin Number")