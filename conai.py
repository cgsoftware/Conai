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
    _description = "Esenzioni Conai"
    _columns = {
              'name':fields.char('Codice Esenzione', size=10, required=True),
              'descrizione':fields.char('Descrizione Esenzione', size=50, require=True),
              }    
conai_esenzioni()




