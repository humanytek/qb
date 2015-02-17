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

from tools.translate import _

class comission_analysis_wizard(osv.osv_memory):
    _name = 'comission.analysis.wizard'
    _description = 'Comission Analysis Wizard'
    _columns = {
                'start_period_id': fields.many2one('account.period', 'Start Period'),
                'end_period_id': fields.many2one('account.period', 'End Period'),
                'with_currency': fields.boolean('With Currency'),
                'journal_ids': fields.many2many('account.journal', 'journal_wizard_rel', 'wizard_id',
                                                'journal_id', 'Journal')
                }
    
    def open_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        period_pool = self.pool.get('account.period')
        obj_model = self.pool.get('ir.model.data')
        data = self.read(cr, uid, ids)[0]
        start_period_id = data.get('start_period_id', [])[0]
        end_period_id = data.get('end_period_id', [])[0]
        journal_ids = data.get('journal_ids', [])
        period_ids = period_pool.build_ctx_periods(cr, uid, start_period_id, end_period_id)
        model_data_ids = obj_model.search(cr,uid,[('model','=','ir.ui.view'),
                                                  ('name','=','comission_analysis_view_search')])
        resource_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        domain = [('journal_id', 'in', journal_ids), ('period_id', 'in', period_ids)]
        ctx = context.copy()
        ctx.update({'search_default_group_salesman': 1, 'search_default_group_partner': 1})
        model_data_ids = obj_model.search(cr,uid,[('model','=','ir.ui.view'),
                                                      ('name','=','comission_analysis_view_form')])
        form_view_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        if data.get('with_currency', False):
            model_data_ids = obj_model.search(cr,uid,[('model','=','ir.ui.view'),
                                                      ('name','=','comission_analysis_view_tree_with_cur')])
            tree_view_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        else:
            model_data_ids = obj_model.search(cr,uid,[('model','=','ir.ui.view'),
                                                      ('name','=','comission_analysis_view_tree')])
            tree_view_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        return {
              'name': _('Comission Analysis'),
              'view_type': 'form',
              'view_mode': 'tree,form',
              'views': [(tree_view_id, 'tree'), (form_view_id,'form')],
              'res_model': 'comission.analysis.report',
              'type': 'ir.actions.act_window',
              'domain': domain,
              'context': ctx,
              'search_view_id': resource_id
              }
    
    def print_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids)[0]
        report_name = 'invoice.comission.report'
        if data.get('with_currency', False):
            report_name = 'invoice.comission.report.with.cur'
        return {
                'type': 'ir.actions.report.xml',
                'report_name': report_name,
                'datas': {
                          'model': 'account.invoice',
                          'id': ids[0],
                          'ids': ids,
                          'report_type': 'pdf',
                          'form': data
                          },
                'nodestroy': False
               }
    
comission_analysis_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
