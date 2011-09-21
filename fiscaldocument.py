 #-*- encoding: utf-8 -*-
import netsvc
import pooler, tools
import math
import decimal_precision as dp
from tools.translate import _

from osv import fields, osv

class FiscalDocRighe(osv.osv):
     
<<<<<<< HEAD
     _inherit = 'fiscaldoc.righe'
    
     _columns = {
               'peso_conai':fields.float('Peso Conai', digits=(2, 7)),
               'totale_conai':fields.float('Totale Conai', digits=(2, 7)),
               }
   
          
     def onchange_articolo(self, cr, uid, ids, product_id, listino_id, qty, partner_id, data_doc, uom):
         #import pdb;pdb.set_trace()
         ## ora faccio delle modifiche e faccio un commit ed un push
## modifiche ricevute passo e chiudo
## e mò basta
         res = super(FiscalDocRighe, self).onchange_articolo(cr, uid, ids, product_id, listino_id, qty, partner_id, data_doc, uom)
         v = {}
         z = {}
         if product_id:
             partner = self.pool.get('res.partner').browse(cr, uid, [partner_id])[0]
             product_obj = self.pool.get('product.product')
             riga_art = product_obj.browse(cr, uid, product_id)   
             art_obj = self.pool.get("product.product").browse(cr, uid, [product_id])[0]
             conai_obj = art_obj.product_tmpl_id.conai # Verifica la presenza del CODICE CONAI
             dati_prz = self.determina_prezzo_sconti(cr, uid, ids, product_id, listino_id, qty, partner_id, uom, data_doc)
             righe_tasse_articolo = self.pool.get('account.fiscal.position').map_tax(cr, uid, False, riga_art.taxes_id)
             data = partner.scad_esenzione
         
             #import pdb;pdb.set_trace()
             
             v['peso_conai'] = 0
             v['totale_conai'] = 0
             v['descrizione_riga'] = riga_art.name
             v['product_prezzo_unitario'] = dati_prz['prezzo']
             v['discount_riga'] = dati_prz['sconto']
             v['sconti_riga'] = dati_prz['StringaSconto']       
             v['prezzo_netto'] = self.calcola_netto(v['product_prezzo_unitario'], v['discount_riga']) 
             v['totale_riga'] = self.totale_riga(qty, v['prezzo_netto'])
             v['product_uom'] = riga_art.uom_id.id
             #v['contropartita']= riga_art.property_account_income
             v['codice_iva'] = righe_tasse_articolo[0]
             if riga_art.property_account_income:
                    v['contropartita'] = riga_art.property_account_income
             else:
                    v['contropartita'] = riga_art.categ_id.property_account_income_categ.id
             if conai_obj:
                 prz_conai = art_obj.product_tmpl_id.conai.valore
                 if data:
                     if data > data_doc:
                         if partner.perc <> 0:       
                             #import pdb;pdb.set_trace()
                             v['peso_conai'] = art_obj.peso * qty
                             prz_conai = prz_conai * partner.perc / 100
                             v['totale_conai'] = prz_conai * art_obj.peso * qty
                             v['totale_riga'] = v['totale_riga'] + v['totale_conai']
                     else:  
                         #import pdb;pdb.set_trace()
                         raise osv.except_osv(_('ATTENZIONE !'), _("L'Esenzione del Cliente è scaduta"))
                         v['peso_conai'] = art_obj.peso * qty
                         v['totale_conai'] = prz_conai * art_obj.peso * qty
                         v['totale_riga'] = v['totale_riga'] + v['totale_conai'] 
                 else:
                     v['peso_conai'] = art_obj.peso * qty
                     v['totale_conai'] = prz_conai * art_obj.peso * qty
                     v['totale_riga'] = v['totale_riga'] + v['totale_conai']   
                         
             return {'value':v}             
             
     
     
#Da SISTEMARE ....     
     def on_change_qty(self, cr, uid, ids, product_id, listino_id, qty, partner_id, uom, data_doc): #

         res = super(FiscalDocRighe, self).on_change_qty(cr, uid, ids, product_id, listino_id, qty, partner_id, uom, data_doc)
         v = {}
         if qty and product_id and listino_id:
             #import pdb;pdb.set_trace()
             product_obj = self.pool.get('product.product')
             riga_art = product_obj.browse(cr, uid, product_id)   
             art_obj = self.pool.get("product.product").browse(cr, uid, [product_id])[0]
             prz_conai = art_obj.conai.valore
             dati_prz = self.determina_prezzo_sconti(cr, uid, ids, product_id, listino_id, qty, partner_id, uom, data_doc)
             righe_tasse_articolo = self.pool.get('account.fiscal.position').map_tax(cr, uid, False, riga_art.taxes_id)
             partner = self.pool.get('res.partner').browse(cr, uid, [partner_id])[0]
             data = partner.scad_esenzione
             v['product_prezzo_unitario'] = dati_prz['prezzo']
             v['descrizione_riga'] = riga_art.name
             v['discount_riga'] = dati_prz['sconto']
             v['sconti_riga'] = dati_prz['StringaSconto']       
             v['prezzo_netto'] = self.calcola_netto(v['product_prezzo_unitario'], v['discount_riga']) 
             v['totale_riga'] = self.totale_riga(qty, v['prezzo_netto'])
             v['product_uom'] = riga_art.uom_id.id
             #v['contropartita']= riga_art.property_account_income
             v['codice_iva'] = righe_tasse_articolo[0]   
             if riga_art.property_account_income:
                    v['contropartita'] = riga_art.property_account_income
             else:
                    v['contropartita'] = riga_art.categ_id.property_account_income_categ.id
             if prz_conai:
                 if data > data_doc:
                     if partner.perc:
                         v['peso_conai'] = art_obj.peso * qty
                         prz_conai = prz_conai * partner.perc / 100
                         v['totale_conai'] = prz_conai * art_obj.peso * qty
                         v['totale_riga'] = v['totale_riga'] + v['totale_conai']
                     else:
                         raise osv.except_osv(_('ATTENZIONE !'), _("L'Esenzione del Cliente è scaduta"))
                         v['peso_conai'] = art_obj.peso * qty
                         v['totale_conai'] = prz_conai * art_obj.peso * qty
                         v['totale_riga'] = v['totale_riga'] + v['totale_conai']  
             return {'value':v}

FiscalDocRighe()

class FiscaldocHeader(osv.osv):
      _inherit = "fiscaldoc.header"
      
      def write(self, cr, uid, ids, vals, context=None):
        res = super(FiscaldocHeader, self).write(cr, uid, ids, vals, context=context)
        if res:
            testata = self.browse(cr, uid, ids)[0]
            lines = self.pool.get('conai.castelletto').search(cr, uid, [("name", "=", testata.id)])
            ok = self.pool.get('conai.castelletto').unlink(cr, uid, lines)
       
                
=======
     _inherit='fiscaldoc.righe'
    
     _columns ={
               'peso_conai':fields.float('Peso Conai',digits=(2,7)),             
               'totale_conai':fields.float('Totale Conai',digits=(2,7)),
               }
   
          
     def onchange_articolo(self, cr, uid, ids, product_id,listino_id,qty,partner_id,data_doc,uom):
         #import pdb;pdb.set_trace()
         res = super(FiscalDocRighe, self).onchange_articolo(cr, uid, ids, product_id,listino_id,qty,partner_id,data_doc,uom)
         v={}
         z={}
         if product_id:
             
             partner = self.pool.get('res.partner').browse(cr,uid,[partner_id])[0]
             product_obj = self.pool.get('product.product')
             riga_art = product_obj.browse(cr, uid, product_id)   
             art_obj= self.pool.get("product.product").browse(cr,uid,[product_id])[0]
             prz_conai = art_obj.codice.valore
             dati_prz = self.determina_prezzo_sconti(cr, uid, ids,product_id,listino_id,qty,partner_id,uom,data_doc)
             righe_tasse_articolo = self.pool.get('account.fiscal.position').map_tax(cr, uid, False, riga_art.taxes_id)
             partner = self.pool.get('res.partner').browse(cr,uid,[partner_id])[0]
             v['peso_conai']=0
             v['totale_conai']=0
             v['descrizione_riga']=riga_art.name
             v['product_prezzo_unitario'] = dati_prz['prezzo']
             v['discount_riga'] =  dati_prz['sconto']
             v['sconti_riga'] =  dati_prz['StringaSconto']       
             v['prezzo_netto']=self.calcola_netto(v['product_prezzo_unitario'],v['discount_riga']) 
             v['totale_riga']=self.totale_riga(qty, v['prezzo_netto'])
             v['product_uom']= riga_art.uom_id.id
             #v['contropartita']= riga_art.property_account_income
             v['codice_iva']= righe_tasse_articolo[0]
             if riga_art.property_account_income:
                    v['contropartita']= riga_art.property_account_income
             else:
                    v['contropartita']= riga_art.categ_id.property_account_income_categ.id
             if prz_conai:
                 if partner.perc:
                     #import pdb;pdb.set_trace()
                     v['peso_conai']=art_obj.peso * qty
                     prz_conai = prz_conai*partner.perc/100
                     v['totale_conai']= prz_conai * art_obj.peso * qty
                     
                 else:
                     v['peso_conai'] =  art_obj.peso * qty
                     v['totale_conai'] = prz_conai * art_obj.peso * qty 
                        
                         
         return {'value':v}
     
     
     
     def on_change_qty(self, cr, uid, ids,product_id,listino_id,qty,partner_id,uom,data_doc):

         res = super(FiscalDocRighe, self).on_change_qty(cr, uid, ids,product_id,listino_id,qty,partner_id,uom,data_doc)
         v={}
         if qty and product_id and listino_id:
             
             riga_art = product_obj.browse(cr, uid, product_id)   
             art_obj= self.pool.get("product.product").browse(cr,uid,[product_id])[0]
             dati_prz = self.determina_prezzo_sconti(cr, uid, ids,product_id, listino_id, qty, partner_id, uom, data_doc)
             righe_tasse_articolo = self.pool.get('account.fiscal.position').map_tax(cr, uid, False, riga_art.taxes_id)
             #partner = self.pool.get('res.partner').browse(cr,uid,[partner_id])[0]
             v['product_prezzo_unitario'] = dati_prz['prezzo']
             v['descrizione_riga']=riga_art.name
             v['discount_riga'] =  dati_prz['sconto']
             v['sconti_riga'] =  dati_prz['StringaSconto']       
             v['prezzo_netto']=self.calcola_netto(v['product_prezzo_unitario'],v['discount_riga']) 
             v['totale_riga']=self.totale_riga(qty, v['prezzo_netto'])
             v['product_uom']= riga_art.uom_id.id
             #v['contropartita']= riga_art.property_account_income
             v['codice_iva']= righe_tasse_articolo[0]   
             if riga_art.property_account_income:
                    v['contropartita']= riga_art.property_account_income
             else:
                    v['contropartita']= riga_art.categ_id.property_account_income_categ.id
             if prz_conai:
                 if partner.perc:
                     #
                     v['peso_conai']=art_obj.peso * qty
                     prz_conai = prz_conai*partner.perc/100
                     v['totale_conai']= prz_conai * art_obj.peso * qty
                 else:
                     v['peso_conai'] =  art_obj.peso * qty
                     v['totale_conai'] = prz_conai * art_obj.peso * qty  
         return {'value':v}

FiscalDocRighe()

class FiscalDocIva(osv.osv):
      _inherit="fiscaldoc.iva"
      
      
      
      def agg_righe_iva(self,cr, uid, ids,context):


        
        def get_perc_iva(self,cr, uid, ids,idiva,context):
            dati  = self.pool.get('account.tax').read(cr, uid, [idiva],(['amount','type']), context=context)
            return dati[0]['amount']
        
        res=super(FiscalDocIva, self).agg_righe_iva(cr, uid, ids, context)
        
   
        lines = self.pool.get('fiscaldoc.righe').search(cr, uid, [('name', '=', ids)])      
        righe_iva ={}
        for riga in self.pool.get('fiscaldoc.righe').browse(cr, uid, lines, context=context):
          if riga.codice_iva.id:
            if righe_iva.get(riga.codice_iva.id,False):
                # esiste gia la riga con questo codice
                dati_iva = righe_iva[riga.codice_iva.id]
                dati_iva['imponibile']= dati_iva['imponibile']+riga.totale_riga
                righe_iva[riga.codice_iva.id]=dati_iva
            else:
                dati_iva ={'imponibile':riga.totale_riga}
                righe_iva.update({riga.codice_iva.id:dati_iva})
                
        for riga in self.pool.get('fiscaldoc.righe').browse(cr, uid, lines , context=context):
            #conai = self.pool.get('fiscaldoc.righe').browse(cr, uid, id)
            if riga.totale_conai:
                if riga.codice_iva.id:
                    dati_iva = righe_iva[riga.codice_iva.id]
                    dati_iva['imponibile']= dati_iva['imponibile']+riga.totale_conai
                    righe_iva[riga.codice_iva.id]=dati_iva
                else:
                    dati_iva ={'imponibile':riga.totale_riga}
                    righe_iva.update({riga.codice_iva.id:dati_iva})
        
        for rg_iva in righe_iva:
            perc_iva = get_perc_iva(self,cr,uid,ids,rg_iva,context)
            dati_iva = righe_iva[rg_iva]
            dati_iva.update({'imposta':dati_iva['imponibile']*perc_iva})
            righe_iva[rg_iva]= dati_iva 
            
        # ORA SCRIVE I RECORD CANCELLA COMUNQUE TUTTE LE REGHE E POI LE RICREA AGGIORNATE QUESTO SALVA LA CONDIZIONE IN CUI SCOMPAIA COMPLETAMENTE 
        # UNA RIGA DI ALIQUOTA IVA
        lines = self.pool.get('fiscaldoc.iva').search(cr, uid, [('name', '=', ids)])
        if lines:
            res = self.pool.get('fiscaldoc.iva').unlink(cr, uid, lines, context) 
        else:
            # E' LA CREATE QUINDI CREA LE SCADENZE 
            totaledoc = 0
            for riga in righe_iva:
                totaledoc+= righe_iva[riga]['imponibile']+righe_iva[riga]['imposta']
            
            ok = self.pool.get('fiscaldoc.scadenze').agg_righe_scad(cr, uid,ids,totaledoc,context)
        
>>>>>>> 458bcde7e624a5f78113ce16df60e6f42bc865cf
        # QUI CREA IL CASTELLETTO CONAI ELENCANDO I TIPI DI IMBALLO DELLE VARIE RIGHE
        # E LE SCRIVE IN UNA TABELLA APPOSITA
        #import pdb;pdb.set_trace()
        linee = self.pool.get('fiscaldoc.righe').search(cr, uid, [('name', '=', ids)])
        for righe in self.pool.get('fiscaldoc.righe').browse(cr, uid, linee , context=context):
    
              
<<<<<<< HEAD
              record = {
                      'name': righe.name.id,
                      'imballo': righe.product_id.conai.id,
                      'desc': righe.product_id.conai.descrizione,
=======
              record={
                      'name': righe.name.name,
                      'codice_conai': righe.product_id.codice.name,
                      'desc': righe.product_id.codice.descrizione,
>>>>>>> 458bcde7e624a5f78113ce16df60e6f42bc865cf
                      'peso': righe.peso_conai,
                      'totale_conai': righe.totale_conai,
                      
                      }
<<<<<<< HEAD
              res = self.pool.get('conai.castelletto').create(cr, uid, record)
         
        
=======
              res =self.pool.get('conai.cast').create(cr, uid, record)
         
        
        
        
        for riga in righe_iva:
            record={
                    'name':ids[0],
                    'codice_iva':riga,
                    'imponibile':righe_iva[riga]['imponibile'],
                    'imposta':righe_iva[riga]['imposta'],
                    }
            res = self.pool.get('fiscaldoc.iva').create(cr, uid, record)
>>>>>>> 458bcde7e624a5f78113ce16df60e6f42bc865cf
          
        return True

        
       
          
    
<<<<<<< HEAD
FiscaldocHeader()
=======
FiscalDocIva()                        
              
              
              
           
        


>>>>>>> 458bcde7e624a5f78113ce16df60e6f42bc865cf
