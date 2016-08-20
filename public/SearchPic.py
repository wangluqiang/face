#coding=utf-8

import os
import requests
import json 
import base64
from DataBase import DataBase
import Config
import DMExceptions
from Base import RESTAPIBase
from Base import get_id_by_name


class SearchPic(RESTAPIBase):
    '''
     封装的人脸图像检索类，该类主要用于人脸图像信息的检索
     属性：
     fsearch_server_ip:操作服务器的IP地址
     fsearch_server_port:操作服务器的端口值
     fsearch_path:URL路径
     url:http的完整路径
    '''
    #server_ip = "192.168.29.217"
    #server_port = 7000
    #server_path = "/v2/facepic"

    def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        if path == None:
            cfg = Config.Config()
            s_path = cfg.url_path_info()["facepic"]
        else:
            s_path = path
        RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)

    #读取照片
    def pic_read(self,filename):
        pic_file_path = os.path.split(os.path.realpath(__file__))[0]+('\\..\\picture')+'\\'+filename
        try:
            file_obj =	open(pic_file_path,	'rb')
            pic_buffer = file_obj.read()
        except Exception as ex:
            raise DMExceptions.ReadPicException(str(ex))
        finally:
            file_obj.close()
        return pic_buffer


    def facepic_search(self, pic_name=None, fd_id=None, fd_name=None, **kwargs):
        '''
            功能：人脸图像检索
            输入：
            pic_name：照片名称
            fd_id:人脸库ID
            fd_name:人脸库名称
            **kwargs包含参数：
                p_name：人员姓名
                return_num：返回的个数
                threshold：相似度

            输出：字典格式：
            检索详细信息
        '''
        facepic_search_data = {}
        facepic_search_data['type'] = 0
        if pic_name != None:
            #判断是否是图片名称
            if pic_name.split(".")[-1] in ['jpg',"jpeg","png","bmp"]:
                pic = self.pic_read(pic_name)
                facepic_search_data['content'] = base64.b64encode(pic).decode()
            else:
                facepic_search_data["content"] = pic_name
        if fd_id:
            facepic_search_data["fd_id"] = fd_id
        if fd_name:
            fd_id = get_id_by_name(ip=self.db_ip, port=self.db_port, name=self.db_name, \
                                       user=self.db_user, passwd=self.db_passwd, type="facedb", by_name=fd_name)
            facepic_search_data["fd_id"] = fd_id
        condition={}
        condition.update(kwargs)
        facepic_search_data['condition'] = condition
        try:
            search_result = requests.post(self.url,data=json.dumps(facepic_search_data),headers=self.headers)
            search_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            search_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(search_result.json())


if __name__ == "__main__":
    SearchPic_test = SearchPic()
    result=SearchPic_test.facepic_search(pic_name='5.jpg', fd_name="facedb_test", return_num=2, threshold=0)
    print(result)
    #for each in result['return_data']:
    #    print(each['p_id'],each['p_name'],each['score'],each['fd_name'])
