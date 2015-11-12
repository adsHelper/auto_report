# -*- coding: utf-8 -*-
import MySQLdb
import time

class MySQL(object):
	"""对MySQL常用函数进行封装"""
	
	error_code = '' #MySQL错误码
	_instance  = None #本类实例
	_conn      = None #数据库conn
	_cur       = None #游标

	_TIMEOUT =30 #默认超时30s
	_timecount = 0

	def __init__(self,dbconfig):
		u'构造器：根据数据库连接参数，创建MySQL连接'
		try:
			self._conn = MySQLdb.connect(host=dbconfig['host'],
						   port = dbconfig['port'],
						   user = dbconfig['user'],
						   passwd = dbconfig['passwd'],
						   db = dbconfig['db'],
						   charset = dbconfig['charset'])
		except Exception, e:
			self.error_code = e.args[0]
			error_msg = 'MySQL error!',e.args[0],e.args[1]
			print error_msg

		#如果没有超过预设超时时间，则再次尝试连接
		if self._timecount < self._TIMEOUT:
			interval = 5
			self._timecount += interval
			time.sleep(interval)
			return self.__init__(dbconfig)
		else:	
			raise Exception(error_msg)

		self._cur = self._conn.cursor()
		self._instance = MySQLdb

	def query(self,table,field,param):
		"""query MySQL 
		Args:
			table: 表名 string
			field: 字段名 string 以逗号作为分隔 eg：username,passwd
			param: 条件参数 dict 
		Returns:
		"""
		try:
			condition = ''
			cmd = "select "+ field + "from" + table
			length = len(param)
			if length > 0:
				condition = " where "
				value = "("
				for key in param:
					condition = condition + key + "=%s and "
					value = value + param[key] +","
				condition = condition[0:len(condition) - 5]
				value = value[0:len(value)-2] + ")"
				cmd = "select "+ field + "from" + table + condition
			result = self._cur.execute(cmd,value)
		except Exception, e:
			self.error_code = e.args[0]
			print "数据库错误代码:",e.args[0],e.args[1]
			result = False
		return result

	def update(self,table,param,con):
		try:
			cmd = " update "+table + "set "
			condition =""
			field = ""
			value = "("
			param_length = len(param)
			con_length = len(con)
			if param_length > 0:
				for key in param:
					field=field + key + "=%s ,"
					value = value + param[key]+","
				field = field[0:len(field)-5]
				value = value[0:len(value)-2]
				cmd = cmd + field 
			if con_length > 0:
				condition = " where "
				for key in con:
					condition = condition + key + "=%s and "
					value = value + ","+ con[key] 
				condition = condition[0:len(condition)-5]
				cmd = cmd + field 
			value=value+")"
			result = self._cur.execute(cmd,value)
		except Exception, e:
			self.error_code = e.args[0]
			print "数据库错误代码:",e.args[0],e.args[1]
			result = False
		return result

	def insert(self,table,param):
		try:
			cmd = "insert into "+table+" ("
			length = len(param)
			field = ""
			key_field = "("
			value="("
			if length > 0:
				for key in param:
					field = field + key+","
					key_field = key_field + "%s,"
					value = value +param[field]+","
				field = field[0:len(field)-2]+")"
				key_field = key_field[0:len(key_field)-2]+")"
				value = value[0:len(value)-2]+")"
				cmd = cmd+field+" values "+key_field
				result = self._cur.execute(cmd,value)
		except Exception, e:
			self.error_code = e.args[0]
			print "数据库错误代码:",e.args[0],e.args[1]
			result = False
		return result


	def fetchOneRow(self):
		return self._cur.fetchone()

	def fetchAllRow(self):
		return self._cur.fetchall()
	
	def getRowCount(self):
		return self._cur.rowcount

	def commit(self):
		self._conn.commit()

	def rollback(self):
		self._conn.rollback()

	def __del__(self):
		try:
			self._cur.close()
			self._conn.close()
		except Exception, e:
			raise e
	def close(self):
		self.__del__()



def main():
	pass
if __name__ == '__main__':
	main()