# _*_ coding: utf-8 _*_
from openerp import models, api, _


class AutoDoneWizard(models.TransientModel):
    _name = "account_move_adjust.account_move_auto_adjust_wizard"

    @api.multi
    def action_ok(self):
        self.ensure_one()
        select_orders = self.env["account.move"].browse(self.env.context.get("active_ids"))
        select_orders.adjust()
        return True
