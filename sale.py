 #-*- encoding: utf-8 -*-
import netsvc
import pooler, tools
import math
import decimal_precision as dp
from tools.translate import _

from osv import fields, osv

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def _tot_riga_conai(self, cr, uid, ids, field_name, arg, context=None):
     #  PER CALCOLARE QUESTI DATI DEVE PRIMA ACCERTARSI CHE IL CASSTELLETTO IVA SIA CORRETTO
     
     res = {}
     return res
   
    _columns = {
               'peso_conai':fields.float('Peso Conai', digits=(2, 7)),
               'totale_conai':fields.float('Totale Conai', digits=(2, 7)),
               }
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):

        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, fiscal_position=fiscal_position, flag=flag)
        
        result = res.get('value', False)
        domain = res.get('domain', False)
        warning = res.get('warning', False)
        if product:
          #import pdb;pdb.set_trace()
          art_obj = self.pool.get("product.product").browse(cr, uid, [product])[0]

          prz_conai = art_obj.conai.valore
          result['peso_conai'] = art_obj.peso * result['product_uos_qty']
          result['totale_conai'] = prz_conai * art_obj.peso * result['product_uos_qty']
          #import pdb;pdb.set_trace()
        return {'value': result, 'domain': domain, 'warning': warning}   
sale_order_line()
