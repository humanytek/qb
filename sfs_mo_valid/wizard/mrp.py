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
from tools.translate import _

class mrp_production(osv.osv):
    
   _inherit = 'mrp.product.produce'
   def do_produce(self, cr, uid, ids, context=None):
       if context == None:
           context = {}
       production_id = context.get('active_id', False)
       assert production_id, "Production Id should be specified in context as a Active ID"
       production_rec = self.pool.get("mrp.production").browse(cr, uid, production_id, context)
       product_pool = self.pool.get("product.product")
       location_id = production_rec.location_src_id and production_rec.location_src_id.id
       warehouse_id = self.pool.get("stock.warehouse").search(cr, uid, [('lot_stock_id','=',location_id)],
                                                               context=context)
       flag = False
       warning_list = []
       for stock_move_rec in production_rec.move_lines:
           product_rec = stock_move_rec.product_id
           if product_rec.type == 'product' and warehouse_id:
               context.update({
                               'warehouse' : warehouse_id[0],
                               'what':('in', 'out'),
                               'states':(['done']),
                               })
               available_products = product_pool.get_product_available(cr, uid, [product_rec.id], context=context)
               if available_products.values() and available_products.values()[0] < stock_move_rec.product_qty :
                   flag = True
                   warning_list.append(_("%s has %s stock and you need %s")%(product_rec.name, 
                                                                    available_products.values()[0], 
                                                                    stock_move_rec.product_qty))
       if flag: 
           raise osv.except_osv(_('Warning ! you cant validate the manufacture order, \
           there are raw materials missing in warehouse.!'),
                        _(','.join(warning_list)))
       return super(mrp_production, self).do_produce(cr, uid, ids, context=context)
   
mrp_production()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
