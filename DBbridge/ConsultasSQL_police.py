from PostgreSQL.ConexionSQL import ConexionSQL 

class ConsultasSQL_police(object):
	"""docstring for ConsultasSQL"""
	def __init__(self):
		super(ConsultasSQL_police, self).__init__()
		conSql = ConexionSQL()
		self.conn_sql = conSql.getConexion_police()
		self.cur_sql = conSql.getCursor_police()

	def setFinishedTask(self, id_task):
		query = "UPDATE policia_tarea SET fin=CURRENT_TIMESTAMP WHERE id=%s;"
		try:
			self.cur_sql.execute(query, [id_task, ])
			self.conn_sql.commit()

			return True
		except Exception, e:
			print str(e)
			return False
