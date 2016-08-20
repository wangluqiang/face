#coding=utf-8
import pymysql
import Config
import DMExceptions
class DataBase(object):
    '''
    封装的人脸库类，该类主要用于数据库的各种操作
    属性：db_server_ip：数据库的IP 
        db_server_port：数据库端口
        db_server_user：数据库用户名
        db_password：数据库密码
        db_name：数据库名称
        conn：数据库连接后返回的对象
        cursor：游标
    '''
    
    def __init__(self, ip=None, port=None, user=None, passwd=None, name=None):
        #设置参数
        if ip == None:
            cfg = Config.Config()
            self.db_server_ip = cfg.db_info()["ip"]
            #print(self.db_server_ip)
        else:
            self.db_server_ip = ip
        if port == None:
            cfg = Config.Config()
            self.db_server_port = int(cfg.db_info()["port"])
            #print(self.db_server_port)
        else:
            self.db_server_port = int(port)
        if user == None:
            cfg = Config.Config()
            self.db_server_user = cfg.db_info()["user"]
            #print(self.db_server_user)
        else:
            self.db_server_user = user
        if passwd == None:
            cfg = Config.Config()
            self.db_server_pwd = cfg.db_info()["passwd"]
            #print(self.db_server_pwd)
        else:
            self.db_server_pwd = passwd
        if name == None:
            self.db_name = cfg.db_info()["name"]
            #print(self.db_name)
        else:
            self.db_name = name
        try:
            self.conn = pymysql.connect(host=self.db_server_ip, port=self.db_server_port, user=self.db_server_user,\
                                 passwd=self.db_server_pwd, db=self.db_name, charset='utf8')
        except Exception as ex:
            raise DMExceptions.DBInitException(ex)
        
        if(self.conn):
            self.cursor = self.conn.cursor()

    
    def fetch_all(self, sql):
        '''
        功能：返回查询结果
         输入：sql：查询用SQL语句
        输出：查询结果
        '''
        if(self.conn):
            try:
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            except Exception as ex:
                raise DMExceptions.DBQueryException(str(ex))
        else:
            raise DMExceptions.DBNoneQueryException()
                

    def update(self, sql):
        '''
        功能：更新数据库操作，增、删、改
        输入：sql:更新用SQL语句
        输出：数据库更新结果，成功返回True,失败返回False
        '''
        flag = False
        if(self.conn):
            try:
                self.cursor.execute(sql)
                self.conn.commit()
                flag = True
            except Exception:
                flag = False
        return flag

    def close(self):
        '''
        功能：关闭数据库连接
        '''
        if(self.conn):
            try:
                if(type(self.cursor)=='object'):
                    self.cursor.close()
                if(type(self.conn)=='object'):
                    self.conn.close()
            except Exception as ex:
                raise DMExceptions.DBCloseException(str(ex))
        else:
            raise DMExceptions.DBNoneCloseException()
                

            
if __name__ == "__main__":
    db = DataBase()
    result = db.fetch_all("select fd_id from frs_facedb where fd_name='wujingjing_test'")
    db.close()
    print(result)
                
                
