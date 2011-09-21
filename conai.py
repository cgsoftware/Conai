# -*- encoding: utf-8 -*-

import netsvc
import pooler, tools
import math

from tools.translate import _

from osv import fields, osv

import wizard
import decimal_precision as dp
import time


 
class conai_cod(osv.osv):
   _name = "conai.cod"
   _description = "Codici CONAI"
   _columns = {
             'name':fields.char('Codice Conai', size=15, required=True),
             'descrizione':fields.char('Descrizione Imballo', size=100, required=True),
             'valore':fields.float('Valore Unitario ', digits=(2, 7), required=True),
                }
conai_cod()

class conai_esenzioni(osv.osv):
    _name = "conai.esenzioni"
    _description = "Esenzioni"
    _columns = {
              'name':fields.char('Codice Esenzione', size=10, required=True),
              'descrizione':fields.char('Descrizione Esenzione', size=50, require=True),
              }    
conai_esenzioni()

class conai_castelletto(osv.osv):
    _name = "conai.castelletto"
    _description = "Castelletto CONAI"      
    _columns = {
                     'name': fields.many2one('fiscaldoc.header', 'Numero Documento', required=True, ondelete='cascade', select=True, readonly=True),
                     
                     'imballo':fields.many2one('conai.cod', 'Codice CONAI', required=True, ondelete='cascade', select=True, readonly=True),
                     
                     'peso':fields.float('Peso', digits=(12, 2)),
                     'totale_conai':fields.float('Totale Imponibile', digits=(12, 2)),
                               
                     }
conai_castelletto()
class conai_cod(osv.osv):
   _name = "conai.cod"
   _description = "Codici CONAI"
   _columns = {
             'name':fields.char('Codice Conai', size=15, required=True),
             'descrizione':fields.char('Descrizione Imballo', size=100, required=True),
             'valore':fields.float('Valore Unitario ', digits=(2, 7), required=True),
             }
conai_cod()

class esenzione(osv.osv):
    _name = "conai.es"
    _description = "Esenzioni"
    _columns = {
              'name':fields.char('Codice Esenzione', size=10, required=True),
              'descrizione':fields.char('Descrizione Esenzione', size=50, require=True)
              }    
esenzione()

class cast(osv.osv):
    _name = "conai.cast"
    _description = "Castelletto CONAI"      
    _columns = {
                     'name': fields.many2one('fiscaldoc.header', 'Numero Documento', required=True, ondelete='cascade', select=True, readonly=True),
                     #'name': fields.char('Descrzione', size=50),
                     'codice_conai':fields.many2one('conai.cod', 'Codice CONAI', required=True, ondelete='cascade', select=True, readonly=True),
                     #'desc':fields.char('Descrzione', size=50),
                     'peso':fields.float('Peso', digits=(12, 2)),
                     'totale_conai':fields.float('Totale Imponibile', digits=(12, 2)),
                     }
cast()

