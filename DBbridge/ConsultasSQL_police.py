from PostgreSQL.ConexionSQL import ConexionSQL 

class ConsultasSQL_police(object):
	"""docstring for ConsultasSQL"""
	def __init__(self):
		super(ConsultasSQL_police, self).__init__()
		self.conSql = ConexionSQL()
		self.cur_sql = None
		self.conn_sql = None

	def setFinishedTask(self, id_task):
		query = "UPDATE policia_tarea SET fin=CURRENT_TIMESTAMP WHERE id=%s;"
		try:
			self.cur_sql = self.conSql.getCursor_police()
			self.conn_sql = self.conSql.getConexion_police()
			
			self.cur_sql.execute(query, [id_task, ])
			self.conn_sql.commit()

			return True
		except Exception, e:
			print str(e)
			return False

	def getSendEmailFromTask(self, id_task):
		query = "SELECT enviar_email FROM policia_tarea WHERE id=%s;"
		try:
			self.cur_sql = self.conSql.getCursor_police()

			self.cur_sql.execute(query, [id_task, ])
			row = self.cur_sql.fetchone()
			return row[0]
		except Exception, e:
			return False

	def getIdUserFromTask(self, id_task):
		query = "SELECT usuario_id FROM policia_tarea WHERE id=%s;"
		try:
			self.cur_sql = self.conSql.getCursor_police()

			self.cur_sql.execute(query, [id_task, ])
			row = self.cur_sql.fetchone()
			return row[0]
		except Exception, e:
			return False

	def getUsernameFromTask(self, id_task):
		query = "SELECT username FROM policia_tarea WHERE id=%s;"
		try:
			self.cur_sql = self.conSql.getCursor_police()

			self.cur_sql.execute(query, [id_task, ])
			row = self.cur_sql.fetchone()
			return row[0]
		except Exception, e:
			return False

	def getTextFromTask(self, id_task):
		query = "SELECT texto FROM policia_tarea WHERE id=%s;"
		try:
			self.cur_sql = self.conSql.getCursor_police()

			self.cur_sql.execute(query, [id_task, ])
			row = self.cur_sql.fetchone()
			return row[0]
		except Exception, e:
			return False

	def getTipoTarea(self, id_task):
		query = "SELECT tipo FROM policia_tarea WHERE id=%s;"
		try:
			self.cur_sql = self.conSql.getCursor_police()

			self.cur_sql.execute(query, [id_task, ])
			row = self.cur_sql.fetchone()
			return row[0]
		except Exception, e:
			return False

	def getEmailFromUser(self, id_user):
		query = "SELECT email FROM policia_usuario WHERE id=%s;"
		try:
			self.cur_sql = self.conSql.getCursor_police()

			self.cur_sql.execute(query, [id_user, ])
			row = self.cur_sql.fetchone()
			return row[0]
		except Exception, e:
			return False
