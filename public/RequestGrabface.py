#coding=utf-8
import json
import requests
import unittest
import datetime
import DataBase
import Config
import LogConfig
import time
import DMExceptions
from Base import RESTAPIBase
from Base import get_id_by_name

class RequestGrabface(RESTAPIBase):
    '''
        功能：对抓拍人脸查询界面相关功能的封装。
    '''

    def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        if path == None:
            cfg = Config.Config()
            s_path = cfg.url_path_info()["require"]
        else:
            s_path = path
        RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)

    def list_match_request(self, type="search", c_id=None, c_name=None, **kwargs):
        #start_time, end_time,channel_name, low_similarity, high_similarity,\
        #person_name,s_type="search", offset=0, limit=10, condition_flag=[0]
        '''
        功能：动态监控版本界面的抓拍人脸查询中的比对结果查询功能
        输入：type:查询类型，默认为search
            c_name:查询的通道名称，列表格式
            c_id:查询的通道ID，列表格式
            kwargs:
                time:查询时间段
                similarity:查询的相似度范围
                p_name:查询的人员名称,列表格式
                condition_flag:预留值
                offset：偏移值
                limit：返回结果的个数
        输出：
        '''
        #构造http传输用data
        data = {}
        content = {}
        paging = []
        condition = []
        if type:
            data["type"] = type
        #根据通道名称查找通道ID
        if c_name:
            channel_id = []
            for name in c_name:
                result = get_id_by_name(ip=self.db_ip, port=self.db_port, name=self.db_name,\
                                       user=self.db_user, passwd=self.db_passwd, type="channel", by_name=name)
                channel_id.append(result)
            channel_con = {'c_id':channel_id,'operator':'in'}
            condition.append(channel_con)
        elif c_id:
            channel_con = {'c_id':c_id,'operator':'in'}
            condition.append(channel_con)
        if 'similarity' in kwargs:
            similarity_con = {'similarity':kwargs['similarity'],'operator':['>=','<=']}
            condition.append(similarity_con)
        if 'condition_flag' in kwargs:
            condition_f_con = {'condition_flag':[kwargs['condition_flag']],'operator':'in'}
            condition.append(condition_f_con)
        if "p_name" in kwargs:
            person_con = {"p_name":[kwargs['p_name']], "operator":"in"}
            condition.append(person_con)
        if "time" in kwargs:
            time_con = {'time':kwargs["time"],'operator':['>=','<=']}
            condition.append(time_con)
        #设置paging的内容
        if "offset" in kwargs:
            paging.append({"offset":kwargs["offset"]})
        if "limit" in kwargs:
            paging.append({"limit":kwargs["limit"]})
        data.update({"condition":condition, "paging":paging})
        try:
            before_time=time.time()
            request_result = requests.post(url=self.url, data=json.dumps(data), headers=self.headers)
            after_time=time.time()
            longs='%.0f'%((after_time-before_time)*1000)
            self.log.logger.info('比对查询用时:'+longs+'毫秒')
            request_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            request_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(request_result.json())


    def list_grabface_request(self, start_time, end_time, channel_name, s_type="grabface", offset=0, limit=1000):
        '''
        功能：动态监控版本对抓拍人脸界面的人脸查询功能封装
        输入：s_type：查询类型，默认为grab_face
        offset:偏移量，默认为 0
        limit：每页返回的个数
        start_time：查询抓拍人脸的开始时间
        end_time:查询抓拍人脸的结束时间
        channel_name:通道名称，列表格式
        输出：
        '''
        time_range = [start_time, end_time]
        time_con = "{'time':"+str(time_range)+",'operator':['>=','<=']}"
        channel_id = []
        db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
        for name in channel_name:
            require_sql = "select c_id from frs_channel where c_name='"+name+"'"
            result	= db.fetch_all(require_sql)
            if len(result) == 0:
                print("find frs_channel fail!")
            else:
                channel_id.append(result[0][0])
        channel_con = "{'c_id':"+str(channel_id)+",'operator':'in'}"
        #构造http发送的数据
        request_data = "{'type':'"+s_type+"','content':{'paging':[{'offset':'"+str(offset)+"'},{'limit':'"+str(limit)+"'}]"+",'condition':["+time_con+","+channel_con+"]}}"
        #print(request_data)
        try:
            before_time=time.time()
            request_result = requests.post(url=self.url, data=json.dumps(request_data), headers=self.headers)
            after_time=time.time()
            longs='%.0f'%((after_time-before_time)*1000)
            self.log.logger.info('人脸查询用时:'+longs+'毫秒')
            request_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            request_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(request_result.json())




if __name__ == "__main__":
    rq = RequestGrabface()
    #d = rq.list_match_request(start_time="2015-8-5 12:00:00", end_time="2015-8-5 14:00:00", channel_name=["test_1"],\
    #d = rq.list_grabface_request(start_time="2015-8-5 12:00:00", end_time="2015-8-5 14:00:00", \
    #							  channel_name=["test_1"])
    #print(d)

    #s_time = datetime.datetime.now()-datetime.timedelta(days=1)
    #f = open('1.txt','w')
    s_time=datetime.datetime.now()
    start_time='%s-%s-%s %s:%s:%s'%(s_time.year,s_time.month,s_time.day,s_time.hour-1,s_time.minute,s_time.second)
    end_time='%s-%s-%s %s:%s:%s'%(s_time.year,s_time.month,s_time.day,s_time.hour,s_time.minute,s_time.second)
    s_time=datetime.datetime.now()
    result = rq.list_match_request(start_time=start_time, end_time=end_time, channel_name=["0",'0'],low_similarity=0, high_similarity=1,person_name='')
    e_time=datetime.datetime.now()
    print(e_time-s_time)
    print(result['total'])
    #f.write(str(result))
    #f.close()