 #-*- encoding: utf-8 -*-
import netsvc
import pooler, tools
import math
import decimal_precision as dp
from tools.translate import _

from osv import fields, osv

def arrot(cr,uid,valore,decimali):
    #import pdb;pdb.set_trace()
    return round(valore,decimali(cr)[1])


class FiscalDocHeader(osv.osv):
    _inherit = 'fiscaldoc.header'

    _columns={
              'esenzione_conai':fields.many2one('conai.esenzioni', 'Tipo di Esenzione Conai'),
              'scad_esenzione_conai': fields.date('Scadenza Esenzione Conai', required=False, readonly=False),
              }
  
    def onchange_partner_id(self, cr, uid, ids, part,context):
        res = super(FiscalDocHeader,self).onchange_partner_id(cr, uid, ids, part,context)
        val = res.get('value', False)
        warning = res.get('warning', False)
        if part: 
             part = self.pool.get('res.partner').browse(cr, uid, part)
             if part.esenzione: #esiste un codice di esenzione conai
                 val['esenzione_conai']= part.esenzione.id
                 val['scad_esenzione_conai']=part.scad_esenzione
        
        return {'value': val, 'warning': warning}        
 

FiscalDocHeader()



class FiscalDocRighe(osv.osv):
    _inherit = 'fiscaldoc.righe'


    
    
    
    
    def _tot_riga_conai(self, cr, uid, ids, field_name, arg, context=None):

        res = {}
        if context is None:
            context = {}
        
        for line in self.browse(cr, uid, ids, context=context):
            if line.name.esenzione_conai and line.name.scad_esenzione_conai>=line.name.data_documento: # c'è una esenzione conai
                # c'è un codice di esenzione
                res[line.id] = line.prezzo_conai * line.peso_conai
                res[line.id] = res[line.id] *(1-line.name.esenzione_conai.perc/100)
            else:
                res[line.id] = line.prezzo_conai * line.peso_conai
            res[line.id]= arrot(cr,uid,res[line.id],dp.get_precision('Account'))  # arrotonda a 2 cifre in genere  
        return res

   
    _columns = {
               'cod_conai':fields.many2one('conai.cod', 'Codice Conai'),
               'peso_conai':fields.float('Peso Conai', digits=(2, 7)),
               'prezzo_conai':fields.float('Valore Unitario ', digits=(2, 7), required=False),
               'totale_conai': fields.function(_tot_riga_conai, method=True, string='Totale riga Conai',  digits_compute=dp.get_precision('Account')),
               # 'totale_conai':fields.float('Totale Conai', digits=(12, 7)),
               }    
    
    def onchange_articolo(self, cr, uid, ids, product_id, listino_id, qty, partner_id, data_doc, uom,context):
                res = super(FiscalDocRighe, self).onchange_articolo(cr, uid, ids, product_id, listino_id, qty, partner_id, data_doc, uom,context)
                v = res.get('value', False)
                warning = res.get('warning', False)
                domain = res.get('domain', False)
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
                          
                                      
                return {'value': v, 'domain': domain, 'warning': warning}
                #return {'value':v}
            
    def on_change_qty(self, cr, uid, ids, product_id, listino_id, qty, partner_id, uom, data_doc,context): #
        res = super(FiscalDocRighe, self).on_change_qty(cr, uid, ids, product_id, listino_id, qty, partner_id, uom, data_doc,context)
        v = res.get('value', False)
        warning = res.get('warning', False)
        domain = res.get('domain', False)
        
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
        return {'value': v, 'domain': domain, 'warning': warning}
        #return {'value':v}
     

FiscalDocRighe()


class conai_castelletto(osv.osv):
    _name = "conai.castelletto"
    _description = "Castelletto CONAI"      
    _columns = {
                     'name': fields.many2one('fiscaldoc.header', 'Numero Documento', required=True, ondelete='cascade', select=True, readonly=True),                
                     'imballo':fields.many2one('conai.cod', 'Codice CONAI', required=True, ondelete='cascade', select=True, readonly=True),
                     'codice_iva':fields.many2one('account.tax', 'Codice Iva', readonly=False, required=True),                 
                     'peso':fields.float('Peso', digits=(12, 7)),
                     'totale_conai':fields.float('Totale Imponibile', digits_compute=dp.get_precision('Account')),
                               
                     }
    
    def agg_tot_conai(self, cr, uid, ids, context):
      if ids:
        #import pdb;pdb.set_trace()
        lines = self.pool.get('fiscaldoc.righe').search(cr, uid, [('name', '=', ids)])   # okkio dai per scontato di avere un solo documento sotto il culo
        idsd = self.search(cr, uid, [('name', '=', ids)])
        if idsd:
            ok = self.unlink(cr,uid,idsd) # cancella subito il castelletto esistente   
        riga_cast = {}
        for riga in self.pool.get('fiscaldoc.righe').browse(cr, uid, lines, context=context):
            if riga.cod_conai: # c'è il conai
                #import pdb;pdb.set_trace()
                par = [('name','=',riga.name.id),('imballo','=',riga.cod_conai.id),('codice_iva','=',riga.codice_iva.id)]
                id_cats = self.search(cr,uid,par)
                if id_cats:
                  for indice in id_cats: 
                    # esiste già un record simile e quindi aggiungo il totale
                    peso = self.browse(cr,uid,indice).peso+riga.peso_conai
                    totale_conai = self.browse(cr,uid,indice).totale_conai+riga.totale_conai
                    ok = self.write(cr,uid,indice,{'peso':peso,'totale_conai':totale_conai})
                else:
                    cast_riga = {
                                 'name':riga.name.id,
                                 'imballo':riga.cod_conai.id,
                                 'codice_iva':riga.codice_iva.id,
                                 'peso':riga.peso_conai,
                                 'totale_conai':riga.totale_conai,
                                 }
                    idcast = self.create(cr,uid,cast_riga)
        
        return True
    
conai_castelletto()



class FiscalDocIva(osv.osv):
    _inherit = "fiscaldoc.iva"
    
    def agg_righe_iva(self, cr, uid, ids, context):
        def get_perc_iva(self, cr, uid, ids, idiva, context):
            dati = self.pool.get('account.tax').read(cr, uid, [idiva], (['amount', 'type']), context=context)
            return dati[0]['amount']

        res = super(FiscalDocIva, self).agg_righe_iva(cr, uid, ids, context) # prima ricalcola il castelletto iva standard
        res = self.pool.get('conai.castelletto').agg_tot_conai(cr,uid,ids,context)
        conai_ids = self.pool.get('conai.castelletto').search(cr,uid,[('name','=',ids)])
        if conai_ids: #ci sono righe di castelletto conai
            for riga_cast in self.pool.get('conai.castelletto').browse(cr,uid,conai_ids):
                iva_id = self.pool.get("fiscaldoc.iva").search(cr,uid,[('name','=',riga_cast.name.id),('codice_iva','=',riga_cast.codice_iva.id)])
                if iva_id:  # somma il solo imponibile
                    iva={}
                    iva['imponibile']= self.pool.get("fiscaldoc.iva").browse(cr,uid,iva_id[0]).imponibile+riga_cast.totale_conai
                    ok = self.pool.get("fiscaldoc.iva").write(cr,uid,[iva_id[0]],iva)           
        # ora ricalcola l'imposta        
            righe_iva = self.pool.get("fiscaldoc.iva").search(cr,uid,[('name','=',ids)])            
            for rg_iva in self.pool.get("fiscaldoc.iva").browse(cr,uid,righe_iva):
                perc_iva = get_perc_iva(self, cr, uid, ids, rg_iva.codice_iva.id, context)
                imposta = rg_iva.imponibile * perc_iva
                imposta = arrot(cr,uid,imposta,dp.get_precision('Account'))
                ok =  self.pool.get("fiscaldoc.iva").write(cr,uid,[rg_iva.id],{'imposta':imposta})
            
            
FiscalDocIva()
