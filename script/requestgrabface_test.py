#coding=utf-8
import unittest
import os,time
import sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import datetime
import RequestGrabface
import FacePerson 
import RequestVideoDetect
import DMExceptions
from handle_exception import handle_exception

class RequestGrabfaceTestCase(unittest.TestCase):
    def setUp(self):
        self.faceperson = FacePerson.FacePerson()
        self.requestvideodetect = RequestVideoDetect.RequestVideoDetect()
        self.requestgrabface = RequestGrabface.RequestGrabface()
        self.items = {}

    def tearDown(self):
        self.requestvideodetect.close()

    @handle_exception
    def test_requestmatchface(self):
        #add person
        result_person_add = self.faceperson.faceperson_add(p_name='test2990',reg_type=1,grab_id=0,sex='0',cardId='test2990',pic_name='zzz.jpg',fd_name='facedb_test',remark='test_auto')
        self.assertGreaterEqual(result_person_add["errorinfo"], 0,'add preson failed')
        self.items["person"] = result_person_add
        #match person
        compare = self.requestvideodetect
        compare.connect()
        result_match = compare.grab_and_match(channel_name="channel_test", pic_name="zzz.jpg", max_face_num=5, facedb_name=["facedb_test"])
        compare.close()
        self.assertEqual(result_match, 0, 'match preson failed')
        time.sleep(4)
        #chaxun person
        time_change = datetime.timedelta(seconds=800)
        s_time=datetime.datetime.now()-time_change
        e_time=datetime.datetime.now()+time_change
        start_time='%s-%s-%s %s:%s:%s'%(s_time.year,s_time.month,s_time.day,s_time.hour,s_time.minute,s_time.second)
        end_time='%s-%s-%s %s:%s:%s'%(e_time.year,e_time.month,e_time.day,e_time.hour,e_time.minute,e_time.second)

        result = self.requestgrabface.list_match_request(c_name=['channel_test'],similarity=[0.7,1], condition_flag=1, \
                                                         p_name='test2990', time=[start_time, end_time], offset=0, limit=1)
        self.assertGreaterEqual(result['total'], 1,'find match preson failed')
        self.assertEqual(result['return_data'][0]['p_name'], 'test2990','find match preson failed')

    def test_requestgrabface(self):
        try:
            #add person
            result_person_add = self.faceperson.faceperson_add(p_name='test2990',reg_type=1,grab_id=0,sex='0',cardId='test2990',pic_name='zzz.jpg',fd_name='facedb_test',remark='test_auto')
            self.assertGreaterEqual(result_person_add["errorinfo"], 0,'add preson failed')

            #chaxun person
            time_change = datetime.timedelta(seconds=800)
            s_time=datetime.datetime.now()-time_change
            e_time=datetime.datetime.now()+time_change
            start_time='%s-%s-%s %s:%s:%s'%(s_time.year,s_time.month,s_time.day,s_time.hour,s_time.minute,s_time.second)
            end_time='%s-%s-%s %s:%s:%s'%(e_time.year,e_time.month,e_time.day,e_time.hour,e_time.minute,e_time.second)
            result_before = self.requestgrabface.list_grabface_request(start_time, end_time,['channel_test'])
            
            #match person
            compare = self.requestvideodetect
            compare.connect()
            result_match = compare.grab_and_match(channel_name="channel_test", pic_name="wujingjing.jpg", max_face_num=5, facedb_name=["facedb_test"])
            compare.close()  
            self.assertEqual(result_match, 0, 'match preson failed')
            time.sleep(4)
            
            #chaxun person
            s_time=datetime.datetime.now()-time_change
            end_time='%s-%s-%s %s:%s:%s'%(e_time.year,e_time.month,e_time.day,e_time.hour,e_time.minute,e_time.second)
            result_after = self.requestgrabface.list_grabface_request(start_time, end_time,['channel_test'])
            self.assertGreater(len(result_after['return_data']), len(result_before['return_data']), 'match or find preson failed')

        except DMExceptions.GetHttpResponseError as ex:
            self.fail("receive http fail")
        except DMExceptions.ResposeToJsonException as ex:           
            self.fail("receive http json error")
        except DMExceptions.RequestVideoDetectInitException as ex:
            self.fail("RequestVideoDetect init fail")
        except DMExceptions.ConnectException as ex:
            self.fail("thrift connect fail")
        finally:
            if 'result_person_add' in locals().keys():
                self.faceperson.faceperson_delete('test2990',result_person_add["errorinfo"])



       
if __name__ == "__main__":
    #unittest.main()
    #RequestGrabfaceTestCase().test_requestgrabface()
    #facepre_test.test_facepre_add_name_prezqq_ip_129()
    #facepre_test.test_facepre_modify_name_prewjj_mid_77_interval_24()
    #facepre_test.test_facepre_query_name_prezqq()
    #facepre_test.test_facepre_delete_name_prezqq()
    r_suite = unittest.TestSuite()
    r_suite.addTest(RequestGrabfaceTestCase('test_requestmatchface'))
    unittest.TextTestRunner().run(r_suite)