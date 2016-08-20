#coding=utf-8
import requests
import json 
from DataBase import DataBase
import Config
import DMExceptions
from Base import RESTAPIBase

class FacePre(RESTAPIBase):
	'''
	 封装的预处理配置类，该类主要用于预处理的增、删、改、查
	 属性：
	 fpre_path:URL路径
	 url:http的完整路径
	'''


	def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
		if path == None:
			cfg = Config.Config()
			s_path = cfg.url_path_info()["preprocess"]
		else:
			s_path = path
		RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)

	def facepre_add(self,**kwargs):    #p_name,p_ip,p_port,m_id,frame_interval,remark=''
		'''
			功能：添加预处理
			输入：
			p_name:添加预处理的名称
			p_ip：预处理IP
			p_port：预处理端口
			m_id:比对服务ID
			m_name:比对服务名称;不选择比对服务，则传0
			frame_interval：帧频
			输出：字典格式：
			{"errorinfo": 1}，表示成功

		'''
		facepre_add_data = {}
		if "p_name" in kwargs:
			facepre_add_data['p_name'] = kwargs['p_name']
		if "p_ip" in kwargs:
			facepre_add_data['p_ip'] = kwargs['p_ip']
		if "p_port" in kwargs:
			facepre_add_data['p_port'] = kwargs['p_port']
		if "m_name" in kwargs:
			Predb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			sql_query_id = "select m_id from frs_match where m_name='"+kwargs['m_name']+"'"
			query_result_id = Predb.fetch_all(sql_query_id)
			Predb.close()
			m_id = query_result_id[0][0]
			facepre_add_data['m_id'] = m_id
		if "m_id" in kwargs:
			facepre_add_data['m_id'] = kwargs['m_id']
		if "m_name" not in kwargs and "m_id" not in kwargs:
			facepre_add_data['m_id'] = 0
		if "frame_interval" in kwargs:
			facepre_add_data['frame_interval'] = kwargs['frame_interval']
		if "remark" in kwargs:
			facepre_add_data['remark'] = kwargs['remark']
		try:
			add_result = requests.post(self.url,data=json.dumps(facepre_add_data),headers=self.headers)
			add_result.raise_for_status()
		except Exception as ex:
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			add_result.json()
		except Exception as ex:
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(add_result.json())

	def facepre_delete(self, p_name=None, p_id=None):
		'''
		功能：删除预处理
		输入：
		p_id：删除预处理的Id
		p_name:删除预处理的名称
		输出：字典格式:{"errorinfo": 0}表示删除成功
		'''
		if p_name is None and p_id is None:
			return
		if p_id==None:
			Predb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			sql_query_id = "select p_id from frs_collection where p_name='"+p_name+"'"
			query_result_id = Predb.fetch_all(sql_query_id)
			Predb.close()
			p_id = query_result_id[0][0]
			facepre_delete_data = {"p_id":p_id}
		else:
			facepre_delete_data={'p_id':p_id}

		#print(facepre_delete_data)
		try:
			delete_result = requests.delete(self.url, data=json.dumps(facepre_delete_data), headers=self.headers)
			delete_result.raise_for_status()
		except Exception as ex:
			raise DMExceptions.GetHttpResponseError(str(ex))

		try:
			delete_result.json()
		except Exception as ex:
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(delete_result.json())

	def facepre_modify(self,p_name=None,p_id=None,**kwargs):
		'''
		功能：修改预处理
		输入：
		p_name:预处理名称
		m_id：比对服务Id
		m_name:比对服务名称，如果不选择比对服务，则将m_id=0
		frame_interval：帧频
		p_ip/p_port:ip地址及接口
		输出：字典格式：{"errorinfo": 0} 表示修改成功
		'''

		if p_name != None:
			Predb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			sql_query_id = "select p_id from frs_collection where p_name='"+p_name+"'"
			query_result_id = Predb.fetch_all(sql_query_id)
			Predb.close()
			p_id = query_result_id[0][0]
			facepre_modify_data = {"p_id":p_id}
		else:
			facepre_modify_data={'p_id':p_id}

		if "p_name_x" in kwargs:
			facepre_modify_data["p_name"] = kwargs['p_name_x']
		if "m_name" in kwargs:
			Predb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			sql_query_id = "select m_id from frs_match where m_name='"+kwargs['m_name']+"'"
			query_result_id = Predb.fetch_all(sql_query_id)
			Predb.close()
			m_id = query_result_id[0][0]
			facepre_modify_data['m_id'] = m_id
		if "m_id" in kwargs:
			facepre_modify_data["m_id"] = kwargs['m_id']
		if "frame_interval" in kwargs:
			facepre_modify_data["frame_interval"] = kwargs['frame_interval']
		if "remark" in kwargs:
			facepre_modify_data["remark"] = kwargs['remark']
		if "p_port" in kwargs:
			facepre_modify_data["p_port"] = kwargs['p_port']
		if "p_ip" in kwargs:
			facepre_modify_data["p_ip"] = kwargs['p_ip']
		#print(facepre_modify_data)
		try:
			modify_result = requests.put(self.url, data=json.dumps(facepre_modify_data), headers=self.headers)
			modify_result.raise_for_status()
		except Exception as ex:
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			modify_result.json()
		except Exception as ex:
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(modify_result.json())


	def facepre_query(self):
		'''
		功能：查询全部预处理
		输入：空
		输出：列表格式，人脸库详细信息
		'''
		try:
			query_result =requests.get(self.url)
			query_result.raise_for_status()
		except Exception as ex:
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			query_result.json()
		except Exception as ex:
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(query_result.json())


if __name__ == "__main__":
	facepre_test = FacePre()

	print(facepre_test.facepre_add(p_name='test119', p_ip='192.168.29.148',p_port=1025,m_name='match_test',frame_interval=124))
	print(facepre_test.facepre_query())
	print(facepre_test.facepre_modify(p_name='test119',p_name_x='test911',p_ip='192.168.29.148',p_port=1025,frame_interval=125))
	print(facepre_test.facepre_delete('test911'))
	print(facepre_test.facepre_query())