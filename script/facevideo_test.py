#coding=utf8
import json
import sys
import sys
import unittest
import os
import time
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import LogConfig
import DataBase
import FaceVideo
import DMExceptions
from handle_exception import handle_exception

class FaceVideoTestCase(unittest.TestCase):
    def setUp(self):  
        self.face_video_class = FaceVideo.FaceVideo()   ##实例化了被测试模块中的类  
        self.log = LogConfig.Logger()
        self.items = {}

    #退出清理工作  
    def tearDown(self):  
        pass  
    
    @handle_exception
    def test_facevideo_add_right_name(self):
        '''
        用例：添加有效视频文件
        :return:
        '''
        self.log.logger.info("")
        result = self.face_video_class.facevideo_add('add.mp4')
        self.assertGreater(result["video_id"], 0)
        #print(result)
        video_id = result.get('video_id')
        video = DataBase.DataBase()
        video_ids = video.fetch_all('SELECT count(*) FROM `frs_channel` where type=1 and c_id='+str(video_id))
        require_sql = "select * from frs_channel where c_id="+str(result['video_id'])
        require_result = video.fetch_all(require_sql)
        video.close()
        self.assertMultiLineEqual(require_result[0][2], result["video_name"], 'add facevideo name error')
        self.assertEqual(require_result[0][5], 1, 'add facevideo type error')
        self.assertEqual(video_ids[0][0],1,'video insert db fail')

    @handle_exception
    def test_facevideo_add_json_value_error(self):
        self.log.logger.info("")
        longer_128 = "123456789012345678901234567890\
                      123456789012345678901234567890\
                      123456789012345678901234567890\
                      123456789012345678901234567890\
                      1234567890123456789012345678901234567890"
        result = self.face_video_class.facevideo_add('addmp4')
        print(result)
        #print(result)
        self.assertEqual(result.get('errorinfo'),-651)
        result = self.face_video_class.facevideo_add(name=longer_128)
        print(result)
        self.assertEqual(result.get('errorinfo'),-651)

    @handle_exception
    def test_facevideo_add_name_used(self):
        '''
        用例：添加视频文件名称已存在
        预期结果：添加成功，自动更新命名
        :return:
        '''
        self.log.logger.info("")
        result = self.face_video_class.facevideo_add(name="test_used.avi")
        self.items["video"] = [result]
        #添加已有视频
        r = self.face_video_class.facevideo_add(name="test_used.avi")
        self.assertGreater(r["video_id"], 0)
        self.items["video"].append(r)

    @handle_exception
    def test_facevideo_delete_right(self):
        self.log.logger.info("")
        results = self.face_video_class.facevideo_add("add_face_video.mp4")
        result = self.face_video_class.facevideo_delete(results['video_id'])
        self.assertEqual(result["errorinfo"], 0,str(id)+' delete fail')
        db = DataBase.DataBase()
        require_sql = "select * from frs_channel where c_id="+str(results['video_id'])
        require_result = db.fetch_all(require_sql)
        db.close()
        self.assertEqual(len(require_result), 0, "执行删除视频文件操作后，数据库未删除该视频文件")

    @handle_exception
    def test_facevideo_delete_invalid(self):
        self.log.logger.info("")
        db = DataBase.DataBase()
        query_sql = "select max(c_id) from frs_channel"
        r = db.fetch_all(query_sql)
        result = self.face_video_class.facevideo_delete(id=r[0][0]+2)
        self.assertEqual(result["errorinfo"], -6,str(id)+' delete fail')

    @handle_exception
    def test_facevideo_delete_json_value_error(self):
        self.log.logger.info("")
        #输入id为字符串
        result = self.face_video_class.facevideo_delete(id='q8945213697')
        self.assertEqual(result["errorinfo"], -651,str(id)+' delete fail')
        #输入id为空
        result = self.face_video_class.facevideo_delete(id="")
        self.assertEqual(result["errorinfo"], -651,str(id)+' delete fail')
        #不传入ID
        result = self.face_video_class.facevideo_delete()
        self.assertEqual(result["errorinfo"], -651,str(id)+' delete fail')

    @handle_exception
    def testfacevideo_query(self):
        self.log.logger.info("")
        result = self.face_video_class.facevideo_query()
        db = DataBase.DataBase()
        require_sql = "select count(*) from frs_channel where type=1"
        require_result = db.fetch_all(require_sql)
        db.close()
        self.assertEqual(len(result), require_result[0][0], 'query fail')

if __name__ == "__main__":
    #unittest.main(exit=False)
    
    r_suite = unittest.TestSuite()
    r_suite.addTest(FaceVideoTestCase('test_facevideo_delete_json_value_error'))
    unittest.TextTestRunner().run(r_suite)
    