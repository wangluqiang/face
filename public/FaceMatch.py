#coding=utf-8
import requests
import json 
from DataBase import DataBase
import Config
import DMExceptions
from Base import RESTAPIBase

class FaceMatch(RESTAPIBase):
    '''
     封装的比对服务配置，该类主要用于比对服务的增、删、改、查
     属性：
     fm_path:URL路径
     url:http的完整路径
    '''
    #加载配置IP及path
    def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        if path == None:
            cfg = Config.Config()
            s_path = cfg.url_path_info()["match"]
        else:
            s_path = path
        RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)
        
    def facematch_add(self,**kwargs):   
        '''
            功能：添加比对服务
            输入：
            m_name:添加比对服务的名称
            m_ip：比对服务IP地址
            m_port：比对服务端口
            face_max：人脸最大数
            client_max：客户端最大数
            min_face_pixel：最小像素
            max_face_pixel：最大像素
            输出：字典格式：
            {"errorinfo": X}，表示成功
            
        '''
        facematch_add_data={}
        if "m_name" in kwargs:
            facematch_add_data['m_name'] = kwargs['m_name']
        if "m_ip" in kwargs:
            facematch_add_data['m_ip'] = kwargs['m_ip']
        if "m_port" in kwargs:
            facematch_add_data['m_port'] = kwargs['m_port']
        if "face_max" in kwargs:
            facematch_add_data['face_max'] = kwargs['face_max']
        if "client_max" in kwargs:
            facematch_add_data['client_max'] = kwargs['client_max']
        if "min_face_pixel" in kwargs:
            facematch_add_data['min_face_pixel'] = kwargs['min_face_pixel']
        if "max_face_pixel" in kwargs:
            facematch_add_data['max_face_pixel'] = kwargs['max_face_pixel']
        if "remark" in kwargs:
            facematch_add_data['remark'] = kwargs['remark']

        try:
            add_result = requests.post(self.url, data=json.dumps(facematch_add_data), headers=self.headers)
            add_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            add_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(add_result.json())
    
    def facematch_delete(self, m_name=None, m_id=None):
        '''
        功能：删除比对服务
        输入：
        m_name：删除比对服务的名称
        m_id：删除比对服务的id
        输出：字典格式:{"errorinfo": 0}表示删除成功
        '''
        if m_name is None and m_id is None:
            return
        if m_id==None:        
            matchdb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            sql_query_id = "select m_id from frs_match where m_name='"+m_name+"'"
            query_result_id = matchdb.fetch_all(sql_query_id)
            matchdb.close()
            m_id = query_result_id[0][0]
            facematch_delete_data = {"m_id":m_id}
        else:
            facematch_delete_data={'m_id':m_id}
        try:
            delete_result = requests.delete(self.url, data=json.dumps(facematch_delete_data), headers=self.headers)
            delete_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            delete_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(delete_result.json())
    
    def facematch_modify(self,m_name,m_id=None,**kwargs):
        '''
        功能：修改比对服务
        输入：
            m_id:修改比对服务id
            m_name:修改比对服务的名称
            m_ip：比对服务IP地址
            m_port：比对服务端口
            face_max：人脸最大数
            client_max：客户端最大数
            min_face_pixel：最小像素
            max_face_pixel：最大像素
        输出：字典格式：{"errorinfo": 0} 表示修改成功
        '''
        
        if m_id==None:        
            matchdb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            sql_query_id = "select m_id from frs_match where m_name='"+m_name+"'"
            query_result_id = matchdb.fetch_all(sql_query_id)
            matchdb.close()
            m_id = query_result_id[0][0]
            facematch_modify_data = {"m_id":m_id}
        else:
            facematch_modify_data={'m_id':m_id}

        if "m_name_x" in kwargs:
            facematch_modify_data["m_name"] = kwargs['m_name_x']
        if "face_max" in kwargs:
            facematch_modify_data["face_max"] = kwargs['face_max']
        if "client_max" in kwargs:
            facematch_modify_data["client_max"] = kwargs['client_max']
        if "min_face_pixel" in kwargs:
            facematch_modify_data["min_face_pixel"] = kwargs['min_face_pixel']
        if "max_face_pixel" in kwargs:
            facematch_modify_data["max_face_pixel"] = kwargs['max_face_pixel']
        if "remark" in kwargs:
            facematch_modify_data["remark"] = kwargs['remark']        
        if "m_ip" in kwargs:
            facematch_modify_data['m_ip'] = kwargs['m_ip']
        if "m_port" in kwargs:
            facematch_modify_data['m_port'] = kwargs['m_port']
        try:
            modify_result = requests.put(self.url, data=json.dumps(facematch_modify_data), headers=self.headers)
            modify_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            modify_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(modify_result.json())
    
    def facematch_query(self):
        '''
        功能：查询全部比对服务
        输入：空
        输出：列表格式，比对服务详细信息
        '''
        try:
            query_result =requests.get(self.url)
            query_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            query_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(query_result.json())


if __name__ == "__main__":
    facematch_test = FaceMatch(ip='192.168.29.139', port=5000, db_ip='192.168.29.139', db_port=3306, db_name='frs_auto_1120', db_user='opzoon', db_passwd='123.com')
    #m_name,m_ip,m_port,face_max,client_max,min_face_pixel,max_face_pixel,remark='test'
    print(facematch_test.facematch_add(m_name='test119',m_ip='192.168.2.3',m_port=8000,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12))
    print(facematch_test.facematch_modify('test119',m_name_x='test911',m_ip='192.168.2.3',m_port=8000))
    print(facematch_test.facematch_query())
    print(facematch_test.facematch_delete('test911'))
    print(facematch_test.facematch_query())
