# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp import exceptions


class AccountMove(models.Model):
    _inherit = "account.move"

    is_adjusted = fields.Boolean(default=False)

    @api.multi
    def adjust(self):
        for move in self:
            credit_lines = move.line_id.filtered(lambda l: l.credit != 0 and l.debit == 0)
            debit_lines = move.line_id.filtered(lambda l: l.debit != 0 and l.credit == 0)

            if move.name.startswith("EXJ".upper()):
                if len(debit_lines) <= 0:
                    raise exceptions.Warning(_("can not find any debit lines"))
                state = move.state
                if state == "posted":
                    move.button_cancel()
                for l in debit_lines:
                    l.debit = round(l.debit)
                if len(credit_lines) <= 0:
                    raise exceptions.Warning(_("can not find any credit lines"))
                if len(credit_lines) > 1:
                    raise exceptions.Warning(_("only one credit line is allowed"))
                credit_lines.ensure_one()
                credit_lines.credit = sum(l.debit for l in debit_lines)
                move.is_adjusted = True
                if state == "posted":
                    move.button_validate()
            elif move.name.startswith("SAJ".upper()):
                if len(credit_lines) <= 0:
                    raise exceptions.Warning(_("can not find any credit lines"))
                state = move.state
                if state == "posted":
                    move.button_cancel()
                for l in credit_lines:
                    l.credit = round(l.credit)
                if len(debit_lines) <= 0:
                    raise exceptions.Warning(_("can not find any debit lines"))
                if len(debit_lines) > 1:
                    raise exceptions.Warning(_("only one debit line is allowed"))
                debit_lines.ensure_one()
                debit_lines.debit = sum(l.credit for l in credit_lines)
                move.is_adjusted = True
                if state == "posted":
                    move.button_validate()
            else:
                raise exceptions.Warning(_("only with name start with EXJ or SAJ"))
