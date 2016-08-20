#coding=utf8
import json
import sys
import unittest
import os
import time,datetime
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import FaceVideoRetrieval
import FaceVideo
import FaceDB
import DataBase
import FacePerson
import RequestVideoFileDetect
import SearchGrabPic
import LogConfig
import DMExceptions
from handle_exception import handle_exception
from Base import get_id_by_name
from Base import get_max_id

class SearchGrabPicTestCase(unittest.TestCase):

    def setUp(self):  
        self.search_grab_pic_class = SearchGrabPic.SearchGrabPic()
        self.log = LogConfig.Logger()
        self.items = {}
        self.c_id = get_id_by_name(ip=self.search_grab_pic_class.db_ip, port=self.search_grab_pic_class.db_port, name=self.search_grab_pic_class.db_name, \
                                       user=self.search_grab_pic_class.db_user, passwd=self.search_grab_pic_class.db_passwd, type="channel", by_name="channel_test")
        self.fd_id = get_id_by_name(ip=self.search_grab_pic_class.db_ip, port=self.search_grab_pic_class.db_port, name=self.search_grab_pic_class.db_name, \
                                       user=self.search_grab_pic_class.db_user, passwd=self.search_grab_pic_class.db_passwd, type="facedb", by_name="facedb_test")
        facevideo = RequestVideoFileDetect.RequestVideoDetect()
        facevideo.connect()
        r = facevideo.request_video_detect(c_id = self.c_id, pic='50010.jpg', max_face=10, face_db_list=[self.fd_id], for_num=10)
        time.sleep(10)
        facevideo.close()
        #print(self.c_id)
    def tearDown(self):
        pass

    @handle_exception
    def test_right_cid_right_pic_right_time_right_score_right_return(self):
        self.log.logger.info("")
        SearchPic_test = SearchGrabPic.SearchGrabPic()
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_start = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        result = SearchPic_test.facepic_grab_search(channel_id =[self.c_id], pic_name='50010.jpg', time=[time_start,time_now], threshold=0.1, return_num=10)
        #print(result)
        return_data = result.get('return_data')
        #print(return_data[0].keys())
        grab = DataBase.DataBase()
        grab_id = grab.fetch_all("select id from frs_grab_condition where c_id = "+str(self.c_id))
        grab.close()
        grab_ids = []
        for id in grab_id:
            grab_ids.append(id[0])
        self.assertLessEqual(len(return_data),10 , 'return_num fail')
        self.assertGreater(len(return_data),0 , 'return_num fail')
        self.assertLessEqual(len(return_data),len(grab_ids) , ' fail')
        for data in return_data:
            self.assertGreaterEqual(data.get('score'), 0, 'score fail')
            self.assertLessEqual(data.get('score'), 1, 'score fail')
            self.assertTrue(data.get('time')<time_now, 'time fail')
            self.assertTrue(data.get('time')>time_start, 'time fail')
            self.assertIn(data.get('grab_id'), grab_ids, 'grab_id fail')

    @handle_exception
    def test_search_grabface_json_format_error(self):
        '''
        用例：json格式错误：不传入图片、时间、相似度、返回个数、通道ID
        '''
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_start = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        #不传入图片
        r = self.search_grab_pic_class.facepic_grab_search(channel_id =[self.c_id], time=[time_start,time_now], threshold=0.1, return_num=10)
        print(r)
        #不传入时间
        r = self.search_grab_pic_class.facepic_grab_search(pic_name='50010.jpg', channel_id =[self.c_id], threshold=0.1, return_num=10)
        print(r)
        #不传入相似度
        r = self.search_grab_pic_class.facepic_grab_search(pic_name='50010.jpg', time=[time_start,time_now], channel_id =[self.c_id], return_num=10)
        print(r)
        #不传入通道ID
        r = self.search_grab_pic_class.facepic_grab_search(pic_name='50010.jpg', time=[time_start,time_now], threshold=0.1, return_num=10)
        print(r)
        #不传入返回个数
        r = self.search_grab_pic_class.facepic_grab_search(pic_name='50010.jpg', channel_id =[self.c_id], time=[time_start,time_now], threshold=0.1)
        print(r)

    @handle_exception
    def test_search_grabface_json_value_error(self):
        '''
        用例：json值错误：
        图片为字符串、“”;
        时间为不符合格式要求的时间，“”，很长；
        相似度为<0、>1、小数点后很长、字符串、“”、很长字符串；
        返回个数为字符串、“”、0、<0、很大；
        通道ID为不存在ID、字符串、“”、很长字符串
        '''
        self.log.logger.info("")
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_start = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        longer_64 = "1234567890123456789012345678901234567890\
                    1234567890123456789012345678901234567890"
        #输入图片为字符串
        #r = self.search_grab_pic_class.facepic_grab_search(pic_name="dasfajksfjasjfjas",channel_id=[self.c_id], time=[time_start, time_now],\
        #                                               threshold=0.4, return_num=10)
        #print(r)
        #输入图片为空
        #r = self.search_grab_pic_class.facepic_grab_search(pic_name="",channel_id=[self.c_id], time=[time_start, time_now],\
         #                                              threshold=0.4, return_num=10)
        #print(r)
        #输入时间为不符合格式要求的时间
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=["2015.12.7 11:11", "2015.12.8 13:13"],\
                                                       threshold=0.4, return_num=10)
        print(r)
        #输入时间为空
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time="",\
                                                           threshold=0.4, return_num=10)
        print(r)
        #输入时间为很长字符串
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time="jajsfjajfkasjfjdasliopeirqiworiqerpqwoerpo[qworqworjfk",\
                                                           threshold=0.4, return_num=10)
        print(r)
        #输入相似度<0
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold=-100, return_num=10)
        print(r)
        #输入相似度>1
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold=100, return_num=10)
        print(r)
        #输入相似度小数点后很多位
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold=0.1111111111111111111111111111111111111111111111, return_num=10)
        print(r)
        #输入相似度为字符串
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold="相似度为字符串", return_num=10)
        print(r)
        #输入相似度为“”
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold="", return_num=10)
        print(r)
        #输入相似度为很长字符串
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold=longer_64, return_num=10)
        print(r)
        #输入返回个数为字符串
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold=0.5, return_num="返回个数为字符串")
        print(r)
        #输入返回个数为""
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold=0.5, return_num="")
        print(r)
        #输入返回个数为0
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold=0.5, return_num=0)
        print(r)
        #输入返回个数<0
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                           threshold=0.5, return_num=-100)
        print(r)
        #输入通道ID为字符串
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id="通道ID为字符串", time=[time_start, time_now],\
                                                           threshold=0.5, return_num=12)
        print(r)
        #输入通道ID为“”
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id="", time=[time_start, time_now],\
                                                           threshold=0.5, return_num=12)
        print(r)
        #输入通道ID为很长字符串
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=longer_64, time=[time_start, time_now],\
                                                           threshold=0.5, return_num=12)
        print(r)

    @handle_exception
    def test_search_grabface_pic_noface(self):
        '''
        用例：检索时上传无人脸图片
        '''
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_start = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="car.jpg",channel_id=[self.c_id], time=[time_start, time_now],\
                                                       threshold=0.4, return_num=10)
        self.assertTrue(r["errorinfo"], -102)

    @handle_exception
    def test_search_grabface_channelID_no_exists(self):
        '''
        用例：检索时输入不存在的通道ID
        '''
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_start = (datetime.datetime.now()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        max_id = get_max_id(ip=self.search_grab_pic_class.db_ip, port=self.search_grab_pic_class.db_port, name=self.search_grab_pic_class.db_name, \
                                       user=self.search_grab_pic_class.db_user, passwd=self.search_grab_pic_class.db_passwd, type="channel")
        r = self.search_grab_pic_class.facepic_grab_search(pic_name="50010.jpg",channel_id=[max_id+10], time=[time_start, time_now],\
                                                       threshold=0.4, return_num=10)
        self.assertTrue(r["errorinfo"], -102)
        
if __name__ == "__main__":
    #unittest.main()

    r_suite = unittest.TestSuite()
    
    #r_suite.addTest(SearchGrabPicTestCase('test_search_grabface_json_format_error'))
    r_suite.addTest(SearchGrabPicTestCase('test_search_grabface_channelID_no_exists'))
    #r_suite.addTest(SearchGrabPicTestCase('test_search_grabface_channelID_no_exists'))
    #r_suite.addTest(SearchGrabPicTestCase('test_right_cid_right_pic_string_time_right_score_right_return'))
    unittest.TextTestRunner().run(r_suite)

    '''
    r_suite.addTest(SearchGrabPicTestCase('test_right_cid_right_pic_right_time_right_score_right_return'))  
    
    r_suite.addTest(SearchGrabPicTestCase('test_invalid_cid_right_pic_right_time_right_score_right_return'))
    r_suite.addTest(SearchGrabPicTestCase('test_int_cid_right_pic_right_time_right_score_right_return'))
    

    r_suite.addTest(SearchGrabPicTestCase('test_right_cid_moreface_pic_right_time_right_score_right_return'))   
    r_suite.addTest(SearchGrabPicTestCase('test_right_cid_no_pic_right_time_right_score_right_return'))
     
    r_suite.addTest(SearchGrabPicTestCase('test_right_cid_right_pic_right_time_invalid_score_right_return'))  
    r_suite.addTest(SearchGrabPicTestCase('test_right_cid_right_pic_right_time_list_score_right_return'))    
    r_suite.addTest(SearchGrabPicTestCase('test_right_cid_right_pic_right_time_no_score_right_return'))      
    r_suite.addTest(SearchGrabPicTestCase('test_right_cid_right_pic_string_time_right_score_right_return'))
    #r_suite.addTest(SearchGrabPicTestCase('test_no_cid_right_pic_right_time_right_score_right_return'))  
    #r_suite.addTest(SearchGrabPicTestCase('test_right_cid_right_pic_no_time_right_score_right_return'))
    unittest.TextTestRunner().run(r_suite)
        '''