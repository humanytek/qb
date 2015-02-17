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

import jasper_reports

import pooler

def jasper_invoice_comission_report(cr, uid, ids, data, context=None):
    pool = pooler.get_pool(cr.dbname)
    period_pool = pool.get('account.period')
    journal_ids = data['form']['journal_ids']
    from_period_id = data['form']['start_period_id'][0]
    from_period_obj = period_pool.browse(cr, uid, from_period_id, context=context)
    from_period_name = from_period_obj.date_start or ''
    end_period_id = data['form']['end_period_id'][0]
    end_period_obj = period_pool.browse(cr, uid, end_period_id, context=context)
    end_period_name = end_period_obj.date_stop
    period_ids = period_pool.build_ctx_periods(cr, uid, from_period_id, end_period_id)
    if len(journal_ids) == 1:
        journal_ids = "(" + str(journal_ids[0]) + ")"
    else:
        journal_ids = tuple(journal_ids)
    if len(period_ids) == 1:
        period_ids = "(" + str(period_ids[0]) + ")"
    else:
        period_ids = tuple(period_ids)
    return {
            'parameters': {
                           'journal_ids': str(journal_ids),
                           'period_ids': str(period_ids),
                           'start_period': from_period_name,
                           'end_period': end_period_name
                          },
           }

jasper_reports.report_jasper(
                             'report.invoice.comission.report',
                             'account.invoice',
                             parser=jasper_invoice_comission_report
                            )
jasper_reports.report_jasper(
                             'report.invoice.comission.report.with.cur',
                             'account.invoice',
                             parser=jasper_invoice_comission_report
                            )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
