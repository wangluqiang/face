#coding=utf8
import os
import struct

import uuid

from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport

import Config
import DataBase
import FaceMatch
from gen_py.match import frs_match, ttypes
import DMExceptions
from Base import ThriftAPIBase
cur_path = os.path.split(os.path.realpath(__file__))[0]



class RequestVideoDetect(ThriftAPIBase):
	'''
	功能：视频文件检索接口

	'''
	def __init__(self, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):

		ThriftAPIBase.__init__(self, ip, port, db_ip, db_port, db_name, db_user, db_passwd)

	def connect(self):
		'''
		功能：与比对端的thrift server建立连接
		输入：无
		输出：无
		'''
		ThriftAPIBase.connect(self)

	def request_video_detect(self,pic=None,max_face=None,for_num=None,c_id=None,face_db_list=None,**kwargs):
		'''
		功能：发送图片给比对服务，比对服务抓取人脸信息，且将抓取的人脸信息进行比对后返回结果
		输入：
		pic:需要比对的图片名称,等于all时传入所有图片
		max_face_num:图片上抓取的最大人脸数
		for_num：循环次数
		c_id:视频id
		face_db_list:人脸库id列表
		kwargs:可选参数输入，face_name_list:比对使用的人脸库名称，列表格式,名称和ID只能使用一种
						c_name:使用的视频名称，列表格式，名称和ID只能使用一种
		输出：整型，0表示抓取人脸成功，其他表示抓取人脸失败。
		'''
		if 'c_name' in kwargs and c_id == None:
			db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			require_sql = "select c_id from frs_channel where  c_name='"+kwargs['c_name']+"'"
			result  = db.fetch_all(require_sql)
			if len(result) == 0:
				print("no video name!")
			else:
				c_id = result[0][0]
			db.close()
		if 'face_name_list' in kwargs and face_db_list==None:
			face_db_list = []
			for name in kwargs['face_name_list']:
				#print (name)
				db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
				require_sql = "select fd_id from frs_facedb where fd_name='"+name+"'"
				result  = db.fetch_all(require_sql)
				if len(result) == 0:
					print("no facedb name!")
					continue
				else:
					face_db_list.append(result[0][0])
				db.close()
		#print(c_id)
		#print(face_db_list)
		result = []
		if pic == 'all':
			pic = cur_path+'\\..\\picture'
		elif pic == None:
			pic = None
			for i in range(for_num):
				try:
					ClientInMsgVideoDetect = ttypes.ClientInMsgVideoDetect(msg_type=0,c_id=c_id,uuid=str(uuid.uuid1()),pic=pic,pic_size=14000,max_face=max_face,face_db_list=face_db_list)
					#print(ClientInMsgVideoDetect)
					r = self.client.request_video_detect(ClientInMsgVideoDetect)
				except struct.error as ex:
					raise DMExceptions.DataInvalidException('data invalid')
			result.append(r)
			return result
		else:
			pic = os.path.abspath(cur_path+'\\..\\picture')+'\\'+str(pic)
		if os.path.isfile(pic):
			f1 = open(pic,'rb')
			pic = f1.read()
			f1.close()
			for i in range(for_num):
				try:
					ClientInMsgVideoDetect = ttypes.ClientInMsgVideoDetect(msg_type=0,c_id=c_id,uuid=str(uuid.uuid1()),pic=pic,pic_size=14000,max_face=max_face,face_db_list=face_db_list)
					r = self.client.request_video_detect(ClientInMsgVideoDetect)
				except struct.error as ex:
					raise DMExceptions.DataInvalidException('data invalid')
			result.append(r)
			return result
		if os.path.isdir(pic):
			list = os.listdir(pic)
			result = []
			names = []
			for l in list:
				name = os.path.join(pic,l)
				names.append(name)
			for i in range(for_num):
				for name in names:
					f1 = open(name,'rb')
					pic = f1.read()
					f1.close()
					try:
						ClientInMsgVideoDetect = ttypes.ClientInMsgVideoDetect(msg_type=0,c_id=c_id,uuid=str(uuid.uuid1()),pic=pic,pic_size=14000,max_face=max_face,face_db_list=face_db_list)
						#print(ClientInMsgVideoDetect)
						r = self.client.request_video_detect(ClientInMsgVideoDetect)
					except struct.error as ex:
						raise DMExceptions.DataInvalidException('data invalid')
					result.append(r)
			return result

	def close(self):
		'''
		功能：关闭thrift连接
		输入：无
		输出：无
		'''
		ThriftAPIBase.close(self)


if __name__ == '__main__':

	#有效的c_id、有人脸图片、有效的人脸数、有效的人脸库  抓拍结果都有
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='50008.jpg', max_face=10, for_num=1,c_id=5,face_db_list=[1])
	# 无效的c_id、有人脸图片、有效的人脸数、有效的人脸库 抓拍结果都有
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='50010.jpg', max_face=10, for_num=1,c_id=55555,face_db_list=[1])
	#不合理的c_id、有人脸图片、有效的人脸数、有效的人脸库    抓拍结果都没有，提示错误
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='50010.jpg', max_face=10, for_num=1,c_id='55125',face_db_list=[1])
	#列表的c_id、有人脸图片、有效的人脸数、有效的人脸库    抓拍结果都没有，提示错误
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='50010.jpg', max_face=10, for_num=1,c_id=[55125],face_db_list=[1])
	#不传c_id、有人脸图片、有效的人脸数、有效的人脸库    抓拍结果都有，但c_id=0
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='50010.jpg', max_face=10, for_num=1,face_db_list=[1])
	#有效的c_id、无人脸图片、有效的人脸数、有效的人脸库  抓拍结果无
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='lia.jpg', max_face=10, for_num=1,c_id=5,face_db_list=[1])
	#有效的c_id、多人脸图片、10人脸数、有效的人脸库  抓拍结果多条结果
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='much-720p.jpg', max_face=10, for_num=1,c_id=15,face_db_list=[1])
	#有效的c_id、不传图片、有效的人脸数、有效的人脸库  抓拍结果无
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(max_face=10, for_num=1,c_id=15,face_db_list=[1])
	#有效的c_id、不存在图片、有效的人脸数、有效的人脸库  抓拍结果无  结果=None
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='1.jpg',max_face=10, for_num=1,c_id=15,face_db_list=[1])
	#有效的c_id、有人脸图片、有效的人脸数、无效的人脸库  抓拍有 结果无
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='50008.jpg', max_face=10, for_num=1,c_id=5,face_db_list=[111])
	#有效的c_id、有人脸图片、有效的人脸数、不合理的人脸库  抓拍结果无 ，提示错误
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='50008.jpg', max_face=10, for_num=1,c_id=5,face_db_list=1)
	#有效的c_id、有人脸图片、有效的人脸数、不传人脸库  抓拍有 结果无
	match_client = RequestVideoDetect()
	match_client.connect()
	r = match_client.request_video_detect(pic='50008.jpg', max_face=10, for_num=1,c_id=55)
	match_client.close()
	#有效的c_id、多人脸图片、1人脸数、有效的人脸库  抓拍结果一条结果
	#facematch_test = FaceMatch.FaceMatch()
	#facematch_test.facematch_modify('test911',m_ip='172.16.200.210',m_port=9999,face_max=1)
	#match_client = RequestVideoDetect()
	#r = match_client.request_video_detect(pic='much-720p.jpg', max_face=1, for_num=1,c_id=1511,face_db_list=[1])
	print(r)
