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

from report import report_sxw

class account_invoice_facturae_pac_sf_pdf(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_invoice_facturae_pac_sf_pdf, self).__init__(cr, uid, name, context=context)
        
report_sxw.report_sxw(
    'report.l10n_mx_facturae_pac_sf.account.invoice.facturae.pac.sf.pdf',
    'account.invoice',
    'addons/sfs_l10n_mx_facturae_pac_sf_customization/report/invoice_facturae_pac_sf_pdf.rml',
    header=False,
    parser=account_invoice_facturae_pac_sf_pdf,
)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
