#coding=utf8

import json
import logging
import requests

import Config
import DataBase
import LogConfig
import DMExceptions
from Base import RESTAPIBase

class FaceVideo(RESTAPIBase):
    '''
     封装的视频文件管理类，该类主要用于视频文件的增加、删除、查询
     属性：
     fv_path:URL路径
     url:http的完整路径
    '''
    def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        if path == None:
            cfg = Config.Config()
            s_path = cfg.url_path_info()["video"]
        else:
            s_path = path
        RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)
        
    def facevideo_add(self,name=None):
        '''
        功能：增加视频文件
        输入：name：视频文件名称
        输出：字典格式:{"video_id": 32, "video_name": "test(2).mp4"}
        '''
        video_data = {}
        if name:
            video_data = {"video_name":name}
        try:
            add_result = requests.post(self.url,data=json.dumps(video_data),headers=self.headers)
            add_result.raise_for_status()
            if name:
                self.log.logger.info("添加视频文件名称为："+name)
        except Exception as ex:
            self.log.logger.warning("添加视频文件出现异常，从server接收响应失败！添加视频文件名称为："+str(id))
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            add_result.json()            
        except Exception as ex:
            self.log.logger.warning("添加视频文件出现异常，响应消息转换为json格式错误！添加视频文件名称为："+str(id))
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(add_result.json())
    
    def facevideo_delete(self,id=None,name=None):
        '''
        功能：删除视频文件
        输入：id：删除视频文件的id
        kwargs: name 视频文件名称
        输出：字典格式:{"errorinfo": 0}表示删除成功
                {"errorinfo": -6}表示删除失败
        '''
        if name:
            db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            require_sql = "select c_id from frs_channel where  type=1 and c_name='"+name+"'"
            result  = db.fetch_all(require_sql)
            v_id = result[0][0]
            db.close()
        else:
            v_id = id
        try:
            if 'v_id' in locals().keys():
                delete_result = requests.delete(self.url+'?video_id='+str(v_id))
                delete_result.raise_for_status()
                self.log.logger.info("删除视频文件id为："+str(v_id))
            else:
                delete_result = requests.delete(self.url+'?video_id=')
                delete_result.raise_for_status()
        except Exception as ex:
            self.log.logger.warning("删除视频文件出现异常，从server接收响应失败！删除视频文件名称为："+str(id))
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            delete_result.json()
        except Exception as ex:
            self.log.logger.warning("删除视频文件出现异常，响应消息转换为json格式错误！删除视频文件名称为："+str(id))
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(delete_result.json())
        
    def facevideo_query(self):
        '''
        功能：查询全部视频文件
        输入：空
        输出：列表格式，视频文件详细信息
        '''
        try:
            query_result = requests.get(self.url)
            query_result.raise_for_status()
            self.log.logger.info("查询视频文件")
        except Exception as ex:
            self.log.logger.warning("查询视频文件出现异常，从server接收响应失败！")
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:   
            query_result.json()
        except Exception as ex:
            self.log.logger.warning("查询视频文件出现异常，响应消息转换为json格式错误！")
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(query_result.json())
    
if __name__ == "__main__":
    videos = FaceVideo()
    
    print(videos.facevideo_add('test.'))
    print(videos.facevideo_query())
    print(videos.facevideo_delete(name='test.'))
    print(videos.facevideo_query())
    #r = videos.facevideo_delete(3)
    #r = videos.facevideo_delete(9)
    #r = videos.facevideo_delete('q9')
    #r = videos.facevideo_delete([9])
    #r = videos.facevideo_delete()
    #r = videos.facevideo_query()
