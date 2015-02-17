# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2012 ZestyBeanz Technologies Pvt. Ltd.
#    (http://wwww.zbeanztech.com)
#    contact@zbeanztech.com
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
from osv import osv

class stock_move(osv.osv):
    
    _inherit = "stock.move"
    
    def action_cancel_done(self, cr, uid, move_obj, context= None):
        res = False
        for move in move_obj:
            if move.state == "done":
                res= self.write(cr, uid, move.id, {'state': 'cancel'}, context=context)
            print res
        return res
    
class mrp_production(osv.osv):
    
   _inherit = 'mrp.production'
   
   def action_cancel(self, cr, uid, ids, context=None):
        res = super(mrp_production, self).action_cancel(cr, uid, ids, context)
        picking_pool = self.pool.get("stock.picking")
        move_obj = self.pool.get("stock.move")
        val = False
        if res: 
           for production in self.browse(cr, uid, ids, context=context):
               if production.move_created_ids:
                   val = move_obj.action_cancel_done(cr, uid, [x for x in production.move_created_ids2], context=context)
               val = move_obj.action_cancel_done(cr, uid, [x for x in production.move_lines2], context=context)
               picking_obj = production.picking_id or False
               if picking_obj and picking_obj.state != 'cancel' and val:
                   picking_pool.write(cr, uid, picking_obj.id, {'state' : 'cancel'}, context=context)
                   move_obj.action_cancel_done(cr, uid, [x for x in picking_obj.move_lines], context=context)
        return res
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
