#coding=utf-8
import os
import uuid
from gen_py.match import frs_match
from gen_py.match import ttypes
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol
import DataBase
import Config
import LogConfig
import DMExceptions
from Base import ThriftAPIBase

class RequestVideoDetect(ThriftAPIBase):
	'''
	对thrift接口request_video_detect(1:ClientInMsgVideoDetect req1)进行封装，该接口的作用是
	检测人脸，并将检测到人脸与在库人脸比对，相当于管理端实时人脸监控
   属性：match_thrift_ip:比对端thrift的IP
		match_thrift_port:比对端thrift的PORT
		tranport:thritf模块中网络读写抽象
		protocol:thrift模块中数据格式抽象
		client:thrift客户端
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

	def grab_and_match(self, pic_name, max_face_num=0, msgtype=0, **kwargs):
		'''
		功能：发送图片给比对服务，比对服务抓取人脸信息，且将抓取的人脸信息进行比对
		输入：msgtype:预留值，默认为0
		pic_name:需要比对的图片名称
		max_face_num:图片上抓取的最大人脸数---目前这个参数在该接口下没什么作用，先前版本使用这个参数；后面的版本在REST API中设置比对抓拍的最大人脸数
		kwargs:可选参数输入，facedb_name:比对使用的人脸库名称，列表格式，facedb_id:比对使用的人脸库的ID，列表格式；名称和ID只能使用一种
						channel_name:使用的通道名称，channel_id:使用的通道ID；名称和ID只能使用一种
		输出：整型，0表示比对接收图片成功，其他表示失败。
		'''
		#获取通道ID
		if 'channel_id' in kwargs:
			channel_id = kwargs['channel_id']
		#根据通道名称获取对应的通道号
		elif 'channel_name' in kwargs:
			db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			require_sql = "select c_id from frs_channel where c_name='"+kwargs['channel_name']+"'"
			result  = db.fetch_all(require_sql)
			if len(result) == 0:
				print("no device name!")
				db.close()
				return
			else:
				channel_id = result[0][0]
			db.close()
		#生成uuid
		cur_uuid = str(uuid.uuid1())
		#获取人脸库ID
		facedb_id = []
		if 'facedb_id' in kwargs:
		#根据人脸名称获取对应的人脸库ID
			facedb_id = kwargs['facedb_id']
		elif 'facedb_name' in kwargs:
			db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			for name in kwargs['facedb_name']:
				req_sql = "select fd_id from frs_facedb where fd_name='"+name+"'"
				#print(req_sql)
				result = db.fetch_all(req_sql)
				if len(result) == 0:
					print("no facedb name!")
					continue
				else:
					facedb_id.append(result[0][0])
			db.close()
		#获取图片
		pic_file_path = os.path.split(os.path.realpath(__file__))[0]+('\\..\\picture')+'\\'+pic_name
		#print(pic_file_path)
		try:
			pic = open(pic_file_path,'rb')
			picture = pic.read()
		except Exception as ex:
			raise DMExceptions.ReadPicException(str(ex))
		finally:
			pic.close()
		#构造thrift用参数
		send_in = ttypes.ClientInMsgVideoDetect(msg_type=msgtype, c_id=channel_id, uuid=cur_uuid, pic=picture, \
												pic_size=len(picture), max_face=max_face_num, face_db_list=facedb_id)
		try:
			result = self.client.request_video_detect(send_in)
			self.log.logger.info("发送图片给比对，图片名称为"+pic_name)
		except Exception as ex:
			self.log.logger.error("发送图片给比对时出现异常！")
			raise DMExceptions.SendException(str(ex))
		return result

	def close(self):
		'''
		功能：关闭thrift连接
		输入：无
		输出：无
		'''
		ThriftAPIBase.close(self)



if __name__ == "__main__":
	test = RequestVideoDetect()
	test.connect()
	result = test.grab_and_match(channel_name="channel_test", pic_name="范冰冰.jpg", max_face_num=5, facedb_name=["facedb_test"])
	print(result)
	test.close()
