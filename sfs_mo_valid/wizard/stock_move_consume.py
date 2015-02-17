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

class stock_move_consume(osv.osv):
    _inherit = "stock.move.consume"
    
    def do_move_consume(self, cr, uid, ids, context= None):
       if context == None:
           context = {}
       data = self.read(cr, uid, ids[0], context=context)
       product_pool = self.pool.get("product.product")
       location_id = data['location_id'] and data['location_id'][0]
       warehouse_id = self.pool.get("stock.warehouse").search(cr, uid, [('lot_stock_id','=',location_id)], 
                                                              context=context)
       flag = False
       warning_msg = ""
       product_id = data['product_id'] and data['product_id'][0]
       product_rec = product_pool.browse(cr, uid, product_id,context=context)
       if product_rec.type == 'product' and warehouse_id:
           context.update({
                           'warehouse' : warehouse_id[0],
                           'what':('in', 'out'),
                           'states':(['done']),
                           })
           available_products = product_pool.get_product_available(cr, uid, [product_id], context=context)
           if available_products.values() and available_products.values()[0] < data['product_qty'] :
               flag = True
               warning_msg = "%s has %s stock and you need %s"%(data['product_id'][1], 
                                                                available_products.values()[0], 
                                                                data['product_qty'])
       if flag: 
           raise osv.except_osv(_('Warning ! you cant validate the manufacture order, \
           there are raw materials missing in warehouse.!'),
                        _(warning_msg))
       return super(stock_move_consume, self).do_move_consume(cr, uid, ids, context=context)

stock_move_consume()
       
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: