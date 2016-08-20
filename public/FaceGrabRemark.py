#coding=utf-8
__author__ = 'Administrator'
import requests,json
from DataBase import DataBase
import Config
import DMExceptions
from Base import RESTAPIBase

class FaceGrabRemark(RESTAPIBase):
    def __init__(self,path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        if path == None:
            cfg = Config.Config()
            s_path = cfg.url_path_info()["grab_remark"]
        else:
            s_path = path
        RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)
    def grab_remark_add(self,**kwargs):
        #封装查询抓拍人脸添加备注的功能
        #grab_id:抓拍人脸ID
        #sex:性别描述
        #age：年龄大小描述
        #'colour':肤色描述
        #glass：眼睛描述
        #face_feature：面部特征
        #clothes_feature：衣物特征
        #remark：备注
        face_grab_remark_add_data={}
        if 'grab_id' in kwargs:
            face_grab_remark_add_data.setdefault('grab_id',kwargs['grab_id'])
        if 'sex' in kwargs:
            face_grab_remark_add_data.setdefault('sex',kwargs['sex'])
        if 'age' in kwargs:
            face_grab_remark_add_data.setdefault('age',kwargs['age'])
        if 'colour' in kwargs:
            face_grab_remark_add_data.setdefault('colour',kwargs['colour'])
        if 'glass' in  kwargs:
            face_grab_remark_add_data.setdefault('glass',kwargs['glass'])
        if 'face_feature' in kwargs:
            face_grab_remark_add_data.setdefault('face_feature',kwargs['face_feature'])
        if 'clothes_feature' in kwargs:
            face_grab_remark_add_data.setdefault('clothes_feature',kwargs['clothes_feature'])
        if 'remark' in kwargs:
            face_grab_remark_add_data.setdefault('remark',kwargs['remark'])
        face_grab_remark_add_data=json.dumps(face_grab_remark_add_data)
        try:
            # print(self.url,face_grab_remark_add_data,self.headers)
            add_result=requests.post(self.url,data=face_grab_remark_add_data,headers=self.headers)
            add_result.raise_for_status()
            if add_result.status_code == 200:
                self.log.logger.info('添加grab_id为%s的备注成功'%(kwargs['grab_id']))
        except Exception as e:
            self.log.logger.error('添加抓拍备注异常')
            raise DMExceptions.GetHttpResponseError(str(e))
        return json.loads(add_result.json())
    def grab_remark_modify(self,grab_id=None,*kwargs):
        #封装抓拍人脸的修改功能
        face_grab_remark_modify_data={}
        if grab_id is None:
            face_grab_remark_modify_data.setdefault('grab_id',grab_id)
        face_grab_remark_modify_data.update(kwargs)
        try:
            modify_result=requests.put(self.url,data=json.dumps(face_grab_remark_modify_data),headers=self.headers)
            modify_result.raise_for_status()
            if modify_result.status_code==200:
                self.log.logger.info('修改ID为%s的备注信息成功'%(grab_id))
        except Exception as e:
            self.log.logger.error('修改备注信息异常')
            raise DMExceptions.GetHttpResponseError(str(e))
        return modify_result.json()

    def grab_remark_query(self):
        pass

    def grab_remark_delete(self):
        pass



if __name__=='__main__':
        fgr=FaceGrabRemark()
        fgr.grab_remark_add(grab_id='sadads',glass='有眼镜')
