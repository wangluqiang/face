#coding=utf-8
import requests
import json	
import base64
import os,time
import sys,shutil
import threading
from DataBase import DataBase
import Config
import DMExceptions
from Base import RESTAPIBase

class FacePerson(RESTAPIBase):
	LL=[]
	'''
	 封装的人员信息管理类，该类主要用于人员信息的增、删、改、查
	'''
	#加载配置IP及path
	def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
		if path == None:
			cfg = Config.Config()
			s_path = cfg.url_path_info()["person"]
		else:
			s_path = path
		RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)

	#读取照片
	def	pic_read(self,filename): 
		pic_file_path = os.path.split(os.path.realpath(__file__))[0]+('\\..\\picture')+'\\'+filename
		try:
			file_obj =	open(pic_file_path,	'rb')
			pic_buffer = file_obj.read()
		except Exception as ex:
			raise DMExceptions.ReadPicException(str(ex))
		finally:
			file_obj.close()
		return pic_buffer

	def pic_read1(self,filename):
		try:
			file_obj=open(filename,'rb')
			pic_buffer=file_obj.read()
		except Exception as ex:
			raise DMExceptions.ReadPicException(str(ex))
		finally:
			file_obj.close()
		return pic_buffer
	
	#添加人员信息
	def	faceperson_add(self, fd_name=None, fd_id=None, pic_name=None, **kwargs):
		'''
		功能：添加人员信息
		输入：
		pic_name：照片名称
		fd_name：人脸库名称
		fd_id：人脸库ID
		kwargs包含：
			p_name:添加人员的名称
			reg_type：注册类型（1：正常注册， 2：抓拍图片注册）
			grab_id：抓拍人员ID（reg_type为1时，grab_id置为0， reg_type为2时，	grab_id为该抓拍人员的ID）
			sex：性别（0为男，1为女）
			cardId：卡号
			remark：备注
			pursuit_no:追逃编号
			census_address:户籍地址
			family_address:家庭住址
			birth_date：出生日期，如：1990-01-01
		输出：字典格式：
		{"errorinfo": X}，X大于0表示成功，且X为p_id
			
		'''
		p_dict = {}
		p_dict.update(kwargs)
		if pic_name:
			pic	= self.pic_read(pic_name)
			p_dict['reg_pic'] =	base64.b64encode(pic).decode()
		if fd_name:
			persondb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			sql_query_id = "select fd_id from frs_facedb where fd_name='"+fd_name+"'"
			query_result_id	= persondb.fetch_all(sql_query_id)
			persondb.close()
			fd_id =	query_result_id[0][0]			
			p_dict['fd_id']	= fd_id
		elif fd_id:
			p_dict['fd_id']	= fd_id
		else:
			pass
		try:
			add_result = requests.post(self.url,data=json.dumps(p_dict),headers=self.headers)
			add_result.raise_for_status()
		except Exception as	ex:
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			add_result.json()
		except Exception as	ex:
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(add_result.json())

	#删除人员信息
	def	faceperson_delete(self,	cardId=None, p_id=None):
		'''
		功能：删除人员信息
		输入：
		cardId：删除人员的卡号
		p_id:删除人员的P_id
		输出：字典格式:{"errorinfo": 0}表示删除成功
		'''
		if cardId:
			#根据卡号名称查询人员id
			persondb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			sql_query_id = "select p_id	from frs_person	where cardId='"+cardId+"'"
			query_result_id	= persondb.fetch_all(sql_query_id)
			persondb.close()
			p_id = query_result_id[0][0]
			faceperson_delete_data = {"p_id":p_id}
		elif p_id:
			faceperson_delete_data = {"p_id":p_id}
		else:
			faceperson_delete_data = {}
		try:
			delete_result =	requests.delete(self.url, data=json.dumps(faceperson_delete_data), headers=self.headers)
			delete_result.raise_for_status()
		except Exception as	ex:
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			delete_result.json()
		except Exception as	ex:
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(delete_result.json())

	#修改人员信息
	def	faceperson_modify(self,	cardId_base=None, p_id=None, pic_name=None, **kwargs):
		'''
		功能：修改人员信息
		输入：
		cardId_base：需要修改的人员卡号
		p_id:需修改人员的p_id
		pic_name:人员图片
		kwargs:需要修改的内容:
			p_name:添加人员的名称
			sex：性别（0为男，1为女）
			fd_id:人脸库ID
			fd_name:人脸库名称；与人脸库ID只传其中一个
			cardId：卡号
			remark：备注
			pursuit_no:追逃编号
			census_address:户籍地址
			family_address:家庭住址
			birth_date：出生日期，如：1990-01-01
			异常内容如果值为None，则默认为不修改，也就是说参数值为未修改前的值。（目前接口做的是，如果修改，需要传输所有的有值参数）
		输出：字典格式：{"errorinfo": 0} 表示修改成功
		'''

		if cardId_base:
		#根据卡号名称查询人员id/name/fd_id/sex
			persondb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			#返回项目依次是 p_id,p_name,birth_date,cardId,pursuit_no,census_address,family_address,fd_id,sex,remark
			sql_query = "select p_id,p_name,birth_date,cardId,pursuit_no,census_address,family_address,fd_id,sex,remark from frs_person	where cardId='"+cardId_base+"'"
			query_result = persondb.fetch_all(sql_query)
			persondb.close()
			p_id = query_result[0][0]
			faceperson_modify_data = {"p_id":p_id}
		elif p_id:
			faceperson_modify_data={'p_id':p_id}
			persondb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			#返回项目依次是 p_id,p_name,birth_date,cardId,pursuit_no,census_address,family_address,fd_id,sex,show_pic,feature,reg_pic,remark
			sql_query = "select p_id,p_name,birth_date,cardId,pursuit_no,census_address,family_address,fd_id,sex,remark from frs_person where p_id='"+str(p_id)+"'"
			query_result = persondb.fetch_all(sql_query)
			persondb.close()
		else:
			faceperson_modify_data = {}
		if pic_name:
			pic	= self.pic_read(pic_name)
			faceperson_modify_data['reg_pic'] =	base64.b64encode(pic).decode()
		faceperson_modify_data.update(kwargs)
		if "p_name" in kwargs:
			if kwargs['p_name'] == None:
				faceperson_modify_data["p_name"] = query_result[0][1]
		if "remark"	in kwargs:
			if kwargs["remark"] == None:
				faceperson_modify_data["remark"] = query_result[0][9]
		if "sex" in	kwargs:
			if kwargs["sex"] == None:
				faceperson_modify_data["sex"] =	query_result[0][8]
		if "fd_name" in kwargs:
			del faceperson_modify_data["fd_name"]
			if kwargs["fd_name"]:
				persondb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
				sql_query_id = "select fd_id from frs_facedb where fd_name='"+kwargs["fd_name"]+"'"
				query_result_id	= persondb.fetch_all(sql_query_id)
				persondb.close()
				fd_id =	query_result_id[0][0]
				faceperson_modify_data['fd_id']	= fd_id
			else:
				faceperson_modify_data["fd_id"] = query_result[0][7]
		elif "fd_id" in kwargs:
			if kwargs["fd_id"]:
				faceperson_modify_data['fd_id']	= kwargs["fd_id"]
			else:
				faceperson_modify_data["fd_id"] = query_result[0][7]
		else:
			pass
		if "cardId"	in kwargs:
			if kwargs["cardId"] == None:
				faceperson_modify_data["cardId"] = query_result[0][3]
		if "pursuit_no" in kwargs:
			if  kwargs['pursuit_no'] == None:
				faceperson_modify_data['pursuit_no'] = query_result[0][4]
		if "census_address" in kwargs:
			if kwargs['census_address'] == None:
				faceperson_modify_data['census_address'] = query_result[0][5]
		if "family_address" in kwargs:
			if kwargs['family_address'] == None:
				faceperson_modify_data['family_address'] = query_result[0][6]
		if "birth_date" in kwargs:
			if kwargs['birth_date'] == None:
				faceperson_modify_data['birth_date'] = query_result[0][2]
		try:
			modify_result =	requests.put(self.url, data=json.dumps(faceperson_modify_data), headers=self.headers)
			modify_result.raise_for_status()
		except Exception as	ex:
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			modify_result.json()
		except Exception as	ex:
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(modify_result.json())

	#查询人员信息
	def	faceperson_query(self,**kwargs):
		'''
		功能：查询人员信息(只传url报错)
		输入：kwargs:
			p_name：人员姓名
			sex：人员性别(0男，1女)
			facedb：人脸库id
			amount：返回数量
		输出：列表格式，人员详细信息
		'''
		if "p_name"	not	in kwargs and "sex"	not	in kwargs and "facedb" not in kwargs and "amount" not in kwargs:
			url_query=self.url
		else:
			url_query=self.url+'?'
			if "p_name"	in kwargs:
				url_query=url_query+'&person_name='+kwargs['p_name']
			if "sex" in	kwargs:
				url_query=url_query+'&sex='+kwargs['sex']
			if "facedb"	in kwargs:
				url_query=url_query+'&facedb='+kwargs['facedb']
			if "amount"	in kwargs:
				url_query=url_query+'&amount='+kwargs['amount']
		try:
			query_result =requests.get(url_query)
			query_result.raise_for_status()
		except Exception as	ex:
			raise DMExceptions.GetHttpResponseError(str(ex))
		try:
			query_result.json()
		except Exception as	ex:
			raise DMExceptions.ResposeToJsonException(str(ex))
		return json.loads(query_result.json())

	########以下函数为批量注册相关###########################################################
	#获取照片绝对地址列表
	def	get_L(self,path):
		L=[]
		for	eachfile in	os.listdir(path):
			if os.path.splitext(eachfile)[1] in	['.jpg','.JPG','.png','.PNG','.bmp','.BMP']:
				eachfile=os.path.join(path,eachfile)
				L.append(eachfile)
		return L  
	def	get_D(self,thread_num,path):
		L=self.get_L(path)
		#print(L)
		group_file=int(len(L)/thread_num)	 
		D={}
		for	i in range(thread_num):
			D[i]=[]
		count=0
		for	i in range(len(L)):
			if i==0:
				D[0].append(L[0])
				continue
			if i%group_file==0:
				count=count+1
				if count==thread_num:
					count-=1
					D[count].append(L[i])
				else:
					D[count].append(L[i])
			else:
				D[count].append(L[i])
		return D
		  
	def	regist(self,url,L,Failed_path,fd_id):
		p_dict={} 
		reg_type=1
		sex=1
		fd_id=fd_id
		grabid=0
		headers= {'Content-Type':'application/json', 'charset':'UTF-8'}
		for	pic_file in	L:	  
			pic=self.pic_read1(pic_file)
			p_dict['p_name'] = os.path.splitext(os.path.split(pic_file)[1])[0]
			p_dict['reg_type'] = reg_type
			p_dict['grab_id'] =	grabid
			p_dict['sex'] =	sex
			p_dict['cardId'] =os.path.splitext(os.path.split(pic_file)[1])[0]
			p_dict['remark'] ='test'
			p_dict['reg_pic'] =	base64.b64encode(pic).decode()
			p_dict['fd_id']= fd_id
			#print(url)
			r=requests.post(url,data=json.dumps(p_dict),headers=headers)
			result=json.loads(r.json())['errorinfo']
			FacePerson.LL.append(None)
			#print(result)
			if result<0:	
				shutil.copy(pic_file,Failed_path)
	#注册进度条
	def	progress(self,path):
		L=self.get_L(path)
		print('---------------------注册开始---------------------')
		while len(FacePerson.LL)<len(L):
			Count=int(int(len(FacePerson.LL)/len(L)*100)/2)
			str1='#'*Count
			str2=str(int(len(FacePerson.LL)/len(L)*100))+'%'
			print ('\r%s %s' % (str1,str2),end='')
		str1='#'*50
		str2='100%'
		print('\r%s	%s'%(str1,str2),end='')	
		   
	def	faceperson_batch_add(self,path,thread_num,url=None,**kwargs):
		'''
		path:本地文件夹地址
		thread_num：注册线程数量
		fd_id：注册的人脸库ID
		fd_name:注册的人脸库名称
		'''
		if url is None:
			url=self.url
		if 'fd_name' in kwargs:
			database=DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
			SQL="SELECT fd_id FROM `frs_facedb` WHERE fd_name='%s';"%(kwargs['fd_name'])
			fd_id=database.fetch_all(SQL)
			if len(fd_id)==0:
				fd_id=0
			elif len(fd_id)>0:
				fd_id=fd_id[0][0]
		if 'fd_id' in kwargs:
			fd_id=kwargs['fd_id']
		if os.path.isdir(path):
			if len(self.get_L(path))!=0:	
				threading.Thread(target=self.progress,args=(path,)).start()
				Failed_path=os.path.join(path,'FailedPicture')
				if not os.path.exists(Failed_path):
					os.mkdir(Failed_path)
				D=self.get_D(thread_num,path)
				#print(D)
				t=[]
				for	i in range(thread_num):
					tt=threading.Thread(target=self.regist,args=(url,D[i],Failed_path,fd_id))	 
					t.append(tt)
				for	i in t:
					i.start()
				for	i in t:
					i.join()
				return 0
			else:
				print('%s--文件夹内没有图片'%(path))
				return 0
		else:
			print('%s--非文件夹'%(path))
			return 0
			
		
		
		


	
	
if __name__	== "__main__":
	faceperson_test	= FacePerson()
	print(faceperson_test.faceperson_add(p_name='test_zzz',reg_type=1,grab_id=0,sex='0',cardId='9999',pic_name='zzz.jpg',fd_name='facedb_test',remark='test_7894'))
	#p_name,reg_type,grab_id,sex,cardId,pic_name,fd_id,remark=''
	print(faceperson_test.faceperson_query(p_name='test_zzz'))
	print(faceperson_test.faceperson_modify('test_zzz',p_name_x='test_www',fd_id=1,cardId='6666'))
	print(faceperson_test.faceperson_query(p_name='test_www'))
	print(faceperson_test.faceperson_delete('test_www'))
#	faceperson_batch_add(self,path,thread_num,fd_id,url=None)
	#faceperson_test.faceperson_batch_add(r'C:\Users\opzoon\Desktop\Picture\望京改名裁剪\2015_09\眼镜',8,'http://192.168.29.139:5000/v2/persons',fd_name='123')
	#print(faceperson_test.get_D(4,r'C:\Users\opzoon\Desktop\Picture\望京改名裁剪\2015_09\眼镜'))
	#test_data=faceperson_test.faceperson_query(p_name='person_test_1_15')
	#print(test_data)
	#for each in test_data:
	 #	 print(str(each['p_id']).ljust(5),each['p_name'])
 
