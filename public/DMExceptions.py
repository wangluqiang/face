#coding=utf-8
'''
    动态监控各封装接口用到的异常
'''
class GetHttpResponseError(Exception):
    '''
        发送了一个失败请求(非200响应)
    '''
    pass

class ResposeToJsonException(Exception):
    '''
    http响应信息转化为json失败异常
    '''
    pass

class ConnectException(Exception):
    '''
    功能：thrift连接异常
    '''
    pass

class RequestVideoDetectInitException(Exception):
    '''
        功能：RequestVideoDetect初始化失败异常
    '''
    pass

class RequestVideoDetectCloseException(Exception):
    '''
    功能：transport关闭异常
    '''
    pass

class NoneTransportClose(Exception):
    '''
    功能：transport不存在情况下关闭异常
    '''
    pass

class SendException(Exception):
    '''
    功能：thrift连接建立后，发送过程出现问题
    '''
    pass

class DBInitException(Exception):
    '''
    DataBase类初始化失败
    '''
    pass

class DBNoneQueryException(Exception):
    '''
            查询时数据库无连接异常
    '''
    pass

class DBQueryException(Exception):
    '''
    DataBase查询失败
    '''
    pass

class DBNoneCloseException(Exception):
    '''
                关闭数据库时无连接异常
    '''
    pass

class DBCloseException(Exception):
    '''
            关闭数据库失败
    '''
    pass


class FacePicRetrievalInitException(Exception):
    '''
        功能：FacePicRetrieval初始化失败异常
    '''
    pass

class FacePicRetrievalCloseException(Exception):
    '''
    功能：transport关闭异常
    '''
    pass


class ReadPicException(Exception):
    '''
    功能：读取照片异常
    '''
    #print("read pic error")
    pass




class NoDBQueryResultException(Exception):
    '''
    功能：查询数据库无该人脸库信息
    '''
    pass
class DataInvalidException(Exception):
    pass



class SetMatchInfoForPreprocessCloseException(Exception):
    pass
