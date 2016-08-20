#coding=utf-8
import os
import xml.dom.minidom

class Config(object):
    '''
        功能：对读取配置文件进行的类封装
        输入：配置文件名称
        属性：root:xml配置文件的根节点
    '''
    
    def __init__(self, file=None):

        if file == None:
            file = os.path.split(os.path.realpath(__file__))[0]+('\\..\\data')+'\\'+"config.xml"
            #print(file)
        try:
            dom = xml.dom.minidom.parse(file)
            self.root = dom.documentElement
        except Exception as ex:
            raise ConfigInitException(str(ex))
        
    def db_info(self):
        '''
            功能：从配置文件读取数据库的信息
            输出：字典格式：ip:数据库IP
            port:数据库端口
            user：数据库登录用户名
            passwd：数据库登录密码
            name:数据库名称
        '''    
        db_info = self.root.getElementsByTagName("db_server")
        db = {}
        db["ip"] = db_info[0].getAttribute("ip")
        db["port"] = db_info[0].getAttribute("port")
        db["user"] = db_info[0].getAttribute("user")
        db["passwd"] = db_info[0].getAttribute("passwd")
        db["name"] = db_info[0].getAttribute("name")
        return db
    
    def rest_server_info(self):
        '''
        功能：返回server的REST API使用的信息
        输出：字典格式
        '''  
        rest_info = self.root.getElementsByTagName("rest_server")  
        db = {}
        db["ip"] = rest_info[0].getAttribute("ip")
        db["port"] = rest_info[0].getAttribute("port")
        return db
    
    def thrift_server_info(self):
        '''
        功能：读取配置文件后的server的thrift信息
        '''
        thrift_info = self.root.getElementsByTagName("thrift_server")
        db = {}
        db["ip"] = thrift_info[0].getAttribute("ip")
        db["port"] = thrift_info[0].getAttribute("port")
        return db
    
    def thrift_match_info(self):
        '''
        功能：读取配置文件获得match的thrift信息
        '''
        thrift_info = self.root.getElementsByTagName("thrift_match")
        db = {}
        db["ip"] = thrift_info[0].getAttribute("ip")
        db["port"] = thrift_info[0].getAttribute("port")
        return db
    
    def thrift_preprocess_info(self):
        '''
        功能：读取配置文件获得preprocess的thrift信息
        '''
        thrift_info = self.root.getElementsByTagName("thrift_preprocess")
        db = {}
        db["ip"] = thrift_info[0].getAttribute("ip")
        db["port"] = thrift_info[0].getAttribute("port")
        return db
        
    def url_path_info(self):
        '''
        功能：读取配置文件，获得不同REST API的路径信息
        '''
        path_info = self.root.getElementsByTagName("path")
        data = {}
        dv = path_info[0].getElementsByTagName("device")[0]
        data[dv.tagName] = dv.firstChild.data
        pre = path_info[0].getElementsByTagName("preprocess")[0]
        data[pre.tagName] = pre.firstChild.data
        ma = path_info[0].getElementsByTagName("match")[0]
        data[ma.tagName] = ma.firstChild.data
        fd = path_info[0].getElementsByTagName("facedb")[0]
        data[fd.tagName] = fd.firstChild.data    
        ps = path_info[0].getElementsByTagName("person")[0]
        data[ps.tagName] = ps.firstChild.data
        rq = path_info[0].getElementsByTagName("require")[0]
        data[rq.tagName] = rq.firstChild.data
        fp = path_info[0].getElementsByTagName("facepic")[0]
        data[fp.tagName] = fp.firstChild.data
        fv = path_info[0].getElementsByTagName("video")[0]
        data[fv.tagName] = fv.firstChild.data
        gr=path_info[0].getElementsByTagName('grab_remark')[0]
        data[gr.tagName]=gr.firstChild.data
        return data
    
    def url_device_info(self):
        '''
        功能：读取配置文件，获取摄像头设备的信息
        '''
        device_info = self.root.getElementsByTagName("camera_device")
        #print(device_info)
        dv = {}
        dv_list = []
        for each in device_info:
           dv["ip"] = each.getAttribute("ip")
           dv["port"] = each.getAttribute("port") 
           dv["user"] = each.getAttribute("user") 
           dv["passwd"] = each.getAttribute("passwd")
           dv_list.append(dv)
        return dv_list

    def url_invalid_device_info(self):
        '''
        功能：读取配置文件，获取无效摄像头设备的信息
        '''
        device_info = self.root.getElementsByTagName("camera_device_invalid")
        #print(device_info)
        dv = {}
        dv_list = []
        for each in device_info:
           dv["ip"] = each.getAttribute("ip")
           dv["port"] = each.getAttribute("port")
           dv["user"] = each.getAttribute("user")
           dv["passwd"] = each.getAttribute("passwd")
           dv_list.append(dv)
        return dv_list

    def mail_from_info(self):
        '''
        功能：读取邮件发送人的信息
        '''
        mail_from_info = self.root.getElementsByTagName("mail_from")
        mail_from = {}
        mail_from["user"] = mail_from_info[0].getAttribute("user")
        mail_from["passwd"] = mail_from_info[0].getAttribute("passwd")
        return mail_from
        
    def mail_to_info(self):
        '''
        功能：读取邮件收件人的信息
        '''
        mail_to_info = self.root.getElementsByTagName("mail_to")
        mail_to_list = []
        for each in mail_to_info:
            mail_to_list.append(each.firstChild.data)
        return mail_to_list
        
class ConfigInitException(Exception):
    '''
    Config类初始化异常
    '''
    pass

if __name__ == "__main__":
    con = Config()
    #print(con.db_info())
    #print(con.rest_server_info())    
    #print(con.thrift_server_info())   
    print(con.mail_to_info())
            