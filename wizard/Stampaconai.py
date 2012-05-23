# -*- encoding: utf-8 -*-

import wizard
import decimal_precision as dp
import pooler
import time
from tools.translate import _
from osv import osv, fields
from tools.translate import _


class tempstatistiche_conai(osv.osv):
    def _pulisci(self,cr,uid,context):
        ids = self.search(cr,uid,[])
        ok = self.unlink(cr,uid,ids,context)
        return True
    
    
    _name = 'tempstatistiche.conai'
    _description = 'temporaneo di stampa conai periodico'
    _columns = {'p_dadata': fields.date('Da Data Documento' ),
                'p_adata': fields.date('A Data Documento'),
                'doc_id':fields.many2one('fiscaldoc.header'),
                'documento':fields.char('NomeDoc', size=20),
                'castelletto_id':fields.many2one('conai.castelletto'),
                'prezzo':fields.float('Prezzo', digits=(25,3)),
                'peso': fields.float('peso', digits=(25,3)),
                'contributo':fields.float('contributo', digits=(25,3)),
                'codice_conai':fields.char('NomeDoc', size=20),
#                'contropartita':fields.char('Contropartita', size=20),
                }
    
    def carica_doc(self, cr,uid,parametri,context):
        ok = self._pulisci(cr, uid, context)
        testa_obj = self.pool.get('fiscaldoc.header')
        partner_obj = self.pool.get('res.partner')
        conai = self.pool.get('conai.castelletto')
        filtro1 = [('tipo_documento', 'in', ('FA','FI','FD','NC','ND'))] #AGGIUNGERE NOTE CREDITO E NOTE DEBITO
        idsTipoDoc = self.pool.get('fiscaldoc.causalidoc').search(cr, uid, filtro1)
        idsTipoDoc = tuple(idsTipoDoc)
        filtro2 = [('data_documento','<=',parametri.adata ),('data_documento','>=', parametri.dadata), ('tipo_doc', 'in', idsTipoDoc)]
        doc_ids = testa_obj.search(cr, uid, filtro2)
        if doc_ids:
            for documento in testa_obj.browse(cr,uid, doc_ids):
                if not documento.esenzione_conai:
                    
                    cerca = [('name', '=', documento.id)]
                    conai_id = conai.search(cr, uid, cerca)
                    if conai_id:
                        #import pdb;pdb.set_trace()
                        cast_obj = conai.browse(cr, uid, conai_id[0])
                        if documento.tipo_doc.tipo_documento == 'NC' or documento.tipo_doc.tipo_documento == 'ND':
                            riga_wr = {'p_dadata' : parametri.dadata,
                                   'p_adata' : parametri.adata,
                                   'doc_id':documento.id,
                                   'documento':documento.name,
                                   'castelletto_id':cast_obj.id,
                                   'prezzo':cast_obj.imballo.valore*-1,                                 
                                   'peso':cast_obj.peso,
                                   'contributo':cast_obj.totale_conai*-1,
                                   'codice_conai':cast_obj.imballo.descrizione
                                   }
                            ok = self.create(cr, uid, riga_wr)
                        else:
                            riga_wr = {'p_dadata' : parametri.dadata,
                                   'p_adata' : parametri.adata,
                                   'doc_id':documento.id,
                                   'documento':documento.name,
                                   'castelletto_id':cast_obj.id,
                                   'prezzo':cast_obj.imballo.valore,                                 
                                   'peso':cast_obj.peso,
                                   'contributo':cast_obj.totale_conai,
                                   'codice_conai':cast_obj.imballo.descrizione
                                   }
                            ok = self.create(cr, uid, riga_wr)
            return True
                            
                        
                            
        
tempstatistiche_conai()
  

class stampa_conai(osv.osv_memory):
    _name = 'stampa.conai'
    _description = 'funzioni necessarie alla stampa periodica CONAI'
    _columns = {
                'dadata': fields.date('Da Data Documento', required=True ),
                'adata': fields.date('A Data Documento', required=True),
    }
        
    def _build_contexts(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        result = {}
        result = {'dadata':data['form']['dadata'], 'adata':data['form']['adata'], }
                
        return result
  
    def _print_report(self, cr, uid, ids, data, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
        pool = pooler.get_pool(cr.dbname)
        #fatture = pool.get('fiscaldoc.header')
        #active_ids = context and context.get('active_ids', [])
        #Primo = True
        #if active_ids:
        #    for doc in fatture.browse(cr, uid, active_ids, context=context):
        #        if Primo:
        #            Primo = False
        #            IdTipoSta = doc.tipo_doc.id
        #            TipoStampa = doc.tipo_doc.tipo_modulo_stampa.report_name
        #        #import pdb;pdb.set_trace()
        #        else:
        #          if IdTipoSta <> doc.tipo_doc.id:
        #              raise osv.except_osv(_('ERRORE !'),_('Devi Selezionare documenti con la stessa Causale Documento'))
	
	TipoStampa = "Conai"
        return {
                'type': 'ir.actions.report.xml',
                'report_name': TipoStampa,
                'datas': data,
            }
 

    def check_report(self, cr, uid, ids, context=None):
        #import pdb;pdb.set_trace()
        if context is None:
            context = {}
            
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['dadata',  'adata'])[0]
        used_context = self._build_contexts(cr, uid, ids, data, context=context)
        data['form']['parameters'] = used_context
        parametri = self.browse(cr,uid,ids)[0]
        
        ok = self.pool.get('tempstatistiche.conai').carica_doc(cr,uid,parametri,context)
        return self._print_report(cr, uid, ids, data, context=context)
  
    def view_init(self, cr, uid, fields_list, context=None):
        # import pdb;pdb.set_trace()
        res = super(stampa_fiscaldoc, self).view_init(cr, uid, fields_list, context=context)

        return res
    
             
    def  default_get(self, cr, uid, fields, context=None):
        #import pdb;pdb.set_trace()
        #pool = pooler.get_pool(cr.dbname)
        #fatture = pool.get('fiscaldoc.header')
        #active_ids = context and context.get('active_ids', [])
        #Primo = True
        #if active_ids:
        #    for doc in fatture.browse(cr, uid, active_ids, context=context):
        #        if Primo:
        #            Primo = False
        #            DtIni = doc['data_documento']
        #            NrIni = doc['name']
        #            danr = doc['id']
        #          #import pdb;pdb.set_trace()
        #        DtFin = doc['data_documento']
        #        NrFin = doc['name']
        #        anr = doc['id']
        
         #{'dadata':DtIni,'adata':DtFin}
        return {}

    

    
stampa_conai()