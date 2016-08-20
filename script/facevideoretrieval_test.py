#coding=utf8
import json
import sys
import unittest
import os
import time
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import FaceVideoRetrieval
import FaceVideo
import FaceDB
import DataBase
import FacePerson
import RequestVideoFileDetect
import LogConfig
import DMExceptions


class FaceVideoRetrievalTestCase(unittest.TestCase):
    def setUp(self):  
        self.face_video_retrieval_class = FaceVideoRetrieval.FaceVideoRetrieval()     
        self.face_video_class=FaceVideo.FaceVideo()
        self.log = LogConfig.Logger()
        video = DataBase.DataBase()
        channel_id = video.fetch_all("select c_id from `frs_channel` where c_name = 'test_video.avi'")
        face_id = video.fetch_all("select fd_id from `frs_facedb` where fd_name = 'facedb_test'")
        video.close()
        self.c_id = channel_id[0][0]
        self.fd_id = face_id[0][0]
        facevideo = RequestVideoFileDetect.RequestVideoDetect()
        facevideo.connect()
        r = facevideo.request_video_detect(c_id = self.c_id, pic='50008.jpg', max_face=10, face_db_list=[self.fd_id], for_num=10)
        time.sleep(3)
        facevideo.close()
    def tearDown(self):  
        clear = DataBase.DataBase()   
        grab = clear.update("delete g.* from frs_grab g,frs_grab_condition gc  where g.grab_id=gc.grab_id and gc.c_id ="+str(self.c_id))
        grab_condition = clear.update("delete from frs_grab_condition where c_id= "+str(self.c_id))
        result = clear.update("delete  from frs_result where c_id ="+str(self.c_id))
        clear.close()
    def testsearch_realtime_video_right_cid(self):
        #视频文件实时结果查询，传正确的c_id
        self.log.logger.info("视频文件实时结果查询，传正确的c_id")
        try:
            result_tmp = self.face_video_retrieval_class.search_realtime_video(c_id=[self.c_id])
            result = result_tmp
            #print(result)
            video = DataBase.DataBase()
            video_id = video.fetch_all('SELECT count(*) FROM `frs_channel` where type=1 and c_id='+str(self.c_id))
            video_result = video.fetch_all('select count(*) from `frs_result` where c_id='+str(self.c_id))
            video.close()
            #print(video_result[0][0])
            #print(len(result.get('return_data')))
            self.assertEqual(video_id[0][0], 1, ' video_id not found')
            self.assertGreaterEqual(video_result[0][0], len(result.get('return_data')), ' query fail')
            self.assertGreaterEqual(len(result.get('return_data')), 0, ' query fail')
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testsearch_realtime_video_error_int(self):
        self.log.logger.info("")
        try: 
             #视频文件实时结果查询，传数字的c_id           
            result_tmp = self.face_video_retrieval_class.search_realtime_video(c_id=self.c_id)
            result = result_tmp            
            self.assertEqual((result.get('errorinfo')), -5, ' query fail')
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败")
    def testsearch_realtime_video_error_96325874110(self):
        self.log.logger.info("")
        try: 
             #视频文件实时结果查询，传无效的c_id           
            result_tmp = self.face_video_retrieval_class.search_realtime_video(c_id=[96325874110])
            #print(result_tmp)
            result = result_tmp            
            video = DataBase.DataBase()
            video_id = video.fetch_all('SELECT count(*) FROM `frs_channel` where type=1 and c_id='+str(96325874110))
            video_result = video.fetch_all('select count(*) from `frs_result` where c_id='+str(96325874110))
            video.close()
            self.assertEqual(video_id[0][0], 0, ' video_id not found')
            self.assertEqual(video_result[0][0], len(result.get('return_data')), ' query fail')
            self.assertEqual(len(result.get('return_data')), 0, ' query fail')
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testvideo_realtime_grabface_error_int(self):
        #视频文件 实时抓拍查询 int的c_id
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.video_realtime_grabface(c_id=self.c_id)
            #print(result_tmp)
            result = result_tmp
            self.assertGreaterEqual(result.get('errorinfo'), -5, ' query fail')
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testvideo_realtime_grabface_right_cid(self):
        #视频文件 实时抓拍查询 正确的c_id
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.video_realtime_grabface(c_id=[self.c_id])
            #print(result_tmp)
            result = result_tmp
            video = DataBase.DataBase()
            video_id = video.fetch_all('SELECT count(*) FROM `frs_channel` where type=1 and c_id='+str(self.c_id))
            video_result = video.fetch_all('select count(*) from `frs_grab_condition` where c_id='+str(self.c_id))
            video.close()
            self.assertEqual(video_id[0][0], 1, ' video_id not found')
            self.assertGreaterEqual(video_result[0][0], len(result.get('return_data')), ' query fail')
            self.assertGreaterEqual(len(result.get('return_data')), 0, ' query fail')
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败")
    def testvideo_realtime_grabface_error_789654123147(self):
        #视频文件 实时抓拍查询 无效的c_id
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.video_realtime_grabface(c_id=[789654123147])
            #print(result_tmp)
            result = result_tmp
            video = DataBase.DataBase()
            video_id = video.fetch_all('SELECT count(*) FROM `frs_channel` where type=1 and c_id='+str(789654123147))
            video_result = video.fetch_all('select count(*) from `frs_grab_condition` where c_id='+str(789654123147))
            video.close()
            self.assertEqual(video_id[0][0], 0, ' video_id not found')
            self.assertEqual(video_result[0][0], len(result.get('return_data')), ' query fail')
            self.assertEqual(len(result.get('return_data')), 0, ' query fail')
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 

    def testoffline_grab_video_right_cid(self):
        #视频文件 离线抓拍查询  正确的c_id
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_grab_video(c_id=[self.c_id])
            result = result_tmp
            video = DataBase.DataBase()
            video_id = video.fetch_all('SELECT count(*) FROM `frs_channel` where type=1 and c_id='+str(self.c_id))
            video_result = video.fetch_all('select count(*) from `frs_grab_condition` where c_id='+str(self.c_id))
            video.close()
            self.assertEqual(video_id[0][0], 1, ' video_id not found')
            self.assertGreaterEqual(video_result[0][0], len(result.get('return_data')), ' query fail') 
            self.assertGreater(len(result.get('return_data')), 0, ' query fail')   
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testoffline_grab_video_error_789456123258(self):
        #视频文件 离线抓拍查询  无效的c_id
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_grab_video(c_id=[789456123258])
            result = result_tmp
            video = DataBase.DataBase()
            video_id = video.fetch_all('SELECT count(*) FROM `frs_channel` where type=1 and c_id='+str(789456123258))
            video_result = video.fetch_all('select count(*) from `frs_grab_condition` where c_id='+str(789456123258))
            video.close()
            self.assertEqual(video_id[0][0], 0, ' video_id not found')
            self.assertEqual(video_result[0][0], len(result.get('return_data')), ' query fail') 
            self.assertEqual(len(result.get('return_data')), 0, ' query fail')   
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testoffline_grab_video_error_int(self):
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_grab_video(c_id=self.c_id)
            result = result_tmp
            self.assertEqual(result.get('errorinfo'), -5, ' query fail')
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testoffline_video_search_right_cid_right_threshold_no_name(self):
        #视频文件 离线结果查询  正确的c_id
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_video_search(c_id=[self.c_id],similarity=[0,1])
            result = result_tmp      
            video = DataBase.DataBase()           
            video_result = video.fetch_all('select count(*) from `frs_result` where c_id='+str(self.c_id))
            video.close()           
            self.assertGreaterEqual(video_result[0][0], len(result.get('return_data')), ' query fail') 
            self.assertGreaterEqual(len(result.get('return_data')), 0, ' query fail') 
            self.assertGreaterEqual(result.get('total'), 0, ' query fail') 
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testoffline_video_search_invalid_cid_right_threshold_no_name(self):
        #视频文件 离线结果查询  无效的c_id
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_video_search(c_id=[789456123258],similarity=[0,1])
            result = result_tmp  
            #print(result)    
            video = DataBase.DataBase()           
            video_result = video.fetch_all('select count(*) from `frs_result` where c_id='+str(789456123258))
            video.close()           
            self.assertEqual(video_result[0][0], len(result.get('return_data')), ' query fail') 
            self.assertEqual(len(result.get('return_data')), 0, ' query fail') 
            self.assertEqual(result.get('total'), 0, ' query fail')           
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败")
    def testoffline_video_search_string_cid_right_threshold_no_name(self):
        #视频文件 离线结果查询  string的c_id
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_video_search(c_id=['c_ids'],similarity=[0,1])
            result = result_tmp  
            #print(result)             
            self.assertEqual(result.get('errorinfo'), -5, ' query fail') 
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 

    def testoffline_video_search_error(self):
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_video_search(c_id=[9999],similarity=[0,1])
            result = result_tmp
        except Exception as ex:
            self.fail(str(9999)+' the testoffline_video_search_error response is not a standard json format!')
        video = DataBase.DataBase()
        video_id = video.fetch_all('SELECT count(*) FROM `frs_channel` where type=1 and c_id='+str(9999))
        video_result = video.fetch_all('select count(*) from `frs_result` where c_id='+str(9999))
        video.close()
        self.assertEqual(video_id[0][0], 0, ' facevideo_add fail')
        self.assertGreaterEqual(video_result[0][0], len(result.get('return_data')), ' query fail')  

    def testoffline_video_search_right_cid_invalid_threshold_no_name(self):
        #视频文件 离线结果查询  无效的threshold
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_video_search(c_id=[self.c_id],similarity=[1,0.9])
            result = result_tmp      
            video = DataBase.DataBase()           
            video_result = video.fetch_all('select count(*) from `frs_result` where c_id='+str(self.c_id))
            video.close()           
            self.assertGreaterEqual(video_result[0][0], len(result.get('return_data')), ' query fail') 
            self.assertEqual(len(result.get('return_data')), 0, ' query fail') 
            self.assertEqual(result.get('total'), 0, ' query fail') 
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testoffline_video_search_right_cid_string_threshold_no_name(self):
        #视频文件 离线结果查询  string的threshold
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_video_search(c_id=['c_ids'],similarity=['cc',1])
            result = result_tmp  
            #print(result)             
            self.assertEqual(result.get('errorinfo'), -5, ' query fail') 
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testoffline_video_search_right_cid_right_threshold_right_name(self):
        #视频文件 离线结果查询  正确的名称
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_video_search(c_id=[self.c_id],similarity=[0,1],p_name='video_test')
            result = result_tmp  
            #print(result)    
            video = DataBase.DataBase()           
            video_result = video.fetch_all('select count(*) from `frs_result` where c_id='+str(self.c_id))
            video.close()           
            self.assertGreaterEqual(video_result[0][0], len(result.get('return_data')), ' query fail') 
            self.assertGreaterEqual(len(result.get('return_data')), 0, ' query fail') 
            self.assertGreaterEqual(result.get('total'), 0, ' query fail')
            return_data =  result.get('return_data')
            for data in return_data:
                self.assertEqual(data.get('p_name'),'video_test',' query fail')
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
    def testoffline_video_search_right_cid_right_threshold_invalid_name(self):
        #视频文件 离线结果查询  无效的name
        self.log.logger.info("")
        try:
            result_tmp = self.face_video_retrieval_class.offline_video_search(c_id=[self.c_id],similarity=[0,1],p_name='fgduiguib')
            result = result_tmp       
            self.assertEqual(len(result.get('return_data')), 0, ' query fail') 
            self.assertEqual(result.get('total'), 0, ' query fail') 
        except DMExceptions.GetHttpResponseError as ex:
            self.fail("get response from server error!")
        except DMExceptions.ResposeToJsonException as ex:
            self.fail("the response is not a standard json format!")  
        except DMExceptions.DBInitException as ex:
            self.fail("connect to database fail!")
        except DMExceptions.DBQueryException as ex:
            self.fail("query database fail!")   
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoFileDetect初始化失败！")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift连接失败") 
if __name__ == "__main__":
    unittest.main(exit=False)
    
    #r_suite = unittest.TestSuite()
    #r_suite.addTest(FaceVideoRetrievalTestCase('testoffline_video_search_error'))
    
    #unittest.TextTestRunner().run(r_suite)
    
    