# -*- encoding: utf-8 -*-
import netsvc
import pooler, tools
import math

from tools.translate import _

from osv import fields, osv

class partner(osv.osv):

    _inherit = 'res.partner'
    
    _columns = {                            
                'esenzione':fields.many2one('conai.esenzioni', 'Tipo di Esenzione Conai'),
                'perc':fields.float('Percentuale di Esenzione', required=False) ,
                'dati':fields.char('Dati di Esenzione', size=100),
                'scad_esenzione': fields.date('Scadenza Esenzione', required=False, readonly=False),
                }
partner()
