# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 SF Soluciones.
#    (http://www.sfsoluciones.com)
#    contacto@sfsoluciones.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields

import decimal_precision as dp

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    def _get_comission(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice_obj in self.browse(cr, uid, ids, context=context):
            invoice_amount = invoice_obj.amount_untaxed or 0.00
            comission_percent = invoice_obj.partner_id and invoice_obj.partner_id.comission_percent or 0.00
            comission_amount = invoice_amount * (comission_percent/100)
            res[invoice_obj.id] = comission_amount
        return res
    
    _columns = {
                'amount_comission': fields.function(_get_comission,
                                                    digits_compute=dp.get_precision('Account'),
                                                    string='Comission',
                                                    store={
                                                           'account.invoice': (lambda self, cr, uid, ids,
                                                                               c={}: ids, ['invoice_line'],
                                                                               20)
                                                           }),
                }

account_invoice()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
