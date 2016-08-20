#coding=utf-8
import requests
import json
import DataBase
import Config
import DMExceptions
from Base import RESTAPIBase

class SearchRealtimeVideo(RESTAPIBase):
    '''
    功能：对实时监控界面显示的类封装。
    '''

    def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        if path == None:
            cfg = Config.Config()
            s_path = cfg.url_path_info()["require"]
        else:
            s_path = path
        RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)
                
    def list_match_result(self, s_type='search_realtime_video', offset=0, limit=1):
        '''
        功能：实时人脸监控界面的比对结果显示功能
        输入：s_type：查询类型，默认为search_realtime_video，即列表比对结果
        offset：偏移值，默认为0
        limit：返回结果个数
        输出：
        '''
        data = "{'type':'"+s_type+"',"+"'content':{'paging':[{'offset':'"+str(offset)+"'},{'limit':'"+str(limit)+"'}]}}"
        #print(json.dumps(data))
        #print(self.url)
        search_result = requests.post(url=self.url, data=json.dumps(data), headers=self.headers)
        search_result.raise_for_status()
        try:
            search_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(search_result.json())
    
    def detail_match_result(self, s_type='search_detail', row=1, operator="="):
        '''
        功能：实时人脸监控界面的比对结果详情显示
        输入：s_type:查询类型，默认为search_detail，即显示详情
        row:查询比对结果中第几行的详细信息
        operator:默认=
        输出：
        '''
        #根据row获取r_id
        db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
        result_count = db.fetch_all("select count(*) from frs_result")
        db.close()
        #print(result_count)
        result_id = result_count[0][0]-row-1
        data = "{'type':'"+s_type+"','content':{'condition':[{'search_data_id':'"+str(result_id)+"','operator':'"\
                    +operator+"'}]}}"
        #print(data)
        search_result = requests.post(url=self.url, data=json.dumps(data), headers=self.headers)
        search_result.raise_for_status()
        try:
            search_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(search_result.json())
    
    def list_grabface(self, s_type='grabface', offset=0, limit=10):
        '''
        功能：实时人脸监控的抓拍人脸显示
        输入：s_type：查询类型，默认为grabface
        offset：默认为0
        limit：返回抓拍人脸图片的个数
        输出：
        '''
        data = "{'type':'"+s_type+"','content':{'paging':[{'offset':'"+str(offset)+"'},{'limit':'"+str(limit)+"'}]}}"
        list_result = requests.post(url=self.url, data=json.dumps(data), headers=self.headers)
        list_result.raise_for_status()
        try:
            list_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(list_result.json())


if __name__ == "__main__":
    search = SearchRealtimeVideo()
    #search.list_match_result()
    #print(search.list_match_result())
    #print(search.detail_match_result(row=1))
    print(search.list_grabface())
    