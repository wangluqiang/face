#coding=utf-8

from _datetime import date
import base64
import datetime
import json 
import os

import requests
import sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
import Config
import DataBase
import LogConfig
import DMExceptions
from Base import RESTAPIBase

class SearchGrabPic(RESTAPIBase):
	'''
	 抓拍库检索，restful接口
	'''


	def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
		if path == None:
			cfg = Config.Config()
			s_path = cfg.url_path_info()["facepic"]
		else:
			s_path = path
		RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)

	#读取照片
	def pic_read(self,filename):
		pic_file_path = os.path.abspath(cur_path+'\\..\\picture')+'\\'+filename
		try:
			file_obj = open(pic_file_path, 'rb')
			pic_buffer = file_obj.read()
		except Exception as ex:
			raise DMExceptions.ReadPicException(str(ex))
		finally:
			file_obj.close()
		return pic_buffer

	def facepic_grab_search(self,pic_name=None,return_num=None,**kwargs):
		'''
			功能：抓拍库检索
			输入：
			pic_name：照片名称
			return_num：返回的个数
				**kwargs包含参数：
				c_id：通道id,列表格式如：[1,2,3]
				c_name:通道名称,列表格式如：['1','2']
				time：时间范围，列表格式如：['2015-07-01 12:00:00','2015-09-02 12:00:00']
				threshold：相似度

			输出：字典格式：
			检索详细信息
		'''

		condition={}
		if return_num==None:
			pass
		else:
			condition['return_num'] = return_num
		if 'c_id' in kwargs:
			condition['c_id']=kwargs['c_id']
		if 'c_name' in kwargs and type(kwargs['c_name']) == list and len(kwargs['c_name'])>0 and 'c_id' not in kwargs:
			c_id = []
			db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			for name in kwargs['c_name']:
				require_sql = "select c_id from frs_channel where  c_name='"+name+"'"
				result  = db.fetch_all(require_sql)
				if len(result) == 0:
					print("no video name!")
				else:
					for each in result:
						c_id.append(each[0])
			db.close()
			if len(c_id)>0:
				condition['c_id'] = c_id
		if 'threshold' in kwargs:
			condition['threshold']=kwargs['threshold']
		'''
		else:
			condition['threshold']=0.8
		'''
		if 'time' in kwargs:
			condition['time']=kwargs['time']
		'''
		else:
			oneday = datetime.timedelta(days=5)
			s_time=datetime.datetime.now()+oneday
			end_time='%s-%s-%s %s:%s:%s'%(s_time.year,s_time.month,s_time.day,s_time.hour,s_time.minute,s_time.second)
			s_time = datetime.datetime.now()-datetime.timedelta(days=25)
			start_time='%s-%s-%s %s:%s:%s'%(s_time.year,s_time.month,s_time.day,s_time.hour,s_time.minute,s_time.second)
			condition['time']=[start_time,end_time]
		'''
		facepic_search_data={}
		facepic_search_data['type'] = 1
		if pic_name == None:
			pass
		else:
			pic = self.pic_read(pic_name)
			facepic_search_data['content'] = base64.b64encode(pic).decode()
		facepic_search_data['condition'] = condition
		try:
			search_result = requests.post(self.url,data=json.dumps(facepic_search_data),headers=self.headers)
			search_result.raise_for_status()
			self.log.logger.info("抓拍库检索图片名称：" + str(pic_name)+" ，返回个数： " +str(return_num)+" ,条件："+str(kwargs))
		except Exception as ex:
			self.log.logger.warning("抓拍库检索出现异常，从server接收响应失败！图片名称：" + str(pic_name)+"  ，返回个数： " +str(return_num)+" ,条件："+str(kwargs))
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			search_result.json()
		except Exception as ex:
			self.log.logger.warning("抓拍库检索出现异常，响应消息转换为json格式错误！图片名称：" + str(pic_name)+"  ，返回个数： " +str(return_num)+" ,条件："+str(kwargs))
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(search_result.json())


if __name__ == "__main__":
	SearchPic_test = SearchGrabPic()

#有效的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    {'return_data': [{'score': 0.4981934428215027, 'grab_pic': '/9j/4AA', 'grab_id': 9720, 'time': '2015-08-27 14:02:23'}]}
	result=SearchPic_test.facepic_grab_search(pic_name='50010.jpg',c_name =['0'],time=['2015-11-11 16:04:01','2015-11-11 16:06:01'],threshold=0,return_num=12)
#无效的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[255],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#数字的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数     {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =25,pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#字符串的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id ='q25',pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#超过i32的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数   {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[111111111111111],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#不传c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    fail
	#result=SearchPic_test.facepic_grab_search(pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#有效的c_id、无人脸图片、有效的时间段、有效的分数段、有效的返回个数    {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='car.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#有效的c_id、多人脸图片、有效的时间段、有效的分数段、有效的返回个数    {'return_data': [{'score': 0.4981934428215027, 'grab_pic': '/9j/4AA', 'grab_id': 9720, 'time': '2015-08-27 14:02:23'}]}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='much-720p.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#有效的c_id、非图片、有效的时间段、有效的分数段、有效的返回个数    {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='1.txt',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#有效的c_id、不传图片、有效的时间段、有效的分数段、有效的返回个数    {'errorinfo': -650}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#有效的c_id、有人脸图片、有效的时间段、无效的分数段、有效的返回个数  {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=-0.2,return_num=1)
#有效的c_id、有人脸图片、有效的时间段、字符串的分数段、有效的返回个数   {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold='q-0.2',return_num=1)
#有效的c_id、有人脸图片、有效的时间段、列表的分数段、有效的返回个数   {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=[0.2],return_num=1)
#有效的c_id、有人脸图片、有效的时间段、不传分数段、有效的返回个数       {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],return_num=1)
#有效的c_id、有人脸图片、无效的时间段、有效的分数段、有效的返回个数   {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time=['2015-12-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=1)
#有效的c_id、有人脸图片、字符串的时间段、有效的分数段、有效的返回个数   {'return_data': []} 
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time='2015-12-04 11:48:01 11:48:01',threshold=0,return_num=1)
#有效的c_id、有人脸图片、不传时间段、有效的分数段、有效的返回个数     崩溃
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',threshold=0,return_num=1)
#有效的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数  {'return_data': [{'score': 0.4981934428215027, 'grab_pic': '/9j/4AA', 'grab_id': 9720, 'time': '2015-08-27 14:02:23'}]}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=12)
#有效的c_id、有人脸图片、有效的时间段、有效的分数段、无效的返回个数     error   全部
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=-12)
#有效的c_id、有人脸图片、有效的时间段、有效的分数段、列表返回个数  {'return_data': []}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0,return_num=[12])
#有效的c_id、有人脸图片、有效的时间段、有效的分数段、不传返回个数   {'errorinfo': -250}
	#result=SearchPic_test.facepic_grab_search(c_id =[25],pic_name='50010.jpg',time=['2015-08-04 11:48:01','2015-09-17 11:48:01'],threshold=0)
	print(result)
	#print(len(result.get('return_data')))

#     for each in result['return_data']:
#         print(each['grab_id'],each['score'],each['time'])
#     print(result)