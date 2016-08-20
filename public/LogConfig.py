#coding=utf-8
import logging   
import os,time,threading

def singleton(cls, *args, **kwargs):
  instances = {}
  def _singleton():
    if cls not in instances:
      instances[cls] = cls(*args, **kwargs)
    return instances[cls]
  return _singleton

logger=logging.getLogger('wangluqiang')

# @singleton
class Logger(object):
    def __init__(self,logfile=None):
        logger.setLevel(logging.INFO)
        if logfile == None:
            cur_path = os.path.split(os.path.realpath(__file__))[0]
            cur_time = time.strftime("%Y_%m_%d",time.localtime())
            filename = cur_path+"//..//log/log_"+str(cur_time)+".log"
        else:
            filename = logfile
        fh = logging.FileHandler(filename)#file
        fh.setLevel(logging.INFO)    
        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(filename)s:%(lineno)d %(funcName)s: %(message)s' )
        fh.setFormatter(formatter)   
        logger.addHandler(fh)
        # hacking the requests' logger
        requests_logger = logging.getLogger("requests")
        requests_logger.setLevel(logging.WARNING)
        self.logger=logger

if __name__ == "__main__":
    a1 = Logger()
    a1.logger.info("a11111")
    a2=Logger()
    a2.logger.info("a22222")