#coding=utf-8
import os,sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\script")
sys.path.append(cur_path+'\\public')
import FaceDB
import FaceDevice
import FaceMatch
import FacePre

def set_env_5000():
	#添加人脸库
	server_ip = "192.168.29.156"
	server_port = 5000
	db_server_ip = "192.168.29.156"
	db_server_port = 3306
	db_name = 'opzoonfrs_1120_5000_9090'
	db_user = "opzoon"
	db_passwd = "123.com"
	fd = FaceDB.FaceDB(ip=server_ip, port=server_port, db_ip=db_server_ip, db_port=db_server_port, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
	fd.facedb_add(name="face", threshold=0.4, remark="性能测试使用的人脸库")
	#添加比对服务
	fm = FaceMatch.FaceMatch(ip=server_ip, port=server_port, db_ip=db_server_ip, db_port=db_server_port, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
	fm.facematch_add(m_name='match_147', m_ip='192.168.29.147', m_port=14700, face_max=10, min_face_pixel=100,max_face_pixel=100)
	fm.facematch_add(m_name='match_148', m_ip='192.168.29.148', m_port=14800, face_max=10, min_face_pixel=100,max_face_pixel=100)
	#添加预处理
	fp = FacePre.FacePre(ip=server_ip, port=server_port, db_ip=db_server_ip, db_port=db_server_port, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
	fp.facepre_add(p_name='pre_147', p_ip='192.168.29.147',p_port=14701,m_name='match_147',frame_interval=200)
	fp.facepre_add(p_name='pre_148', p_ip='192.168.29.148',p_port=14801,m_name='match_148',frame_interval=200)
	#添加设备
	device = FaceDevice.FaceDevice(ip=server_ip, port=server_port, db_ip=db_server_ip, db_port=db_server_port, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
	channel = device.channel_add(0,'test0',fd_name_list=['face'])
	device.facedevice_add(device_name='test_5faces',device_ip='192.168.31.190',device_port=80,url_user='admin',url_pwd='12345',device_type=0,channel=[channel], \
						  p_name='pre_148')
	device.facedevice_add(device_name='test_1face',device_ip='192.168.30.227',device_port=80,url_user='admin',url_pwd='opzoon12345',device_type=0,channel=[channel], \
						  p_name='pre_147')

def set_env_6000():
	#添加人脸库
	server_ip = "192.168.29.156"
	server_port = 6000
	db_server_ip = "192.168.29.156"
	db_server_port = 3306
	db_name = 'opzoonfrs_1120_6000_9095'
	db_user = "opzoon"
	db_passwd = "123.com"
	fd = FaceDB.FaceDB(ip=server_ip, port=server_port, db_ip=db_server_ip, db_port=db_server_port, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
	fd.facedb_add(name="face", threshold=0.4, remark="性能测试使用的人脸库")
	#添加比对服务
	fm = FaceMatch.FaceMatch(ip=server_ip, port=server_port, db_ip=db_server_ip, db_port=db_server_port, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
	fm.facematch_add(m_name='match_150', m_ip='192.168.29.150', m_port=15000, face_max=10, min_face_pixel=100,max_face_pixel=100)
	#添加预处理
	fp = FacePre.FacePre(ip=server_ip, port=server_port, db_ip=db_server_ip, db_port=db_server_port, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
	fp.facepre_add(p_name='pre_155', p_ip='192.168.29.155',p_port=15501,m_name='match_150',frame_interval=200)
	#添加设备
	device = FaceDevice.FaceDevice(ip=server_ip, port=server_port, db_ip=db_server_ip, db_port=db_server_port, db_name=db_name, db_user=db_user, db_passwd=db_passwd)
	channel = device.channel_add(0,'test0',fd_name_list=['face'])
	device.facedevice_add(device_name='test_5faces',device_ip='192.168.31.190',device_port=80,url_user='admin',url_pwd='12345',device_type=0,channel=[channel], \
						  p_name='pre_155')
	device.facedevice_add(device_name='test_1face',device_ip='192.168.30.227',device_port=80,url_user='admin',url_pwd='opzoon12345',device_type=0,channel=[channel], \
						  p_name='pre_155')

if __name__ == "__main__":
    set_env_5000()
    set_env_6000()
