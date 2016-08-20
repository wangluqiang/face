#coding=utf-8
import requests
import json 
from DataBase import DataBase
import Config
import DMExceptions
from Base import RESTAPIBase

class FaceDevice(RESTAPIBase):
    '''
     封装的设备配置类，该类主要用于设备的增、删、改、查
     属性：
     fdevice_path:URL路径

    '''
    #server_ip = "192.168.29.217"
    #server_port = 7000
    #server_path = "/v2/devices"
    
    #加载配置IP及path
    def __init__(self, path=None, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        if path == None:
            cfg = Config.Config()
            s_path = cfg.url_path_info()["device"]
        else:
            s_path = path
        RESTAPIBase.__init__(self, ip, port, s_path, db_ip, db_port, db_name, db_user, db_passwd)
               
	#配置通道信息
    def channel_add(self,c_no,c_name,fd_id_list=None,fd_name_list=None,**kwargs):
            
        '''功能：添加通道
           输入：
           c_no：通道号
           c_name：通道名称
           fd_id_list:人脸库id
           fd_id_name:人脸库名称，与fd_id_list只能有一个参数
        '''
        channel={}
        channel['c_no'] = c_no
        channel['c_name'] = c_name
        if fd_id_list:
            channel['fd_id_list'] = fd_id_list
        if fd_name_list:
            channel['fd_id_list'] = []
            for name in fd_name_list:
                Devicedb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
                sql_query_id = "select fd_id from frs_facedb where fd_name=%s"%(name)
                query_result_id = Devicedb.fetch_all(sql_query_id)
                Devicedb.close()
                channel['fd_id_list'].append(query_result_id[0][0])
        if 'c_id' in kwargs:
            channel['c_id']=kwargs['c_id']
        return channel
    
    #添加设备
    def facedevice_add(self, **kwargs):
        '''
                功能：添加设备
                输入：
                device_name:添加设备的名称
                device_ip/port：添加设备IP及端口
                url_user：用户名
                url_pwd:密码
                device_type:设备类型
                p_id:预处理id
                channel:通道信息
                输出：
                {"errorinfo": X}，x>0表示成功

            '''
        facedevice_add_data = {}
        if "device_name" in kwargs:
            facedevice_add_data['device_name'] = kwargs['device_name']
        if "device_ip" in kwargs:
            facedevice_add_data['device_ip'] = kwargs['device_ip']
        if "device_port" in kwargs:
            facedevice_add_data['device_port'] = kwargs['device_port']
        if "url_user" in kwargs:
            facedevice_add_data['url_user'] = kwargs['url_user']
        if "url_pwd" in kwargs:
            facedevice_add_data['url_pwd'] = kwargs['url_pwd']
        if "device_type" in kwargs:
            facedevice_add_data['device_type'] = kwargs['device_type']
        if "p_name" in kwargs:
            Devicedb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user,
                                passwd=self.db_passwd)
            sql_query_id = "select p_id from frs_collection where p_name='" + kwargs['p_name'] + "'"
            query_result_id = Devicedb.fetch_all(sql_query_id)
            Devicedb.close()
            p_id = query_result_id[0][0]
            facedevice_add_data['p_id'] = p_id
        if "p_id" in kwargs:
            facedevice_add_data['p_id'] = kwargs['p_id']

        if "p_name" not in kwargs and "p_id" not in kwargs:
            facedevice_add_data['p_id'] = 0
        if "remark" in kwargs:
            facedevice_add_data['remark'] = kwargs['remark']
        if "channel" in kwargs:
            facedevice_add_data['channel'] = kwargs['channel']
        facedevice_add_data = str(facedevice_add_data).replace('"', '')
        try:
            add_result = requests.post(self.url, data=json.dumps(facedevice_add_data), headers=self.headers)
            add_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            add_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(add_result.json())
    #删除设备
    def facedevice_delete(self, device_name=None, device_id=None):
        '''
        功能：删除设备
        输入：
        device_name:删除设备的名称
        device_id：删除设备的id
        输出：
        字典格式:{"errorinfo": 0}表示删除成功
        '''
        if device_name is None and device_id is None:
            return
        if device_id==None:        
        #根据设备名称查询设备id
            devicedb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            sql_query_id = "select device_id from frs_device where device_name='"+device_name+"'"
            query_result_id = devicedb.fetch_all(sql_query_id)
            devicedb.close()
            device_id = query_result_id[0][0]
            facedevice_delete_data = {"device_id":device_id}

        else:
            facedevice_delete_data={'device_id':device_id}
  
        try:
            delete_result = requests.delete(self.url, data=json.dumps(facedevice_delete_data), headers=self.headers)
            delete_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            delete_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(delete_result.json())
    #修改设备
    def facedevice_modify(self,device_name=None,device_id=None,**kwargs):
        '''
            功能：添加设备
            输入：
            device_id:设备id
            device_name:添加设备的名称
            device_ip/port：添加设备IP及端口
            url_user：用户名
            url_pwd:密码
            device_type:设备类型
            p_id:预处理id
            输出：
            {"errorinfo": 0}，表示成功
        '''
        if device_name is None and device_id is None:
            return
        if device_id==None:        
        #根据设备名称查询设备id
            devicedb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            sql_query_id = "select device_id from frs_device where device_name='"+device_name+"'"
            query_result_id = devicedb.fetch_all(sql_query_id)
            devicedb.close()
            device_id = query_result_id[0][0]
            facedevice_modify_data = {"device_id":device_id}
        else:
            facedevice_modify_data={'device_id':device_id}
        if "device_name_x" in kwargs:
            facedevice_modify_data["device_name"] = kwargs['device_name_x']
        if "device_ip" in kwargs:
            facedevice_modify_data["device_ip"] = kwargs['device_ip']        
        if "device_port" in kwargs:
            facedevice_modify_data["device_port"] = kwargs['device_port']    
        if "url_user" in kwargs:
            facedevice_modify_data["url_user"] = kwargs['url_user']    
        if "url_pwd" in kwargs:
            facedevice_modify_data["url_pwd"] = kwargs['url_pwd']    
        if "device_type" in kwargs:
            facedevice_modify_data["device_type"] = kwargs['device_type']    
        if "p_id" in kwargs:
            facedevice_modify_data["p_id"] = kwargs['p_id']
        if "p_name" in kwargs:
            devicedb = DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
            sql_query_id = "select device_id from frs_device where device_name='"+kwargs['p_name']+"'"
            query_result_id = devicedb.fetch_all(sql_query_id)
            devicedb.close()
            facedevice_modify_data["p_id"] = query_result_id[0][0]
        if "remark" in kwargs:
            facedevice_modify_data["remark"] = kwargs['remark']    
        if "channel" in kwargs:
            facedevice_modify_data["channel"] = kwargs['channel']    
        try:              
            modify_result = requests.put(self.url, data=json.dumps(facedevice_modify_data), headers=self.headers)
            modify_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            modify_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(modify_result.json())
    #查询设备
    def facedevice_query(self,**kwargs):
        '''
        功能：查询设备信息(只传url报错)
        输入：kwargs:
            device_id：设备id
            device_name：设备名称
        输出：列表格式，设备详细信息
        '''

        if 'device_id' not in kwargs and 'device_name' not in kwargs:
            url_query=self.url
        else:
            url_query=self.url+'?'
            if "device_id" in kwargs:
                url_query=url_query+'&device_id='+kwargs['device_id']
            if "device_name" in kwargs:
                url_query=url_query+'&device_name='+kwargs['device_name']
        try:
            query_result =requests.get(url_query)
            query_result.raise_for_status()
        except Exception as ex:
            raise DMExceptions.GetHttpResponseError(str(ex))
        try:
            query_result.json()
        except Exception as ex:
            raise DMExceptions.ResposeToJsonException(str(ex))
        return json.loads(query_result.json())


if __name__ == "__main__":
    facedevice_test = FaceDevice(ip="192.168.29.139", port=5000, db_ip="192.168.29.139", db_port=3306,\
                                 db_name="frs_auto_1120", db_user="opzoon", db_passwd="123.com")
    #添加-----------------------------
    channel1=facedevice_test.channel_add(0,'test0',fd_name_list=['facedb_test'])
    channel2=facedevice_test.channel_add(1,'test1',fd_name_list=['facedb_test'])
    channel=[channel1,channel2]
    #device_name,device_ip,device_port,url_user,url_pwd,device_type,p_id,channel,remark='test_add'
    print(facedevice_test.facedevice_add(device_name='test_socket',device_ip='192.168.1.2',device_port=1111,url_user='admin',url_pwd='admin',device_type=0,channel=channel))
    #    ----------------------------
    
    #修改----
    #channel1=facedevice_test.channel_add(0,'test77',[1,2,3],c_id='4')
    #channel2=facedevice_test.channel_add(1,'test99',[1,2,3],c_id='15')
    #channel=[channel1]
    #print(channel)
    print(facedevice_test.facedevice_modify(device_name='test_socket',device_name_x='socket99'))


    #删除-----
    print(facedevice_test.facedevice_delete('socket99'))
    
    #查询----
    #print(facedevice_test.facedevice_query())