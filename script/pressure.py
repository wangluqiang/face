#coding=utf-8
import unittest
import sys
import os
import time
import random
sys.path.append('..\public')
import DataBase
import FaceDB
import SearchGrabPic
import RequestVideoDetect
import threading
import LogConfig
import multiprocessing
Mylog=LogConfig.Logger()
file_names=os.listdir(os.path.abspath(r'..\picture')) 
def thread_run(ip,port,c_id,mintime,maxtime):
		Req=RequestVideoDetect.RequestVideoDetect(ip,port)
		Req.connect()
		while 1:
			thread_name=threading.currentThread().getName()
			picname=random.choice(file_names)
			Mylog.logger.info('%s send to %s_%s picname:%s channelID:%s'%(thread_name,ip,port,picname,c_id))
			msg=Req.grab_and_match(pic_name=picname,channel_id=c_id,facedb_id=[1])
			Mylog.logger.info('%s recived:%s'%(thread_name,msg))
			time.sleep(random.randint(mintime,maxtime)/1000)
	
def thread_start (ip,port,thread_num,mintime=None,maxtime=None):
		Mylog.logger.info('Pressure_test Begin,the thread_num is %s,thrift server is %s_%s'%(thread_num,ip,port))
		if mintime is None:
			mintime=100
		if maxtime is None:
			maxtime=1000
		t=[]
		for n in range(thread_num):
			t.append(threading.Thread(target=thread_run,name='线程'+str(n+1),args=(ip,port,n+1,mintime,maxtime)))
		for i in t:
			i.start()
		for i in t:
			i.join()
			
if __name__=='__main__':
	#thread_start('192.168.29.212','11000',2)
	p1=multiprocessing.Process(target=thread_start,args=('192.168.29.155','9092',2))
	#p2=multiprocessing.Process(target=thread_start,args=('192.168.29.212','12000',2))
	p1.start()
	#p2.start()