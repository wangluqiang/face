#coding=utf-8
import unittest
import os,time
import sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import FaceDB
import DataBase
import FacePerson
import RequestVideoDetect
import LogConfig
import DMExceptions
from handle_exception import handle_exception

class FaceDBTestCase(unittest.TestCase):
	'''
	功能： 人脸库相关功能测试脚本
	'''
	def setUp(self):
		'''
		功能：脚本运行前配置环境
		'''
		self.facedb = FaceDB.FaceDB()
		self.log = LogConfig.Logger()
		self.items = {}

	def tearDown(self):
		'''
		功能：脚本运行后清理环境
		'''
		self.items = {}

	@handle_exception
	def test_facedb_add_name_wujingjing_threshold_08(self):
		'''
		用例：添加人脸库，名称为某个英文字符串，阈值为0.8
		'''
		self.log.logger.info("")
		#添加人脸库
		result = self.facedb.facedb_add(fd_name="wujingjing_test", fd_threshold=0.8)
		self.items['facedb'] = result
		#通过http reponse信息验证是否添加成功
		self.assertGreaterEqual(result["errorinfo"], 0,'add facedb fail')
		db = DataBase.DataBase()
		require_sql = "select * from frs_facedb where fd_id="+str(result['errorinfo'])
		require_result = db.fetch_all(require_sql)
		if len(require_result) < 1:
			self.fail("add facedb to frs_facedb error!")
		else:
				#通过表frs_facedb验证是否添加成功
			self.assertEqual(require_result[0][1], "wujingjing_test", "add facedb name error!")
			self.assertEqual(require_result[0][2], 0.8, "add facedb threshold error!")
			self.assertEqual(require_result[0][3],None,"add facedb remark error!")
			#通过上传图片验证该人脸库是否添加成功
		face_person = FacePerson.FacePerson()

			#print(pic_file_path)
		person_result = face_person.faceperson_add(p_name="facedb_add_person_test", reg_type=1, grab_id=0, \
								   sex=1, cardId='12345678', pic_name='50008.jpg', fd_id=result["errorinfo"])
		self.assertGreaterEqual(person_result['errorinfo'], 0)
		self.items['person'] = person_result
			#给比对发送该图片，比对成功，验证人脸库可用
		compare = RequestVideoDetect.RequestVideoDetect()
		self.items['compare'] = compare
		compare.connect()
			#print([result['errorinfo']])
		compare_r = compare.grab_and_match(pic_name='50008.jpg', max_face_num=5,\
										   facedb_id=[result["errorinfo"]], channel_name='channel_test')
		self.assertEqual(compare_r, 0, "未抓取到人脸")
		time.sleep(5)
		db = DataBase.DataBase()
		self.items['db'] = db
		grab_sql = "select * from frs_grab order by grab_id desc limit 1"
		result_sql = "SELECT * from frs_result where pid1="+str(person_result['errorinfo'])

		result_r = db.fetch_all(result_sql)
			#print(grab_r)
			#db.close()
			#print(result_r)
		self.assertNotEqual(result_r[0][0], 0, "上传在库人员相同照片时比对失败")

	@handle_exception
	def test_facedb_add_name_used(self):
		'''
		用例：添加人脸库名字与已有人脸库名字重复
		'''
		self.log.logger.info("")
		#首先添加一个人脸库
		r = self.facedb.facedb_add(fd_name="name_used_test", fd_threshold=0.8)
		self.items['facedb'] = r
		#再添加同名的人脸库
		result = self.facedb.facedb_add(fd_name="name_used_test", fd_threshold=0.8)
		self.assertEqual(result["errorinfo"], -7)

	@handle_exception
	def test_facedb_add_json_format_error(self):
		'''
		用例：restful串格式有误，添加人脸库，不输入必填项名称或者阈值
		'''
		self.log.logger.info("")
		#添加人脸库，不输入名称
		r = self.facedb.facedb_add(fd_threshold=1)
		self.assertEqual(r['errorinfo'],-650)
		#添加人脸库，不输入阈值
		r = self.facedb.facedb_add(fd_name="error_test")
		self.assertEqual(r['errorinfo'],-651)

	@handle_exception
	def test_facedb_add_json_value_error(self):
		'''
		用例：restful串值有误：添加人脸库，名称输入为空；
		阈值输入为空、字符串、<0>1；
		'''
		self.log.logger.info("")
		#添加名称为空--应该是-651，开发准备改
		r = self.facedb.facedb_add(fd_name="",fd_threshold=0.4)
		self.assertEqual(r['errorinfo'],-650)
		#添加阈值为空
		r = self.facedb.facedb_add(fd_name="test",fd_threshold="")
		self.assertEqual(r['errorinfo'],-651)
		#添加阈值为字符串
		#r = self.facedb.facedb_add(name="test",threshold="阈值用字符串")
		#self.assertEqual(r['errorinfo'],-651)
		#添加阈值大于1
		r = self.facedb.facedb_add(fd_name="test",fd_threshold=100)
		self.assertEqual(r['errorinfo'],-651)
		#添加阈值小于0
		r = self.facedb.facedb_add(fd_name="test",fd_threshold=-100)
		self.assertEqual(r['errorinfo'],-651)

	@handle_exception
	def test_facedb_add_fail(self):
		'''
		由于server未对字符串长度做限制，但是数据库有长度限制。过长的字符串，导致添加失败。
		用例：添加人脸库，输入名称为>64位字符串，备注>256位字符串
		'''
		self.log.logger.info("")
		#添加人脸库，名称长度为大于64位字符串(70位)
		r = self.facedb.facedb_add(fd_name="1234567890123456789012345678901234567890\
									123456789012345678901234567890",fd_threshold=0.4)
		self.assertEqual(r['errorinfo'],-4)
		#输入人脸库，备注长度超过256位字符串(280位)
		remark = "0123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890123456789"
		r = self.facedb.facedb_add(fd_name="remark_long_test", fd_threshold=0.4,remark=remark)
		self.assertEqual(r['errorinfo'],-4)

	@handle_exception
	def test_facedb_delete(self):
		'''
		用例：删除人脸库
		'''
		self.log.logger.info("")
		#首先添加人脸库
		result = self.facedb.facedb_add(name="facedb_delete_test", threshold=1, remark="删除人脸库的用例测试")
		#验证删除人脸库成功
		d_r= self.facedb.facedb_delete(face_id=result['errorinfo'])
		self.assertEqual(d_r['errorinfo'], 0, "删除人脸库的测试中删除人脸库失败")
		#查询数据库验证该人脸库不存在
		db = DataBase.DataBase()
		self.items["db"] = db
		require_sql = "select * from frs_facedb where fd_id="+str(result['errorinfo'])
		require_result = db.fetch_all(require_sql)
		self.assertEqual(len(require_result), 0, "执行删除人脸库操作后，数据库未删除该人脸库")

	@handle_exception
	def test_facedb_delete_json_format_error(self):
		'''
		用例：删除人脸库，不传fd_id
		:return:
		'''
		r = self.facedb.facedb_delete()
		self.assertEqual(r["errorinfo"],-650)

	@handle_exception
	def test_facedb_delete_json_value_error(self):
		'''
		用例：删除人脸库，fd_id为空、fd_id为字符串
		:return:
		'''
		#fd_id为空
		r = self.facedb.facedb_delete(face_id="")
		self.assertEqual(r["errorinfo"], -651)
		#fd_id为字符串
		r = self.facedb.facedb_delete(face_id="ID为字符串")
		self.assertEqual(r["errorinfo"], -651)

	@handle_exception
	def test_facedb_delete_faceid_error(self):
		'''
		用例：删除人脸库，传入fd_id不存在、fd_id为空、fd_id为字符串
		:return:
		'''
		db  = DataBase.DataBase()
		self.items["db"] = db
		query_sql = "select max(fd_id) from frs_facedb"
		result = db.fetch_all(query_sql)
		#fd_id不存在
		r = self.facedb.facedb_delete(face_id=result[0][0]+2)
		self.assertEqual(r["errorinfo"], -6)


	@handle_exception
	def test_facedb_modify_name_threshold0_remark(self):
		'''
		用例：修改人脸库,修改人脸库名称、阈值和备注
		'''
		self.log.logger.info("")
		basic_fd = self.facedb.facedb_add(fd_name="modify_facedb_test", fd_threshold=1, remark="facedb")
		self.items["facedb"] = basic_fd
		time.sleep(2)
		facep = FacePerson.FacePerson()
		basic_person = facep.faceperson_add(p_name="facedb_modify_test", reg_type=1, grab_id=0, \
							   sex=1, cardId='123456', pic_name='50008.jpg', fd_id=basic_fd["errorinfo"])
		self.items["person"] = basic_person
		time.sleep(2)
		m_r = self.facedb.facedb_modify(fd_id=basic_fd["errorinfo"], fd_name="modify_face", fd_threshold=0.1, \
								   remark="修改了人脸库的名称、相似度和备注")
		self.assertEqual(m_r['errorinfo'], 0, "修改人脸库失败！")
		#查询数据库，验证是否修改成功
		db = DataBase.DataBase()
		require_sql = "select * from frs_facedb where fd_id="+str(basic_fd['errorinfo'])
		rdb_r = db.fetch_all(require_sql)
		db.close()
		self.assertNotEqual(len(rdb_r), 0, "更改后查询数据库，无该人脸库信息")
		self.assertEqual(rdb_r[0][1],"modify_face")
		self.assertEqual(rdb_r[0][2], 0.1)
		self.assertEqual(rdb_r[0][3], "修改了人脸库的名称、相似度和备注")
		#比对与在库人脸完全不同的照片，因为相似度为0.1，比对成功
		compare = RequestVideoDetect.RequestVideoDetect()
		self.items["compare"] = compare
		compare.connect()
		compare_r = compare.grab_and_match(pic_name='50159.jpg', max_face_num=5,\
									   facedb_id=[basic_fd["errorinfo"]], channel_name='channel_test')
		self.assertEqual(compare_r, 0, "未抓取到人脸")
		time.sleep(5)
		db = DataBase.DataBase()
		result_sql = "SELECT * from frs_result where pid1="+str(basic_person['errorinfo'])
		result_r = db.fetch_all(result_sql)
		self.items["db"] = db
		self.assertNotEqual(result_r[0][0], 0, "修改人脸库相似值为0.1,仍比对失败")

	@handle_exception
	def test_facedb_modify_json_format_error(self):
		'''
		用例：修改人脸库，不输入必填项fd_id，
		'''
		#不填写fd_id
		r = self.facedb.facedb_modify(fd_name="no_fd_id", fd_threshold=0.2, remark="测试不输入fd_id")
		self.assertEqual(r["errorinfo"],-650)

	@handle_exception
	def test_facedb_modify_json_value_error(self):
		'''
		用例：修改人脸库，名称输入为空；阈值输入为空、字符串、<0、>1
		'''
		#创建人脸库，用于修改
		result = self.facedb.facedb_add(fd_name="modify_basic", fd_threshold=0.5)
		self.items["facedb"] = result
		#名称输入为空
		r = self.facedb.facedb_modify(fd_id=result["errorinfo"], fd_name="", fd_threshold=0.5)
		self.assertEqual(r["errorinfo"],0)
		#阈值输入为空
		#r = self.facedb.facedb_modify(fd_id=result["errorinfo"], fd_name="modify_basic", fd_threshold="")
		#self.assertEqual(r["errorinfo"],-651)
		#阈值输入为字符串
		#r = self.facedb.facedb_modify(fd_id=result["errorinfo"], fd_name="modify_basic", fd_threshold="阈值为字符串")
		#self.assertEqual(r["errorinfo"],-651)
		#阈值输入<0
		r = self.facedb.facedb_modify(fd_id=result["errorinfo"], fd_name="modify_basic", fd_threshold=-100)
		self.assertEqual(r["errorinfo"],-651)
		#阈值输入>1
		r = self.facedb.facedb_modify(fd_id=result["errorinfo"], fd_name="modify_basic", fd_threshold=100)
		self.assertEqual(r["errorinfo"],-651)

	@handle_exception
	def test_facedb_modify_error_faceid(self):
		'''
		用例：修改人脸库，传的id不存在
		:return:
		'''
		db  = DataBase.DataBase()
		self.items["db"] = db
		query_sql = "select max(fd_id) from frs_facedb"
		result = db.fetch_all(query_sql)
		#id不存在
		r = self.facedb.facedb_modify(fd_id=result[0][0]+2,fd_name="test", fd_threshold=1)
		self.assertEqual(r["errorinfo"], -6)
		#id格式错误
		r = self.facedb.facedb_modify(fd_id="ID为字符串",fd_name="test", fd_threshold=1)
		self.assertEqual(r["errorinfo"], -6)

	@handle_exception
	def test_facedb_modify_fail(self):
		'''
		用例：修改人脸库，输入名称为>64位字符串，备注>256位字符串
		:return:
		'''
		#创建人脸库，用于修改
		result = self.facedb.facedb_add(fd_name="modify_basic", fd_threshold=0.5)
		self.items["facedb"] = result
		#修改名称>64位
		name = "1234567890123456789012345678901234567890\
				123456789012345678901234567890"
		r = self.facedb.facedb_modify(fd_id=result["errorinfo"], fd_name=name, fd_threshold=0.5)
		self.assertEqual(r["errorinfo"], -2)
		#修改备注>128位
		remark = "0123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890\
				  123456789012345678901234567890123456789"
		r = self.facedb.facedb_modify(fd_id=result["errorinfo"], fd_name="modify_basic", fd_threshold=0.5, remark=remark)
		self.assertEqual(r["errorinfo"], -2)


if __name__ == "__main__":
	#unittest.main()
	r_suite = unittest.TestSuite()
	r_suite.addTest(FaceDBTestCase('test_facedb_delete_json_value_error'))
	#r_suite.addTest(FaceDBTestCase('test_facedb_modify_json_format_error'))
	#r_suite.addTest(FaceDBTestCase('test_facedb_add_json_format_error'))
	#r_suite.addTest(FaceDBTestCase('test_facedb_add_json_value_error'))
	#r_suite.addTest(FaceDBTestCase('test_facedb_add_fail'))
	unittest.TextTestRunner().run(r_suite)
