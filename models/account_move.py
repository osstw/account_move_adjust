# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp import exceptions
import math


class AccountMove(models.Model):
    _inherit = "account.move"

    customize_internal_code = fields.Char(readonly=True)

    @api.multi
    def adjust(self):
        self.ensure_one()
        credit_lines = self.line_id.filtered(lambda l: l.credit != 0 and l.debit == 0)
        debit_lines = self.line_id.filtered(lambda l: l.debit != 0 and l.credit == 0)

        if self.name.startswith("EXJ".upper()):
            if len(debit_lines) <= 0:
                raise exceptions.Warning("can not find any debit lines")
            for l in debit_lines:
                l.debit = round(l.debit)
            if len(credit_lines) <= 0:
                raise exceptions.Warning("can not find any credit lines")
            if len(credit_lines) > 1:
                raise exceptions.Warning("only one credit line is allowed")
            credit_lines.ensure_one()
            credit_lines.credit = sum(l.debit for l in debit_lines)
        elif self.name.startswith("SAJ".upper()):
            if len(credit_lines) <= 0:
                raise exceptions.Warning("can not find any credit lines")
            for l in credit_lines:
                l.credit = round(l.credit)
            if len(debit_lines) <= 0:
                raise exceptions.Warning("can not find any debit lines")
            if len(debit_lines) > 1:
                raise exceptions.Warning("only one debit line is allowed")
            debit_lines.ensure_one()
            debit_lines.debit = sum(l.credit for l in credit_lines)
        else:
            raise exceptions.Warning("only with name start with EXJ or SAJ")
