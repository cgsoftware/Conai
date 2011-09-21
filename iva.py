 #-*- encoding: utf-8 -*-
import netsvc
import pooler, tools
import math
import decimal_precision as dp
from tools.translate import _

from osv import fields, osv

<<<<<<< HEAD
class FiscalDocIva(osv.osv):
      _inherit="fiscaldoc.iva"
      
      
      
      def agg_righe_iva(self,cr, uid, ids,context):


=======
class ivaconai(osv.osv):
     _name="conai.iva"
     _description="Castelletto IVA CONAI"
     _columns ={
               'name': fields.many2one('fiscaldoc.header', 'Numero Documento', required=True, ondelete='cascade', select=True, readonly=True),
               'codice_iva':fields.many2one('account.tax', 'Codice Iva', readonly=False, required=True),
               'imp_conai':fields.float("Totale Imponibile",digits=(12,2)),             
               'imposta':fields.float("Imposta",digits=(12,2)),    
               }     
     def agg_righe_iva(self,cr, uid, ids,context):
>>>>>>> 458bcde7e624a5f78113ce16df60e6f42bc865cf
        
        def get_perc_iva(self,cr, uid, ids,idiva,context):
            dati  = self.pool.get('account.tax').read(cr, uid, [idiva],(['amount','type']), context=context)
            return dati[0]['amount']
<<<<<<< HEAD
        
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
                    dati_iva['imponibile']= dati_iva['imponibile']
                    righe_iva[riga.codice_iva.id]=dati_iva
                else:
                    dati_iva ={'imponibile':riga.totale_riga}
                    righe_iva.update({riga.codice_iva.id:dati_iva})
        
        for rg_iva in righe_iva:
            perc_iva = get_perc_iva(self,cr,uid,ids,rg_iva,context)
            dati_iva = righe_iva[rg_iva]
            dati_iva.update({'imposta':dati_iva['imponibile']*perc_iva})
            righe_iva[rg_iva]= dati_iva 
        
        #import pdb;pdb.set_trace()    
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
        
       
        
        linee = self.pool.get('fiscaldoc.righe').search(cr, uid, [('name', '=', ids)])
        for righe in self.pool.get('fiscaldoc.righe').browse(cr, uid, linee , context=context):
         for riga in righe_iva:
             record={
                     'name':ids[0],
                     'codice_iva':riga,
                     'imponibile':righe_iva[riga]['imponibile'],
                     'imposta':righe_iva[riga]['imposta'],
                     }
             res = self.pool.get('fiscaldoc.iva').create(cr, uid, record)
          
        return True

        
       
          
    
FiscalDocIva() 
=======
        import pdb;pdb.set_trace()
        # PRIMA SCORRE TUTTE LE RIGHE DI ARTICOLI
        lines = self.pool.get('fiscaldoc.righe').search(cr, uid, [('name', '=', ids)])      
        righe_conai ={}
        for riga in self.pool.get('fiscaldoc.righe').browse(cr, uid, lines, context=context):
            if righe_conai.get(riga.codice_iva.id,False):
                # esiste gia la riga con questo codice
                dati_iva = righe_iva[riga.codice_iva.id]
                dati_iva['totale_conai']= dati_iva['totale_conai']+riga.totale_riga
                righe_conai[riga.codice_iva.id]=dati_iva
            else:
                dati_iva ={'imponibile':riga.totale_riga}
                righe_conai.update({riga.codice_iva.id:dati_iva}) 
        # QUI DEVE CALCOLARE LE POSIZIONI IVA DI TUTTE LE SPESE ACCESSORIE
        for rg_iva in righe_conai:
            perc_iva = get_perc_iva(self,cr,uid,ids,rg_iva,context)
            dati_iva = righe_conai[rg_iva]
            dati_iva.update({'imposta':dati_iva['imp_conai']*perc_iva})
            righe_conai[rg_iva]= dati_iva   
           
        # ORA SCRIVE I RECORD CANCELLA COMUNQUE TUTTE LE REGHE E POI LE RICREA AGGIORNATE QUESTO SALVA LA CONDIZIONE IN CUI SCOMPAIA COMPLETAMENTE 
        # UNA RIGA DI ALIQUOTA IVA
        lines = self.pool.get('conai.iva').search(cr, uid, [('name', '=', ids)])
        if lines:
            res = self.pool.get('conai.iva').unlink(cr, uid, lines, context) 
        else:
            # E' LA CREATE QUINDI CREA LE SCADENZE 
            totaledoc = 0
            for riga in righe_conai:
                totaledoc+= righe_conai[riga]['imp_conai']+righe_conai[riga]['imposta']
            
            #ok = self.pool.get('fiscaldoc.scadenze').agg_righe_scad(cr, uid,ids,totaledoc,context)
         
        for riga in righe_conai:
            record={
                    'name':ids[0],
                    'codice_iva':riga,
                    'imp_conai':righe_conai[riga]['imponibile'],
                    'imposta':righe_conai[riga]['imposta'],
                    }
            res = self.pool.get('conai.iva').create(cr, uid, record)
          
        return True
ivaconai()
>>>>>>> 458bcde7e624a5f78113ce16df60e6f42bc865cf
