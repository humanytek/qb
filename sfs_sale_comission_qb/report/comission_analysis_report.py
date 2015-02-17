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

import xml.etree.cElementTree as ET
import tools

class comission_analysis_report(osv.osv):
    _name = 'comission.analysis.report'
    _description = 'Analysis on comission on invoice'
    _auto = False
    
    _columns = {
                'salesman_id': fields.many2one('res.users', 'Salesman'),
                'partner_id': fields.many2one('res.partner', 'Customer'),
                'invoice_number': fields.char('Invoice Number', size=128),
                'date_invoice': fields.datetime('Date of Invoice'),
                'amount_untaxed': fields.float('Amount Untaxed'),
                'comission_amount': fields.float('Comission Amount'),
                'journal_id': fields.many2one('account.journal', 'Journal'),
                'period_id': fields.many2one('account.period', 'Period'),
                'currency_id': fields.many2one('res.currency', 'Currency'),
                'invoice_date_from':fields.function(lambda *a, **k:{}, method=True, type='datetime',
                                                    string="Invoice Date From"),
                'invoice_date_to':fields.function(lambda *a, **k:{}, method=True, type='datetime',
                                                  string="Invoice Date To")
                }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'comission_analysis_report')
        cr.execute("""
            create or replace view comission_analysis_report as (
                select inv.id as id,
                    inv.user_id as salesman_id,
                    inv.partner_id as partner_id,
                    inv.number as invoice_number,
                    inv.date_invoice as date_invoice,
                    case
                        when inv.type = 'out_invoice' then inv.amount_untaxed
                        when inv.type = 'out_refund' then inv.amount_untaxed * -1
                    end as amount_untaxed,
                    inv.amount_comission as comission_amount,
                    inv.journal_id as journal_id,
                    inv.period_id as period_id,
                    inv.currency_id as currency_id
                from 
                    account_invoice inv
                where
                    inv.type in ('out_invoice', 'out_refund') and
                    inv.state not in ('draft', 'cancel')
                )""")

comission_analysis_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
