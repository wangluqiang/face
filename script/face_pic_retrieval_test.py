#coding=utf-8
import unittest
import sys,os
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import DataBase
import FaceDB
import FacePicRetrieval
import LogConfig
import DMExceptions

class FacePicRetrievalTestCase(unittest.TestCase):
    
    def setUp(self):
        '''
        功能：测试初始化环境设置
        '''
        self.log = LogConfig.Logger()
        try:
            self.face_retrieval = FacePicRetrieval.FacePicRetrieval()
        except DMExceptions.FacePicRetrievalInitException as ex:
            self.fail("FacePicRetrieval初始化失败！")
    
    def tearDown(self):
        '''
        功能：测试环境清理
        '''
        self.face_retrieval.close()
    
    def test_lib15_face1_picless1M_picjpg_return1(self):
        '''
        用例：人脸库中存在多15个匹配照片，模拟server发送jpg格式的单个人脸的照片，照片大小小于1M，查询所有人脸库，阈值为0.8，返回个数为1
        '''
        self.log.logger.info("")
        try:
            #脚本测试初始化环境中有15张相同的范冰冰证件照片
            self.face_retrieval.connect()
            result = self.face_retrieval.match(pic_name="范冰冰.jpg", threshold=0.8, pic_num=1)
            #验证返回结果是否正确
            self.assertEqual(result.success_flag, 1, '相同照片为比对成功！')
            self.assertEqual(len(result.info), 1, '设置返回个数为1，但结果不是1')
            self.assertGreaterEqual(result.info[0].score, 0.8, '查询设置相似度为0.8，返回结果小于该值')
            #查询数据库，查找facedb_test的人脸库ID和person_test_1_\d的人员ID
            db = DataBase.DataBase()
            facedb_r = db.fetch_all("select fd_id from frs_facedb where fd_name='facedb_test'")
            person_r = db.fetch_all("select p_id from frs_person where p_name regexp 'person_test_1_[0-9]*'")
            self.assertEqual(result.info[0].face_db, facedb_r[0][0], "返回的人脸库信息错误")
            person_id = []
            for p in person_r:
                person_id.append(p[0])
            self.assertIn(result.info[0].p_id, person_id, "比对结果失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败")
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!") 
        finally:
            #关闭数据库
            if 'db' in locals().keys():
                db.close()
    
    def test_lib15_facedbtest_face3_picless1M_picpng_threshold5_return12(self):
        '''
        用例：某个人脸库中存在15个匹配照片，模拟server发送png格式的多个人脸的照片，照片大小小于1M，查询某个特定人脸库，阈值为0.5，返回个数为12
        '''
        self.log.logger.info("")
        try:
            #脚本运行初始化环境时有15张范冰冰证件照的注册，发送范冰冰多人合照的照片
            self.face_retrieval.connect()
            result = self.face_retrieval.match(pic_name="范冰冰多人合照 .png", threshold=0.5, pic_num=12, facedb_name='facedb_test')
            #验证返回成功的标志位为1
            self.assertEqual(result.success_flag, 1, "阈值设为0.5，有15个相同人脸的情况下仍比对失败")
            #查询数据库，人脸库ID和人员ID
            db = DataBase.DataBase()
            facedb_r = db.fetch_all("select fd_id from frs_facedb where fd_name='facedb_test'")
            person_r = db.fetch_all("select p_id from frs_person where p_name regexp 'person_test_1_[0-9]*'")
            person_id = []
            for p in person_r:
                person_id.append(p[0])
            #验证返回个数为设置的12
            self.assertEqual(len(result.info), 12, '设置返回个数为12，有15个相同人脸的情况下个数不等于12')
            for pic_info in result.info:
                #验证返回所有结果的得分大于设置的相似度0.5
                self.assertGreaterEqual(pic_info.score, 0.5, '设置相似度为0.5，返回结果相似度小于0.5')
                #验证返回所有结果的人脸库正确
                self.assertEqual(pic_info.face_db, facedb_r[0][0], '返回结果的查询人脸库失败')
                self.assertIn(pic_info.p_id, person_id, '比对结果的人员失败')
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败")
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!") 
        finally:
            if 'db' in locals().keys():
                db.close()        
        
    def test_lib15_uselib0_picbmp_picmore1M_usealllib_threshold9_return20(self):
        '''
        用例：人脸库中存在15个匹配照片，模拟server发送bmp格式的单个人脸的照片，照片大小大于1M，查询全部人脸库，阈值为0.9，返回个数为20
        预期结果：
        '''
        pass
    
    def test_otherlib15_face1_picjpg_picless1m_threshold9_return12(self):
        '''
        用例：某个人脸库中存在15个匹配照片，模拟server发送jpg格式的单人脸的照片，照片大小小于1M，查询不存在该人脸的人脸库，阈值为0.9，返回个数为12
        '''
        self.log.logger.info("")
        try:
            #新建一个不存在需查询照片的人脸库
            fd = FaceDB.FaceDB()
            fd_r = fd.facedb_add(name='usedfortest', threshold=0.4, remark='测试比对服务时，暂用的人脸库')
            #使用该人脸库查询
            self.face_retrieval.connect()
            result = self.face_retrieval.match(pic_name="范冰冰.jpg", threshold=0.8, pic_num=1, facedb_name='usedfortest')
            self.assertEqual(result.success_flag, 1, "图片处理和提取特征失败")
            self.assertEqual(len(result.info), 0 , "该人脸库无匹配图片，但是匹配成功")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败")
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the facedb add response is not a standard json format!")  
        finally:
            #删除人脸库
            if 'fd' in locals().keys():
                fd.facedb_delete(face_id=fd_r['errorinfo'])
        
    def test_noface_picjpg(self):
        '''
        用例：模拟server发送不存在人脸的jpg格式的图片
        预期结果：返回success_flag=0
        '''
        self.log.logger.info("")    
        try:
            self.face_retrieval.connect()
            result = self.face_retrieval.match(pic_name="car.jpg", threshold=0.8, pic_num=1)
            #print(result)
            self.assertEqual(result.success_flag, 0, "发送无人脸图片，检测到人脸")
            self.assertEqual(len(result.info), 0, "发送无人脸图片，比对到在库人员")   
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
        
    
if __name__ == '__main__':
    '''
    suite = unittest.TestSuite()
    suite.addTest(FacePicRetrievalTestCase('test_lib15_face1_picless1M_picjpg_return1'))
    unittest.TextTestRunner().run(suite)
    '''
    unittest.main()