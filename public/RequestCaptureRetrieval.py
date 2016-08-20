#coding=utf-8
'''
 与另一个REST API接口的封装功能相同，该接口弃用。
'''
import os
import struct
import sys
import uuid

from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
from gen_py.match import frs_match
from gen_py.match import ttypes
import Config
import DataBase
import DMExceptions
from Base import ThriftAPIBase

class RequestCaptureRetrieval(ThriftAPIBase):
	'''
				功能：抓拍库检索接口 thrift接口;该接口有相应的REST API，相应的文件是SearchGrabPic.py，该封装弃用。测试脚本不调用该接口。
				输入：     ip:连接的比对服务IP
				port：连接的比对服务port
				pic:图片所在路径
				c_id:通道id  列表
				time:开始结束的时间段 列表
				score：阈值
				pic_num：结果返回个数
				输出：GrabPicSearchReturn(success_flag=1, info=[SearchGrabPicInfo()])
				success_flag=1 检索成功
				success_flag=0 检索失败，图片无人脸等
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

	def request_grabpic_search(self,pic=None,c_id=None,time=None,score=None,pic_num=None, **kwargs):
		if 'c_name' in kwargs and type(kwargs['c_name'] == list) and c_id == None:
			c_id = []
			db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			for name in kwargs['c_name']:
				require_sql = "select c_id from frs_channel where  c_name='"+name+"'"
				result  = db.fetch_all(require_sql)
				if len(result) == 0:
					print("no video name!")
				else:
					c_id.append(result[0][0])
			db.close()
		if pic == None:
			try:
				PicSearchInGrab = ttypes.PicSearchInGrab(uuid=str(uuid.uuid1()),pic=pic,c_id=c_id,time=time,score=score,pic_num=pic_num)
				#print(PicSearchInGrab)
				result = self.client.request_grabpic_search(PicSearchInGrab)
			except struct.error as ex:
				raise DMExceptions.DataInvalidException('data invalid')
			return result
		else:
			pic = os.path.abspath('..\\picture')+'\\'+pic
		if not os.path.exists(pic):
			return  (pic +' is invalid')
		if os.path.isfile(pic):
			#if os.path.splitext(pic)[1] in ['.jpg','.png','.bmp']:
			f1 = open(pic,'rb')
			pic = f1.read()
			f1.close()
			try:
				PicSearchInGrab = ttypes.PicSearchInGrab(uuid=str(uuid.uuid1()),pic=pic,c_id=c_id,time=time,score=score,pic_num=pic_num)
				#print(PicSearchInGrab)
				result = self.client.request_grabpic_search(PicSearchInGrab)
				return result
			except struct.error as ex:
				raise DMExceptions.DataInvalidException('data invalid')
			'''
				if result.success_flag==0:
					print('picture has no face')
				elif result.success_flag==1 and len(result.info) ==0:
					print('picture has no result')
				else:
					print('picture success')
				'''
				#GrabPicSearchReturn(info=[], success_flag=0) no find face
				#GrabPicSearchReturn(info=[], success_flag=1) no result
				#GrabPicSearchReturn(info=[SearchGrabPicInfo(time=b'', c_id=2, score=0.5396379828453064, grab_id=1845),SearchGrabPicInfo(time=b'', c_id=2, score=0.509118914604187, grab_id=427)], success_flag=1) result

	def close(self):
		'''
		功能：关闭thrift连接
		输入：无
		输出：无
		'''
		ThriftAPIBase.close(self)

if __name__ == '__main__':
	test = RequestCaptureRetrieval()
	test.connect()
	#有效的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    GrabPicSearchReturn(success_flag=1, info=[SearchGrabPicInfo]
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#无效的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    GrabPicSearchReturn(info=[], success_flag=1)
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25555], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#数字的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    提示错误
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=25, time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#字符串的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    提示错误
	#r = test.request_grabpic_search(pic='50008.jpg', c_id='[25]', time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#超过i32的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    提示错误
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25,12,50,5111111111], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#不传c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    提示错误  fail
	#r = test.request_grabpic_search(pic='50008.jpg', time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#有效的c_id、无人脸图片、有效的时间段、有效的分数段、有效的返回个数    GrabPicSearchReturn(success_flag=0, info=[SearchGrabPicInfo]
	#r = test.request_grabpic_search(pic='lia.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#有效的c_id、多人脸图片、有效的时间段、有效的分数段、有效的返回个数    GrabPicSearchReturn(success_flag=1, info=[SearchGrabPicInfo]
	#r = test.request_grabpic_search(pic='much-720p.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#有效的c_id、非图片、有效的时间段、有效的分数段、有效的返回个数    GrabPicSearchReturn(info=[], success_flag=0)
	#r = test.request_grabpic_search(pic='1.txt', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#有效的c_id、不传图片、有效的时间段、有效的分数段、有效的返回个数    GrabPicSearchReturn(info=[], success_flag=0)
	#r = test.request_grabpic_search(c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=12)
	#有效的c_id、有人脸图片、有效的时间段、无效的分数段、有效的返回个数    GrabPicSearchReturn(info=[], success_flag=1)
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=-0.2, pic_num=12)
	#有效的c_id、有人脸图片、有效的时间段、字符串的分数段、有效的返回个数    提示错误
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score='-0.2', pic_num=12)
	#有效的c_id、有人脸图片、有效的时间段、列表的分数段、有效的返回个数    提示错误
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=[0.2,1], pic_num=12)
	#有效的c_id、有人脸图片、有效的时间段、不传分数段、有效的返回个数   GrabPicSearchReturn(success_flag=1, info=[SearchGrabPicInfo]
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'], pic_num=12)
	#有效的c_id、有人脸图片、无效的时间段、有效的分数段、有效的返回个数    GrabPicSearchReturn(success_flag=1, info=[])
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-1-17 11:48:01'],score=0, pic_num=12)
	#有效的c_id、有人脸图片、字符串的时间段、有效的分数段、有效的返回个数    GrabPicSearchReturn(success_flag=1, info=[])
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time='2015-08-04 11:48:01',score=0, pic_num=12)
	#有效的c_id、有人脸图片、不传时间段、有效的分数段、有效的返回个数     fail
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25],score=0, pic_num=12)
	#有效的c_id、有人脸图片、有效的时间段、有效的分数段、有效的返回个数    GrabPicSearchReturn(success_flag=1, info=[SearchGrabPicInfo]
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num=1)
	#有效的c_id、有人脸图片、有效的时间段、有效的分数段、无效的返回个数  提示错误
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0, pic_num='1')
	#有效的c_id、有人脸图片、有效的时间段、有效的分数段、列表返回个数  GrabPicSearchReturn(success_flag=0, info=[])
	r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0,pic_num=[1])
	#有效的c_id、有人脸图片、有效的时间段、有效的分数段、不传返回个数  GrabPicSearchReturn(success_flag=0, info=[])
	#r = test.request_grabpic_search(pic='50008.jpg', c_id=[25], time=['2015-08-04 11:48:01','2015-12-17 11:48:01'],score=0)
	test.close()
	print(r)
