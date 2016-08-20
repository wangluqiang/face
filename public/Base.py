#coding=utf-8
import LogConfig
import DMExceptions
import DataBase
from Config import Config
from gen_py.match import frs_match
from gen_py.match import ttypes
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol

class RESTAPIBase(object):
    '''
    封装的REST API类的父类，主要对初始化函数进行定义
    '''
    def __init__(self, ip=None, port=None, path=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        self.cfg = Config()
        if ip == None:
            self.server_ip = self.cfg.rest_server_info()["ip"]
        else:
            self.server_ip = ip
        if port == None:
            self.server_port = self.cfg.rest_server_info()["port"]
        else:
            self.server_port = port
        if db_ip == None:
            self.db_ip = self.cfg.db_info()['ip']
        else:
            self.db_ip = db_ip
        if db_port == None:
            self.db_port = self.cfg.db_info()['port']
        else:
            self.db_port = db_port
        if db_name == None:
            self.db_name = self.cfg.db_info()['name']
        else:
            self.db_name = db_name
        if db_user == None:
            self.db_user = self.cfg.db_info()['user']
        else:
            self.db_user = db_user
        if db_passwd == None:
            self.db_passwd = self.cfg.db_info()['passwd']
        else:
            self.db_passwd = db_passwd
        if path == None:
            self.server_path = self.cfg.url_path_info()["facedb"]
        else:
            self.server_path = path
        self.url = "http://"+self.server_ip+":"+str(self.server_port)+self.server_path
        self.headers = {'Content-Type':'application/json', 'charset':'UTF-8'}
        self.log = LogConfig.Logger()

class ThriftAPIBase(object):
    '''
    thrift接口封装的父类，主要对__init__函数
    '''
    def __init__(self, ip=None, port=None,  db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        self.cfg = Config()
        if ip == None:
            self.match_thrift_ip = self.cfg.thrift_match_info()["ip"]
        else:
            self.match_thrift_ip = ip
        if port == None:
            self.match_thrift_port = self.cfg.thrift_match_info()["port"]
        else:
            self.match_thrift_port = port
        if db_ip == None:
            self.db_ip = self.cfg.db_info()['ip']
        else:
            self.db_ip = db_ip
        if db_port == None:
            self.db_port = self.cfg.db_info()['port']
        else:
            self.db_port = db_port
        if db_name == None:
            self.db_name = self.cfg.db_info()['name']
        else:
            self.db_name = db_name
        if db_user == None:
            self.db_user = self.cfg.db_info()['user']
        else:
            self.db_user = db_user
        if db_passwd == None:
            self.db_passwd = self.cfg.db_info()['passwd']
        else:
            self.db_passwd = db_passwd
        self.log = LogConfig.Logger()
        try:
            self.transport = TSocket.TSocket(self.match_thrift_ip,self.match_thrift_port)
            self.transport = TTransport.TBufferedTransport(self.transport)
            self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
            self.client = frs_match.Client(self.protocol)
        except Exception as ex:
            self.log.logger.error("初始化失败")
            raise DMExceptions.FacePicRetrievalInitException(str(ex))
    def connect(self):
        '''
        功能：与比对端的thrift server建立连接
        输入：无
        输出：无
        '''
        try:
            self.transport.open()
            self.log.logger.info("thrift建立连接")
        except Exception as ex:
            self.log.logger.error("thrift建立连接失败")
            raise DMExceptions.ConnectException(str(ex))
    def close(self):
        '''
        功能：关闭thrift连接
        输入：无
        输出：无
        '''
        if(self.transport):
            try:
                self.transport.close()
                self.log.logger.info("关闭thrift连接")
            except Exception as ex:
                self.log.logger.error("关闭thrift连接失败")
                raise DMExceptions.FacePicRetrievalCloseException(str(ex))
        else:
            self.log.logger.error("无thrift连接导致关闭失败")
            raise DMExceptions.NoneTransportClose()

def get_id_by_name(ip=None, port=None, name=None, user=None, passwd=None, type="facedb", by_name="facedb_test"):
    items = {"facedb":{"table_name":"frs_facedb", "id_item":"fd_id", "name_item":"fd_name"},\
             "match":{"table_name":"frs_match", "id_item":"m_id", "name_item":"m_name"},\
             "preprocess":{"table_name":"frs_collection", "id_item":"p_id", "name_item":"p_name"},\
             "channel":{"table_name":"frs_channel", "id_item":"c_id", "name_item":"c_name"},\
             "device":{"table_name":"frs_device", "id_item":"device_id", "name_item":"device_name"},\
             "person":{"table_name":"frs_person", "id_item":"p_id", "name_item":"p_name"}}
    query_sql = "select "+items[type]["id_item"]+" from "+items[type]["table_name"]+\
                " where "+items[type]["name_item"]+"='"+by_name+"'"
    if ip==None:
        cfg = Config()
        db_ip = cfg.db_info()["ip"]
    else:
        db_ip  = ip
    if port==None:
        cfg = Config()
        db_port = cfg.db_info()["port"]
    else:
        db_port = int(port)
    if name == None:
        cfg = Config()
        db_name = cfg.db_info()["name"]
    else:
        db_name = name
    if user == None:
        cfg = Config()
        db_user = cfg.db_info()["user"]
    else:
        db_user = user
    if passwd == None:
        cfg = Config()
        db_passwd = cfg.db_info()["passwd"]
    else:
        db_passwd = passwd
    try:
        db = DataBase.DataBase(ip=db_ip, port=db_port, name=db_name, user=db_user, passwd=db_passwd)
        query_result_id	= db.fetch_all(query_sql)
        db.close()
    except DMExceptions.DBInitException as ex:
        print("connect to database fail!")
    except DMExceptions.DBNoneQueryException as ex:
        print("查询时数据库连接异常！")
    except DMExceptions.DBQueryException as ex:
        print("查询数据库失败!")
    except DMExceptions.NoDBQueryResultException as ex:
        print("查询数据库无信息！")
    except DMExceptions.DBNoneCloseException as ex:
        print("关闭数据库时无数据库连接！")
    except DMExceptions.DBCloseException as ex:
        print("关闭数据库时失败！")
    return query_result_id[0][0]

def get_max_id(ip=None, port=None, name=None, user=None, passwd=None, type="facedb"):
    items = {"facedb":{"table_name":"frs_facedb", "id_item":"fd_id"},\
             "match":{"table_name":"frs_match", "id_item":"m_id"},\
             "preprocess":{"table_name":"frs_collection", "id_item":"p_id"},\
             "channel":{"table_name":"frs_channel", "id_item":"c_id"},\
             "device":{"table_name":"frs_device", "id_item":"device_id"},\
             "person":{"table_name":"frs_person", "id_item":"p_id"}}
    query_sql = "select max("+items[type]["id_item"]+") from "+items[type]["table_name"]
    if ip==None:
        cfg = Config()
        db_ip = cfg.db_info()["ip"]
    else:
        db_ip  = ip
    if port==None:
        cfg = Config()
        db_port = cfg.db_info()["port"]
    else:
        db_port = int(port)
    if name == None:
        cfg = Config()
        db_name = cfg.db_info()["name"]
    else:
        db_name = name
    if user == None:
        cfg = Config()
        db_user = cfg.db_info()["user"]
    else:
        db_user = user
    if passwd == None:
        cfg = Config()
        db_user = cfg.db_info()["passwd"]
    else:
        db_passwd = passwd
    try:
        db = DataBase.DataBase(ip=db_ip, port=db_port, name=db_name, user=db_user, passwd=db_passwd)
        query_result_id	= db.fetch_all(query_sql)
        db.close()
    except DMExceptions.DBInitException as ex:
        print("connect to database fail!")
    except DMExceptions.DBNoneQueryException as ex:
        print("查询时数据库连接异常！")
    except DMExceptions.DBQueryException as ex:
        print("查询数据库失败!")
    except DMExceptions.NoDBQueryResultException as ex:
        print("查询数据库无信息！")
    except DMExceptions.DBNoneCloseException as ex:
        print("关闭数据库时无数据库连接！")
    except DMExceptions.DBCloseException as ex:
        print("关闭数据库时失败！")
    return query_result_id[0][0]


