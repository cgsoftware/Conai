     def cast_conai(self,cr, uid, ids,context):
          import pdb;pdb.set_trace()
          _name="conai.cast"
          _description="Codici CONAI"      
          _columns ={
                     'name': fields.many2one('fiscaldoc.header', 'Numero Documento', required=True, ondelete='cascade', select=True, readonly=True),
                     'codice_conai':fields.many2one('conai.cod', 'Codice Conai', readonly=False, required=True),
                     'totale conai':fields.float("Totale Imponibile",digits=(12,2)),             
                     }
          _rec_name='name'
          
          lines = self.pool.get('fiscaldoc.righe').search(cr, uid, [('name', '=', ids)])
          v={}
          for riga in self.pool.get('fiscaldoc.righe').browse(cr, uid, lines , context=context):
              
              v = riga
          
          return {'value':v}