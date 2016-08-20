#coding=utf8
import json
import logging
import requests
import Config
from DataBase import DataBase
import LogConfig
import DMExceptions
from Base import RESTAPIBase

class FaceVideoRetrieval(RESTAPIBase):
    '''
     封装的视频文件检索类，该类主要用于视频文件检索的实时结果展示，实时抓拍展示，离线结果查询,离线抓拍查询
     对应于管理端的功能为：视频文件检索标签的现场抓拍人像和比对结果；抓拍人脸查询的视频文件人脸查询、视频文件查询
     属性：
     fsearch_server_ip:操作服务器的IP地址
     fsearch_server_port:操作服务器的端口值
     fsearch_path:URL路径
     url:http的完整路径
    '''
    def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        if path == None:
            cfg = Config.Config()
            s_path = cfg.url_path_info()["require"]
        else:
            s_path = path
        RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)

    def search_realtime_video(self,limit=10,c_id=None,c_name=None):
        '''     
        功能：视频文件文件检索-实时结果查询
        输入：
        limit:返回个数
        c_id:视频文件id []（传值显示传入id的实时结果）
        c_name:视频文件名称[]
        输出：字典格式：{"total": 0, "return_data": []} total =0 是写死的
        '''
        if c_id == None and type(c_name) == list:
            c_id = []
            db = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            for name in c_name:
                require_sql = "select c_id from frs_channel where  c_name='"+name+"'"
                result  = db.fetch_all(require_sql)
                if len(result) == 0:
                    print("no video name!")
                else:
                    c_id.append(result[0][0])
            db.close()
        #print(c_id)
        data = {'type': 'search_realtime_video', 'content':{'paging': [{'offset': '0'}, {'limit': str(limit)}], 'condition': [{'c_id':c_id,'operator':'in'}]}}
        #print(data)
        try:
            realtime_video_result = requests.post(self.url,data=json.dumps(data),headers=self.headers) 
            realtime_video_result.raise_for_status()
            self.log.logger.info("视频文件-实时结果查询" + str(data))
        except Exception as ex:
            self.log.logger.warning("视频文件-实时结果查询出现异常，从server接收响应失败！" + str(data))
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            realtime_video_result.json()
        except Exception as ex:
            self.log.logger.warning("视频文件-实时结果查询出现异常，响应消息转换为json格式错误！" + str(data))
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(realtime_video_result.json())

    def video_realtime_grabface(self,limit=10,c_id=None,c_name=None):
        '''     
        功能：视频文件检索-实时抓拍人像查询
        输入：
         c_id:视频文件id []（传值显示传入id的实时抓拍）
         c_name:视频文件名称[]
        输出：字典格式：{"total": 10, "return_data": []} 
        '''
        if c_id == None and type(c_name) == list:
            c_id = []
            db = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            for name in c_name:
                require_sql = "select c_id from frs_channel where  c_name='"+name+"'"
                result  = db.fetch_all(require_sql)
                if len(result) == 0:
                    print("no video name!")
                else:
                    c_id.append(result[0][0])
            db.close()
        #print(c_id)
        try:
            data = {'type': 'grabface', 'content':{'paging': [{'offset': '0'}, {'limit': str(limit)}], 'condition': [{'c_id':c_id,'operator':'in'}]}}
            realtime_grabface_result = requests.post(self.url,data=json.dumps(data),headers=self.headers)
            realtime_grabface_result.raise_for_status()
            self.log.logger.info("视频文件-实时抓拍查询" + str(data))
        except Exception as ex:
            self.log.logger.warning("视频文件-实时抓拍查询出现异常，从server接收响应失败！" + str(data))
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            realtime_grabface_result.json()
        except Exception as ex:
            self.log.logger.warning("视频文件-实时抓拍查询出现异常，响应消息转换为json格式错误！" + str(data))
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(realtime_grabface_result.json())

    def offline_video_search(self,limit=10,c_id=None,c_name=None,**kwargs):
        '''     
        功能：抓拍人脸查询-离线比对结果查询
        输入：c_id:视频文件id []
        kwargs:查询条件:  
                          similarity：相似度范围  列表[0,1]
                          p_name:姓名   字符串''
        输出：字典格式：{"total": 10, "return_data": []}
        '''
        condition =[]
        if c_id!=None and type(c_id) == list:
            condition.append({'c_id':c_id,'operator':'in'})  
        elif c_id == None and type(c_name) == list:
            c_id = []
            db = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            for name in c_name:
                require_sql = "select c_id from frs_channel where  c_name='"+name+"'"
                result  = db.fetch_all(require_sql)
                if len(result) == 0:
                    print("no video name!")
                else:
                    c_id.append(result[0][0])
            db.close()
            condition.append({'c_id':c_id,'operator':'in'})  
            #print(c_id)      
        if 'similarity' in kwargs:
            condition.append({'similarity': kwargs['similarity'],'operator':['>=','<=']})
        if 'p_name' in kwargs:
            if kwargs['p_name']=='':
                condition.append({'p_name': '','operator':['in']})
            else:
                condition.append({'p_name': [kwargs['p_name']],'operator':['in']})
        condition.append({'condition_flag':[0],'operator':'in'})    
        #print(condition)
        try:
            data = {'type': 'search', 'content':{'paging': [{'offset': '0'}, {'limit': limit}], 'condition': condition}}
            offline_video_result = requests.post(self.url,data=json.dumps(data),headers=self.headers)
            offline_video_result.raise_for_status()
            self.log.logger.info("视频文件-离线结果查询" + str(data))
        except Exception as ex:
            self.log.logger.warning("视频文件-离线结果查询出现异常，从server接收响应失败！" + str(data))
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            offline_video_result.json
        except Exception as ex:
            self.log.logger.warning("视频文件-离线结果查询出现异常，响应消息转换为json格式错误！" + str(data))
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(offline_video_result.json())

    def offline_grab_video(self,limit=10,c_id=None,c_name=None): #{'time': ['2014-1-27 12:00:00', '2016-2-2 12:00:00'], 'operator': ['>=', '<=']},
        '''     
        功能：抓拍人脸查询-离线抓拍查询
        输入：   
        limit:返回个数
        c_id:视频文件id[]
        c_name：视频文件名称[]
        
        输出：字典格式：{"total": 10, "return_data": []}
        '''
        if c_id == None and type(c_name) == list:
            c_id = []
            db = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            for name in c_name:
                require_sql = "select c_id from frs_channel where  c_name='"+name+"'"
                result  = db.fetch_all(require_sql)
                if len(result) == 0:
                    print("no video name!")
                else:
                    c_id.append(result[0][0])
            db.close()
        #print(c_id)
        try:
            data = {'type': 'grabface', 'content':{'paging': [{'offset': '0'}, {'limit': limit}], 'condition': [{'c_id': c_id, 'operator': 'in'}]}}
            offline_grab_result = requests.post(self.url,data=json.dumps(data),headers=self.headers)
            offline_grab_result.raise_for_status()
            self.log.logger.info("视频文件-离线抓拍查询" + str(data))
        except Exception as ex:
            self.log.logger.warning("视频文件-离线抓拍查询出现异常，从server接收响应失败！" + str(data))
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            offline_grab_result.json
        except Exception as ex:
            self.log.logger.warning("视频文件-离线抓拍查询出现异常，响应消息转换为json格式错误！" + str(data))
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(offline_grab_result.json())
    
if __name__ == "__main__":
    VideoRetrieval = FaceVideoRetrieval()
    result = VideoRetrieval.search_realtime_video(limit=10,c_id=[12])
    print(result)
    #result = VideoRetrieval.video_realtime_grabface(c_id=[11])
    result = VideoRetrieval.offline_grab_video(limit=10,c_id=[12])
    #result = VideoRetrieval.offline_video_search(limit=1,similarity=[0,1])   
    print(result)
    #print(len(result.get('return_data')))
    