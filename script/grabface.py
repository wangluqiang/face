#coding=utf-8
import unittest
import random
import os,time
import sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import datetime
import RequestGrabface
import LogConfig

class RequestGrabface_Test(unittest.TestCase):
    def setUp(self):
        self.requestgrabface = RequestGrabface.RequestGrabface()
        self.log = LogConfig.Logger()
    def tearDown(self):
        pass
  
    def test_requestgrabface(self):
        while 1:
            time_change = datetime.timedelta(seconds=random.randint(3600,7200))
            now_time=datetime.datetime.now()
            s_time=now_time-time_change
            e_time=now_time
            start_time='%s-%s-%s %s:%s:%s'%(s_time.year,s_time.month,s_time.day,s_time.hour,s_time.minute,s_time.second) 
            end_time='%s-%s-%s %s:%s:%s'%(e_time.year,e_time.month,e_time.day,e_time.hour,e_time.minute,e_time.second)
            channel_name = []
            channel = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
            for i in range(1,random.randint(2,15)):
                cho=random.choice(channel)
                if cho not in channel_name:
                    channel_name.append(cho)
            #before_time=time.time()
            result = self.requestgrabface.list_grabface_request(start_time, end_time,channel_name)
            #after_time=time.time()
            #longs='%.0f'%((after_time-before_time)*1000)
            self.log.logger.info('开始时间:'+start_time+',结束时间:'+end_time+'设备通道:'+str(channel_name))
            print(result)
            time.sleep(random.randint(4,4))

if __name__ == "__main__":
    unittest.main()