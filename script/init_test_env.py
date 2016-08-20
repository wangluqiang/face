#coding=utf-8
import sys
import os
import time
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import FaceDB
import FaceDevice
import FaceMatch
import FacePerson
import FacePre
import Config
import DataBase
import FaceVideo
import RequestVideoFileDetect
def add_init_facedb():
	fd = FaceDB.FaceDB()
	r = fd.facedb_add(name="facedb_test", threshold=0.8, remark="用户自动化测试的人脸库")
	return r["errorinfo"]

def add_init_person():
	fp = FacePerson.FacePerson()
	for num in range(15):
		person = {}
		person['p_name'] = "person_test_1_"+str(num+1)
		person['reg_type'] = 1
		person['grab_id'] = 0
		person['sex'] = 1
		person['cardId'] = '1234'+str(num+1)
		person['remark'] = '用于接口自动化测试的图片'
		person['pic_name'] = '范冰冰.jpg'
		person['fd_name'] = 'facedb_test'
		fp.faceperson_add(**person)
	fp = FacePerson.FacePerson() 
	person = {}
	person['p_name'] = 'video_test'
	person['reg_type'] = 1
	person['grab_id'] = 0
	person['sex'] = 1
	person['cardId'] = 'video_test'
	person['remark'] = '用于接口自动化测试的图片'
	person['pic_name'] = '50008.jpg'
	person['fd_name'] = 'facedb_test'
	fp.faceperson_add(**person)

def add_init_match():
	cfg = Config.Config()
	m_info = cfg.thrift_match_info()
	match = FaceMatch.FaceMatch()
	data = {}
	data["m_name"] = "match_test"
	data["m_ip"] = m_info["ip"]
	data["m_port"] = m_info["port"]
	data["face_max"] = 10
	data["client_max"] = 10
	data["min_face_pixel"] = 100
	data["max_face_pixel"] = 100
	data["remark"] = "用于自动化测试的比对服务"
	r = match.facematch_add(**data)
	return r["errorinfo"]
	
def add_init_preprocess(m_id=None):
	match_id = DataBase.DataBase()
	ids = match_id.fetch_all("SELECT m_id FROM `frs_match` where m_name='match_test'")
	match_id.close()
	m_id = ids[0][0]
	cfg = Config.Config()
	pre_info = cfg.thrift_preprocess_info()
	pre = FacePre.FacePre()
	r = pre.facepre_add(p_name="preprocess_test", p_ip=pre_info["ip"], p_port=pre_info["port"], m_id=m_id, frame_interval=500, \
						remark="用于自动化测试的预处理")
	return r["errorinfo"]
	
def add_init_device(fd_id=None,p_id=None):
	cfg = Config.Config()
	camera_info = cfg.url_device_info()
	invalid_camera_info = cfg.url_invalid_device_info()
	facedv = FaceDevice.FaceDevice()
	if fd_id == None:
		face_id = DataBase.DataBase()
		ids = face_id.fetch_all("SELECT fd_id FROM `frs_facedb` where fd_name='facedb_test'")
		face_id.close()
		fd_id = ids[0][0]
	if p_id == None:
		pre_id = DataBase.DataBase()
		ids = pre_id.fetch_all("SELECT p_id FROM `frs_collection` where p_name='preprocess_test'")
		pre_id.close()
		p_id = ids[0][0]
	#添加有效的摄像头
	for each_device in camera_info:
		c_r = facedv.channel_add(c_no=0, c_name="channel_test", fd_id_list=[fd_id])
		r = facedv.facedevice_add(device_name="device_test", device_ip=each_device["ip"], device_port=int(each_device["port"]), \
						  url_user=each_device["user"], url_pwd=each_device["passwd"], device_type=0, p_id=p_id, \
						  channel=[c_r], remark="用于自动化测试的设备")
		print(r)
	#添加无效的摄像头
	c_r = facedv.channel_add(c_no=0, c_name="invalid_channel_test", fd_id_list=[fd_id])
	r = facedv.facedevice_add(device_name="invalid_device_test", device_ip=invalid_camera_info[0]["ip"], device_port=int(invalid_camera_info[0]["port"]), \
						  url_user=invalid_camera_info[0]["user"], url_pwd=invalid_camera_info[0]["passwd"], device_type=0, p_id=p_id, \
						  channel=[c_r], remark="用于自动化测试的设备，该设备是不存在的摄像头")
	print(r)

def add_init_video(): 
	#添加视频文件test_video.avi
	channel = DataBase.DataBase()
	channel_id = channel.fetch_all("select c_id from `frs_channel` where c_name = 'test_video.avi'")
	channel.close()
	if len(channel_id)==0:
		facev=FaceVideo.FaceVideo()
		video_tmp = facev.facevideo_add('test_video.avi')
		c_id =video_tmp.get('video_id')
	else: 
		c_id = channel_id[0][0] 
if __name__ == '__main__':
	#add_init_facedb()
	#add_init_match()
	#time.sleep(10)
	#add_init_person()
	#add_init_preprocess()
	#time.sleep(5)
	add_init_device()
	#add_init_video()