 #-*- encoding: utf-8 -*-
import netsvc
import pooler, tools
import math
import decimal_precision as dp
from tools.translate import _

from osv import fields, osv


class sale_order(osv.osv):
    _inherit = 'sale.order'
    _columns={
              'esenzione_conai':fields.many2one('conai.esenzioni', 'Tipo di Esenzione Conai'),
              'scad_esenzione_conai': fields.date('Scadenza Esenzione Conai', required=False, readonly=False),
              }
    
    def onchange_partner_id(self, cr, uid, ids, part):
        res = super(sale_order,self).onchange_partner_id(cr, uid, ids, part)
        val = res.get('value', False)
        if part: 
             part = self.pool.get('res.partner').browse(cr, uid, part)
             if part.esenzione: #esiste un codice di esenzione conai
                 val['esenzione_conai']= part.esenzione.id
                 val['scad_esenzione_conai']=part.scad_esenzione
        
        return {'value': val}               
    
    
    
sale_order()



class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def _tot_riga_conai(self, cr, uid, ids, field_name, arg, context=None):
     #  PER CALCOLARE QUESTI DATI DEVE PRIMA ACCERTARSI CHE IL CASSTELLETTO IVA SIA CORRETTO
        res = {}
        if context is None:
            context = {}
        
        for line in self.browse(cr, uid, ids, context=context):
            if line.order_id.esenzione_conai and line.order_id.scad_esenzione_conai>=line.order_id.date_order: # c'è una esenzione conai
                # c'è un codice di esenzione
                res[line.id] = line.prezzo_conai * line.peso_conai
                res[line.id] = res[line.id] *(1-line.order_id.esenzione_conai.perc/100)
            else:
                res[line.id] = line.prezzo_conai * line.peso_conai
                
        return res
   
    _columns = {
               'cod_conai':fields.many2one('conai.cod', 'Codice Conai'),
               'peso_conai':fields.float('Peso Conai', digits=(2, 7)),
               'prezzo_conai':fields.float('Valore Unitario ', digits=(2, 7), required=True),
               'totale_conai': fields.function(_tot_riga_conai, method=True, string='Totale riga Conai', digits=(12, 7)),
               # 'totale_conai':fields.float('Totale Conai', digits=(12, 7)),
               }
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        #import pdb;pdb.set_trace()
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, fiscal_position=fiscal_position, flag=flag)
        
        result = res.get('value', False)
        domain = res.get('domain', False)
        warning = res.get('warning', False)
        if product:
          #import pdb;pdb.set_trace()
          art_obj = self.pool.get("product.product").browse(cr, uid, [product])[0]
          if art_obj.conai.id:
              prz_conai = art_obj.conai.valore
              result['cod_conai'] = art_obj.conai.id
              result['peso_conai'] = art_obj.production_conai_peso * result['product_uos_qty']
              result['prezzo_conai'] = prz_conai
          else:
              result['cod_conai'] = 0.0
              result['peso_conai'] = 0.0
              result['prezzo_conai'] = 0.0
               
               
         # result['totale_conai'] = prz_conai * art_obj.peso * result['product_uos_qty']
          #import pdb;pdb.set_trace()
        return {'value': result, 'domain': domain, 'warning': warning}
       
    def on_change_qty(self, cr, uid, ids, product_id, listino_id, qty, partner_id, uom, data_doc): #
    
        v = {}
        if product_id:
                    art_obj = self.pool.get("product.product").browse(cr, uid, [product_id])[0]
                    if art_obj.conai.id:
                        prz_conai = art_obj.conai.valore
                        v['cod_conai'] = art_obj.conai.id
                        v['peso_conai'] = art_obj.production_conai_peso * qty
                        v['prezzo_conai'] = prz_conai
                    else:
                        v['cod_conai'] = 0.0
                        v['peso_conai'] = 0.0
                        v['prezzo_conai'] = 0.0
        
        return {'value':v}    
    
    
    
    
sale_order_line()
