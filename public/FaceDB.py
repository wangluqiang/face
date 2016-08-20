#coding=utf-8
import requests
import json 
import DataBase
import Config
import LogConfig
import DMExceptions
from Base import RESTAPIBase

class FaceDB(RESTAPIBase):
	'''
	 封装的人脸库类，该类主要用于人脸库的增、删、改、查
	'''

	def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
		if path == None:
			cfg = Config.Config()
			s_path = cfg.url_path_info()["facedb"]
		else:
			s_path = path
		RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)

	def facedb_add(self, **kwargs):
		'''
			功能：添加人脸库
			输入：fd_name:添加人脸库的名称
			fd_threshold：添加人脸库的阈值
			remark：添加人脸库的备注，默认为空
			输出：字典格式：
			{"errorinfo": 1}，返回数字为人脸库的fd_id

		'''
		facedb_add_data = {}
		facedb_add_data.update(kwargs)
		#失败请求(非200响应)抛出异常
		try:
			add_result = requests.post(self.url,data=json.dumps(facedb_add_data),headers=self.headers)
			add_result.raise_for_status()
			if 'fd_name' in facedb_add_data and 'fd_threshold' in facedb_add_data and "remark" in facedb_add_data:
				self.log.logger.info("添加人脸库名称为："+facedb_add_data["fd_name"]+",阈值为："\
									 +str(facedb_add_data["fd_threshold"])+",备注为："+str(facedb_add_data["remark"]))
		except Exception as ex:
			self.log.logger.error("添加人脸库出现异常，从server接收响应失败！")
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			add_result.json()
		except Exception as ex:
			self.log.logger.error("添加人脸库出现异常，响应消息转换为json格式错误！")
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(add_result.json())

	def facedb_delete(self, name=None, face_id=None):
		'''
		功能：删除人脸库，参数有face_id情况下，根据face_id删除人脸库，参数有name情况下，根据name删除人脸库。id和name只能传一个参数。
		输入：name：删除人脸库的名称
		face_id:删除人脸库的ID
		输出：字典格式:{"errorinfo": 0}表示删除成功
		'''
		if face_id != None:
			facedb_id = face_id
			facedb_delete_data = {"fd_id":facedb_id}
		#根据人脸库名称查询其ID
		elif name != None:
			facedb = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			sql_query = "select fd_id from frs_facedb where fd_name='"+name+"'"
			query_result = facedb.fetch_all(sql_query)
			facedb.close()
			facedb_id = query_result[0][0]
			facedb_delete_data = {"fd_id":facedb_id}
		else:
			facedb_delete_data = {}
		try:
			delete_result = requests.delete(self.url, data=json.dumps(facedb_delete_data), headers=self.headers)
			delete_result.raise_for_status()
			if "facedb_id" in locals().keys():
				self.log.logger.info("删除人脸库，人脸库id为："+str(facedb_id))
		except Exception as ex:
			self.log.logger.error("添加人脸库出现异常，从server接收响应失败！")
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			delete_result.json()
		except Exception as ex:
			self.log.logger.error("添加人脸库出现异常，响应消息转换为json格式错误！")
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(delete_result.json())

	def facedb_modify(self, fd_id=None, name=None, **kwargs):
		'''
		功能：修改人脸库
		输入：fd_id:需要修改的人脸库的id
		name:需要修改的人脸库的名称
			需要修改的内容:  fd_threshold:修改后人脸库阈值
				  fd_name:修改后人脸库名称
				  remark：修改后人脸库备注
				  若需正确修改，则需修改人脸库的相应部分必须填写，包括未修改部分
		输出：字典格式：{"errorinfo": 0} 表示修改成功
		'''
		if fd_id != None:
			facedb_modify_data = {"fd_id":fd_id}
			facedb_id = fd_id
		elif name != None:
			#根据人脸库名称查询其ID
			facedb = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			#查询数据库，返回数据依次是fd_id, fd_name, fd_threshold, remark
			sql_query = "select * from frs_facedb where fd_name='"+name+"'"
			query_result = facedb.fetch_all(sql_query)
			facedb.close()
			facedb_id = query_result[0][0]
			facedb_modify_data = {"fd_id":facedb_id}
		else:
			facedb_modify_data = {}
		facedb_modify_data.update(kwargs)
		try:
			modify_result = requests.put(self.url, data=json.dumps(facedb_modify_data), headers=self.headers)
			modify_result.raise_for_status()
			if "fd_id" in modify_result:
				self.log.logger.info("修改人脸库，人脸库ID为："+str(facedb_id))
		except Exception as ex:
			self.log.logger.error("添加人脸库出现异常，从server接收响应失败！")
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			modify_result.json()
		except Exception as ex:
			self.log.logger.error("添加人脸库出现异常，响应消息转换为json格式错误！")
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(modify_result.json())

	def facedb_query(self):
		'''
		功能：查询全部人脸库
		输入：空
		输出：列表格式，人脸库详细信息
		'''
		try:
			query_result =requests.get(self.url)
			query_result.raise_for_status()
			self.log.logger.info("查询全部人脸库")
		except Exception as ex:
			self.log.logger.error("添加人脸库出现异常，从server接收响应失败！")
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			query_result.json()
		except Exception as ex:
			self.log.logger.error("添加人脸库出现异常，响应消息转换为json格式错误！")
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(query_result.json())

 
if __name__ == "__main__":
	facedb_test = FaceDB()
	print(facedb_test.facedb_add("wujingjing", 0.8))
	#q = facedb_test.facedb_modify("wujingjing", threshold=1, remark='modify facedb testjfladsjsalk!')
	#print(facedb_test.facedb_query())
	print(facedb_test.facedb_modify(fd_name="wujingjing", modify_remark="更改人脸库"))
	print(facedb_test.facedb_delete(name="wujingjing"))