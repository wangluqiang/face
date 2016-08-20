#coding=utf-8
import os
import uuid
import LogConfig
import DMExceptions
import DataBase
import Config
from gen_py.match import frs_match
from gen_py.match import ttypes
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol
from Base import ThriftAPIBase
import DMExceptions

class FacePicRetrieval(ThriftAPIBase):
	'''
	对thrift接口PicSerchReturn request_pic_search(1:ClientInMsgPicSearch req1)的封装，该接口的功能是：
	server发给比对服务一张图片，比对服务返回比对结果给server，相当于管理端界面的人脸图像检索功能,不写入数据库，只有图片展示。
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

	def match(self, pic_name, threshold, pic_num, facedb_name=None):
		'''
		功能：发送图片和其他参数给比对服务，比对服务返回结果
		输入：pic_name:需要检索的图片名称
		facedb_name:检索使用的人脸库，默认为None，表示在全部人脸库检索
		threshold：检索比对值
		pic_num:检索返回图片数量的最大值
		以上几个参数，与管理端界面的人脸图像检索对应
		输出：PicSerchReturn类，该类的属性有：success_flag:为0表示图片处理或提取特征失败，为1表示图片处理且提取特征成功
								info：列表格式，为空表示无匹配的在库人员，不为空则包含匹配成功的人员信息，人员信息格式为类SearchPicInfo，
																									该类的属性有p_id：匹配到在库人员的ID； face_db匹配人员所在的人脸库ID；score：相似度
		'''
		#读取图片
		pic_file_path = os.path.split(os.path.realpath(__file__))[0]+('\\..\\picture\\')+pic_name
		#print(pic_file_path)
		try:
			pic = open(pic_file_path,'rb')
			picture = pic.read()
			pic.close()
		except Exception as ex:
			#print(ex)
			raise DMExceptions.ReadPicException(str(ex))
		#生成uuid
		cur_uuid = str(uuid.uuid1())
		#根据人脸库名称查找人脸库
		if facedb_name == None:
			face_id = 0
		else:
			facedb = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			sql_query = "select fd_id from frs_facedb where fd_name='"+facedb_name+"'"
			query_result = facedb.fetch_all(sql_query)
			facedb.close()
			face_id = query_result[0][0]
		#生成thrift参数
		retrieval_in = ttypes.ClientInMsgPicSearch(uuid=cur_uuid, pic=picture, face_no=face_id, threshold=threshold, pic_num=pic_num)
		#print(retrieval_in)
		self.log.logger.info("向服务器发送的参数生成成功！")
		result = self.client.request_pic_search(retrieval_in)
		self.log.logger.info("向比对服务发送图片，图片名称为："+pic_name)
		return result

	def close(self):
		'''
		功能：关闭thrift连接
		输入：无
		输出：无
		'''
		ThriftAPIBase.close(self)



if __name__ == "__main__":
	retrieval_1 = FacePicRetrieval()
	retrieval_1.connect()
	#try:
	r = retrieval_1.match(pic_name="50012.jpg",  threshold=0.8, pic_num=12, facedb_name="facedb_test")
	#except Exception as ex:
		#print(str(ex))
	print(r)

