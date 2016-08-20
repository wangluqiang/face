#coding=utf-8
import unittest,time
import sys,os
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import DataBase
import RequestVideoDetect
import FaceDB
import FacePerson
import LogConfig
import DMExceptions

class RequestVideoDetectTestCase(unittest.TestCase):
    def setUp(self):
         '''
         功能：测试使用的初始化环境
         '''
         self.log = LogConfig.Logger()
         try:
            self.videodetect = RequestVideoDetect.RequestVideoDetect()
         except RequestVideoDetect.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoDetect初始化失败！")
         
    def tearDown(self):
        '''
        功能：测试清理环境使用
        '''
        self.videodetect.close()
        
    def test_libmulti_onvif_face1_picjpg_picless1M_alllib(self):
        '''
        功能：人脸库中存在多张某个人脸的图片，模拟用onvif方式向比对端发送一张单个人脸的jpg格式的图片，大小为1M以下，检索人脸库为全部人脸库
        预期结果：函数返回值为0，表frs_grab增加了一项，frs_result中也增加一项
        '''
        self.log.logger.info("")
        try:
            #增加新的人脸库，用于模拟多人脸库情况
            fd = FaceDB.FaceDB()
            r_1 = fd.facedb_add(name='usedformatchtest_1', threshold=0.8, remark='用户验证比对功能时添加的人脸库')
            r_2 = fd.facedb_add(name='usedformatchtest_2', threshold=0.8, remark='用户验证比对功能时添加的人脸库')
            #查询数据库，获取全部人脸库的ID
            db = DataBase.DataBase()
            all_fd = db.fetch_all('SELECT fd_id from frs_facedb')
            #关闭数据库
            db.close()
            fd_list = []
            for each in all_fd:
                fd_list.append(each[0])
            result = self.send_pic_to_match(match_pic_name='范冰冰非证件单人照.jpg', fd_list=fd_list)
            self.assertGreater(len(result[0]), 0, "单张人脸照，插入抓取库失败")
            #验证比对结果新增记录
            self.assertGreater(len(result[1]), 0, "比对结果失败")
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("向服务器发送请求后，收到的响应有问题！")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("返回的http应答json格式不正确！")
        finally:
            if 'r_1' in locals().keys():              
                fd.facedb_delete(face_id=r_1['errorinfo'])
            if 'r_2' in locals().keys():    
                fd.facedb_delete(face_id=r_2['errorinfo'])  
        
    def test_libmulti_onvif_face3_picjpg_picless1m_multilib(self):
        '''
        功能：人脸库中存在多张多人脸的图片，模拟用onvif方式向比对端发送一张多人脸的jpg格式的图片，大小为1M以下，max_face为2，检索人脸库为多个人脸库
        '''
        self.log.logger.info("")
        try:
            #增加新的人脸库，用于模拟多人脸库情况
            fd = FaceDB.FaceDB()
            r_1 = fd.facedb_add(name='usedformatchtest_1', threshold=0.8, remark='用户验证比对功能时添加的人脸库')
            r_2 = fd.facedb_add(name='usedformatchtest_2', threshold=0.8, remark='用户验证比对功能时添加的人脸库')
            #发送一张多人脸照片，验证比对结果
            facedb_name = ['facedb_test', 'usedformatchtest_1', 'usedformatchtest_2']
            result = self.send_pic_to_match(match_pic_name='范冰冰多人合照 .jpg', fd_name_list=facedb_name)
            self.assertEqual(len(result[0]), 3, "图片有三张人脸，抓取人脸数不是3")
            #验证比对结果新增记录
            self.assertGreater(len(result[1]), 0, "比对结果失败")
            self.assertLessEqual(len(result[1]), 3, "共三张人脸，比对结果大于3")
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("向服务器发送请求后，收到的响应有问题！")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("返回的http应答json格式不正确！")
        finally:
            if 'r_1' in locals().keys():              
                fd.facedb_delete(face_id=r_1['errorinfo'])
            if 'r_2' in locals().keys():    
                fd.facedb_delete(face_id=r_2['errorinfo'])     
    
    def test_libmulti_onvif_facemulti_picpng_libspecific(self):
        '''
        用例：某个人脸库中存在多张某个人脸的图片，模拟用onvif方式向比对端发送一张多个人脸的png格式的图片，检索人脸库为某特定人脸库
        '''
        self.log.logger.info("")
        result = self.send_pic_to_match(match_pic_name='范冰冰多人合照 .png', fd_name_list=["facedb_test"])
        time.sleep(5)
        self.assertEqual(len(result[0]), 3, "图片有三张人脸，抓取人脸数不是3")
        #验证比对结果新增记录
        self.assertGreater(len(result[1]), 0, "比对结果失败")
        self.assertLessEqual(len(result[1]), 3, "共三张人脸，比对结果大于3")
                
    def test_facedb1_onvif_facemore_picbmp_picless1m_libspecific(self):
        '''
        用例：某个人脸库中存在1张某个人脸的图片，模拟用onvif方式向比对端发送一张单人脸的bmp格式的图片，大小为1M以上，检索人脸库为某特定人脸库
        '''
        self.log.logger.info("")
        try:
            #添加人脸库
            fd = FaceDB.FaceDB()
            r = fd.facedb_add(name="testforonlyonematch", threshold=0.9, remark="用于测试人脸库中仅有一个匹配 人员情况")
            person = FacePerson.FacePerson()
            p_1 = {"p_name":"孙俪", "reg_type":1, "sex":1, "cardId":"123456778", "pic_name":"孙俪.jpg", "fd_id":r["errorinfo"]}
            p_2 = {"p_name":"景甜", "reg_type":1, "sex":1, "cardId":"122211122", "pic_name":"景甜.jpg", "fd_id":r["errorinfo"]}
            p_1_r = person.faceperson_add(**p_1)
            p_2_r = person.faceperson_add(**p_2)
            result = self.send_pic_to_match(match_pic_name='孙俪单人照.bmp', fd_list=[r["errorinfo"]])
            time.sleep(5)
            self.assertGreater(len(result[0]), 0, "单张人脸照，插入抓取库失败")
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("向服务器发送请求后，收到的响应有问题！")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("返回的http应答json格式不正确！")
        finally:
            #删除人员
            if "p_1_r" in locals().keys():
                person.faceperson_delete(p_id=p_1_r["errorinfo"])
            if "p_2_r" in locals().keys():
                person.faceperson_delete(p_id=p_2_r["errorinfo"])
            #删除人脸库
            if 'r' in locals().keys():
                fd.facedb_delete(face_id=r["errorinfo"])
        
    def test_otherlibmulti_onvif_picpng_facemulti_picless1m_nofacelibspecific(self):
        '''
        用例：某个人脸库中存在多张某个人脸的图片，模拟用onvif方式向比对端发送一张多个人脸的png格式的图片，大小为1M以下，检索人脸库为不存在该人脸的某特定人脸库
        '''  
        self.log.logger.info("")  
        try:
            #新建一个不存在该人脸图片的库
            fd = FaceDB.FaceDB()
            r = fd.facedb_add(name="testfornomatch", threshold=0.9, remark="用于测试不存在所需人脸图片的库")
            person = FacePerson.FacePerson()
            p_1 = {"p_name":"孙俪", "reg_type":1, "sex":1, "cardId":"123456778", "pic_name":"孙俪.jpg", "fd_id":r["errorinfo"]}
            p_2 = {"p_name":"景甜", "reg_type":1, "sex":1, "cardId":"122211122", "pic_name":"景甜.jpg", "fd_id":r["errorinfo"]}
            p_1_r = person.faceperson_add(**p_1)
            p_2_r = person.faceperson_add(**p_2)
            result = self.send_pic_to_match(match_pic_name='范冰冰多人合照 .png', fd_list=[r["errorinfo"]])
            time.sleep(3)
            self.assertEqual(len(result[0]), 3, "发送图片中有三张人脸，抓拍不是3")
            self.assertEqual(len(result[1]), 0, "指定库中没有符合要求的图片，仍有比对结果")
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("向服务器发送请求后，收到的响应有问题！")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("返回的http应答json格式不正确！")
        finally:
            #删除人员
            if "p_1_r" in locals().keys():
                person.faceperson_delete(p_id=p_1_r["errorinfo"])
            if "p_2_r" in locals().keys():
                person.faceperson_delete(p_id=p_2_r["errorinfo"])
            #删除人脸库
            if 'r' in locals().keys():
                fd.facedb_delete(face_id=r["errorinfo"])    
        
    def test_onvif_noface(self):
        '''
        用例：模拟用onvif方式发送无人脸图片给比对服务
        ''' 
        self.log.logger.info("")
        result = self.send_pic_to_match(match_pic_name='car.jpg', fd_name_list=["facedb_test"])
        self.assertEqual(len(result[0]), 0, "发送非人脸图片后，添加到抓拍库")

    #发送图片到比对，返回发送后的抓拍结果和比对结果
    def send_pic_to_match(self,match_pic_name, fd_list=None, fd_name_list=None, c_name="invalid_channel_test"):
        try:
            db = DataBase.DataBase()
            #查询无效通道的ID
            invalid_cid = db.fetch_all("select c_id from frs_channel where c_name='invalid_channel_test'")[0][0]
            #查询目前最大的抓拍人员ID和结果ID
            grab_count = db.fetch_all('select max(grab_id) from frs_grab')[0][0]
            result_count = db.fetch_all('select max(r_id) from frs_result')[0][0]
            db.close()
            self.videodetect.connect()
            if fd_list:
                result = self.videodetect.grab_and_match(pic_name=match_pic_name, facedb_id=fd_list, channel_name=c_name)
            else:
                result = self.videodetect.grab_and_match(pic_name=match_pic_name, facedb_name=fd_name_list, channel_name=c_name)
            time.sleep(3)
            #验证返回结果为0
            self.assertEqual(result, 0, "比对服务接收图片失败")
            #查询发送图片后抓拍数据和比对数据
            db = DataBase.DataBase()
            grab_sql = "select * from frs_grab_condition where id > "+str(grab_count)+" and c_id="+str(invalid_cid)
            result_sql = "select * from frs_result where r_id > "+str(result_count)+"  and c_id="+str(invalid_cid)
            grab_r = db.fetch_all(grab_sql)
            result_r = db.fetch_all(result_sql)
            db.close()
            return (grab_r,result_r)
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败")
        finally:
            if db.conn:
                db.close()


if __name__ == "__main__":

    #unittest.main()
    r_suite = unittest.TestSuite()
    #r_suite.addTest(RequestVideoDetectTestCase('test_facedb1_onvif_facemore_picbmp_picless1m_libspecific'))
    r_suite.addTest(RequestVideoDetectTestCase('test_libmulti_onvif_facemulti_picpng_libspecific'))
    unittest.TextTestRunner().run(r_suite)