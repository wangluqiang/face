#coding=utf-8
import unittest
import sys,os,time
import HTMLTestRunner
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\script")
import init_test_env
import facedb_test
import request_video_detect_test
import face_pic_retrieval_test
import facedevice_test
import facematch_test
import faceperson_test
import facepre_test
import searchpic_test
import requestgrabface_test
import facevideoretrieval_test
import facevideo_test
import facesearchgrabpic_test


init_test_env.add_init_facedb()
init_test_env.add_init_match()
time.sleep(10)
init_test_env.add_init_person()
init_test_env.add_init_preprocess()
time.sleep(10)
init_test_env.add_init_device()
init_test_env.add_init_video()




'''
test.addTest(unittest.makeSuite(facedb_test.FaceDBTestCase))
test.addTest(unittest.makeSuite(request_video_detect_test.RequestVideoDetectTestCase))
test.addTest(unittest.makeSuite(face_pic_retrieval_test.FacePicRetrievalTestCase))
test.addTest(unittest.makeSuite(facedevice_test.FaceDeviceTestCase))
test.addTest(unittest.makeSuite(facematch_test.FaceMatchTestCase))
test.addTest(unittest.makeSuite(faceperson_test.FacePersonTestCase))
test.addTest(unittest.makeSuite(facepre_test.FacePreTestCase))
test.addTest(unittest.makeSuite(searchpic_test.SearchPicTestCase))
test.addTest(unittest.makeSuite(requestgrabface_test.RequestGrabfaceTestCase))
test.addTest(unittest.makeSuite(facevideoretrieval_test.FaceVideoRetrievalTestCase))
test.addTest(unittest.makeSuite(facevideo_test.FaceVideoTestCase))
test.addTest(unittest.makeSuite(facesearchgrabpic_test.SearchGrabPicTestCase))
'''


#unittest.TextTestRunner().run(test)

test = unittest.TestSuite()
discover = unittest.defaultTestLoader.discover(start_dir=cur_path+"\\script", pattern="*_test.py", top_level_dir=None)
for s in discover:
    for c in s:
        test.addTests(c)

cur_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())
file_name = cur_path+"//result/result_"+str(cur_time)+".html"
fp = open(file_name,"wb")
runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title="人脸识别系统动态监控版本自动化测试结果",description="")
runner.run(test)

