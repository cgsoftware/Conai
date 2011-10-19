# -*- encoding: utf-8 -*-
import netsvc
import pooler, tools
import math

from tools.translate import _

from osv import fields, osv


class producttemplate(osv.osv):
    
    _inherit = 'product.template'
    
    _columns = {
                'conai':fields.many2one('conai.cod', 'Codice Conai'),
                'peso_template':fields.float('Peso Imballo', digits=(2, 7), required=False),
                #'valore_conai_template':fields.float('Costo CONAI') #NON OCCORRE A LIVELLO DI TEMPLATE....
                }
producttemplate()


class product_product(osv.osv):

    _inherit = 'product.product'
    
    def _calcola_valore_conai(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        #import pdb;pdb.set_trace()
        if ids:
            for product_obj in self.pool.get('product.product').browse(cr, uid, ids):
              if product_obj.product_tmpl_id.conai:
                conai_obj = product_obj.product_tmpl_id.conai
                prezzo_unit = conai_obj.valore
                peso_prod = product_obj.peso_prod
                res[product_obj.id] = {'valore_conai_prod': prezzo_unit * peso_prod}
                   
        return res
    
    _columns = {
#                'conai':fields.many2one('conai.cod','Codice Conai'),
                'conai': fields.related('product_tmpl_id', 'conai', string="Codice Conai", relation='conai.cod', type='many2one', store=True),
                'peso_prod':fields.float('Peso Imballo', digits=(2, 7), required=False),
                'valore_conai_prod':fields.function(_calcola_valore_conai , method=True, string='Valore Conai', store=True, multi='sums')  #campo function moltiplica il peso dell'imballo per il prezzo unitario della tabella CONAI
                
                }
product_product()

