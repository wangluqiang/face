#coding=utf-8
from gen_py.preprocess import net_video_service
from gen_py.preprocess import ttypes
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol
import DataBase
import Config
import DMExceptions

class SetMatchInfoForPreprocess(object):
    '''
    功能：修改预处理绑定的比对信息
    属性： preprocess_thrift_ip:比对端thrift的IP
    preprocess_thrift_port:比对端thrift的PORT
    tranport:thritf模块中网络读写抽象
    protocol:thrift模块中数据格式抽象
    client:thrift客户端
    '''
    
    def __init__(self, ip=None, port=None, db_ip=None, db_port=None, db_name=None, db_user=None, db_passwd=None):
        
        if ip == None:
            cfg = Config.Config()
            self.preprocess_thrift_ip = cfg.thrift_preprocess_info()["ip"]
        else:
            self.preprocess_thrift_ip = ip
        if port == None:
            cfg = Config.Config()
            self.preprocess_thrift_port = int(cfg.thrift_preprocess_info()["port"])
        else:
            self.preprocess_thrift_port = port
        if db_ip == None:
            self.db_ip = cfg.db_info()['ip']
        else:
            self.db_ip = db_ip
        if db_port == None:
            self.db_port = cfg.db_info()['port']
        else:
            self.db_port = db_port
        if db_name == None:
            self.db_name = cfg.db_info()['name']
        else:
            self.db_name = db_name
        if db_user == None:
            self.db_user = cfg.db_info()['user']
        else:
            self.db_user = db_user
        if db_passwd == None:
            self.db_passwd = cfg.db_info()['passwd']
        else:
            self.db_passwd = db_passwd
        try:
            self.transport = TSocket.TSocket(self.preprocess_thrift_ip,self.preprocess_thrift_port)
            print(self.preprocess_thrift_ip,self.preprocess_thrift_port)
            self.transport = TTransport.TBufferedTransport(self.transport)
            self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
            self.client = net_video_service.Client(self.protocol)
        except Exception as ex:
            raise DMExceptions.SetMatchInfoForPreprocessCloseException(str(ex))
        
    def connect(self):
        '''
        功能：建立thrift连接
        '''
        try:
            self.transport.open()
        except Exception as ex:
            raise DMExceptions.ConnectException(str(ex))
        
    def set_match_info(self, match_name=None, match_id=None, msg_type=7):
        '''
        功能：修改预处理服务绑定的比对
        输入：match_name：修改预处理绑定比对，比对名称
        match_id：修改预处理绑定比对，比对ID，名称和ID只用一个
        msg_type:默认为7
        '''
        db = DataBase.DataBase(ip=self.db_ip, port=self.db_port, name=self.db_name, user=self.db_user, passwd=self.db_passwd)
        if match_id != None:
            require_sql = "select m_ip,m_port from frs_match where m_id="+str(match_id)
        elif match_name != None:
            require_sql = "select m_ip,m_port from frs_match where m_name="+str(match_name)
        db_r = db.fetch_all(require_sql)
        m_ip = db_r[0][0]
        m_port =db_r[0][1]
        send_in = ttypes.match_conf(msg_type=msg_type, match_ip=m_ip, match_port=m_port)
        result = self.client.set_match_info(send_in)
        print(result)
     
    def close(self):
        '''
        功能：关闭thrift连接
        '''
        if(self.transport):
            try:
                self.transport.close()
            except Exception as ex:
                DMExceptions.SetMatchInfoForPreprocessCloseException(str(ex))
        else:
            raise DMExceptions.NoneTransportClose("no transport to close!")
        

       
if __name__ == "__main__":
    m = SetMatchInfoForPreprocess()
    m.connect()
    m.set_match_info(match_id=3)
    m.close()
            