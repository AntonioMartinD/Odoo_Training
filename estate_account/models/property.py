from odoo import models, Command

class Property(models.Model):
    _inherit = "property"

    def action_sold(self):
        for record in self:
            accepted_offer = record.offer_ids.get_accepted_offer()
            journal = record.env["account.journal"].search([("type", "=", "sale")], limit=1)
            record.env['account.move'].create({
            'partner_id': accepted_offer.partner_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                Command.create(
                    {"name": record.name,
                    "quantity": 1,
                    "price_unit": record.selling_price
                    }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
                Command.create({
                    'name': 'Sales Commission',
                    'quantity': 1,
                    'price_unit': record.selling_price * 0.06,
                })
            ]
            })
        res = super().action_sold()
        return res

