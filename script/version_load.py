#coding=utf-8
from ftplib import FTP
import time,os
import zipfile

def load_version():
    ftp = FTP()
    ftp.connect("192.168.29.210",21,30)
    ftp.login()
    ftp.cwd("FaceVersion/")
    file = []
    ftp.retrlines('LIST',file.append)
    #file_1 = ftp.nlst()
    #print(file_1)
    file.sort(key=lambda file:time.mktime(time.strptime(file[:17], "%m-%d-%y %H:%M%p")))
    file_name = file[-1].split()[-1]
    print(file_name)
    load_file_path = "E:\\FRS\\版本\\"+file_name
    print(load_file_path)
    load_fp = open(load_file_path,"wb")
    ftp.retrbinary("RETR %s" % file_name, load_fp.write)
    ftp.quit()
    load_fp.close()
    #解压缩文件
    print(load_file_path)
    os.chdir("E:\\FRS\\版本\\")
    os.mkdir(file_name[:-4])
    f = zipfile.ZipFile(file_name,"r")
    for file in f.namelist():
        f.extract(file, "E:\\FRS\\版本\\"+file_name[:-4])
    #print(file_1)
    #分别解压缩不同压缩包
    os.chdir(file_name[:-4])
    cur_file_list = os.listdir(path='.')
    print(cur_file_list)
    for each in cur_file_list:
        if zipfile.is_zipfile(each):
            f = zipfile.ZipFile(each,"r")
            for f_e in f.namelist():
                f.extract(f_e, ".")

def run_service():
    software_path = "E:\FRS\版本\FRSV2.1.5.819"
    os.chdir(software_path)
    #修改比对服务信息且启动
    os.chdir("match")
    match_conf = open("service.conf","r+")
    conf_list = match_conf.readlines()
    conf_list[19] = "        <server_ip>192.168.29.213</server_ip>\n"
    conf_list[21] = "        <listen_ip>192.168.29.213</listen_ip>\n"
    match_conf.seek(0,0)
    match_conf.writelines(conf_list)
    match_conf.close()
    #修改预处理信息且启动
    os.chdir("..//preprocess")
    pre_conf = open("preprocess.ini","r+")
    pre_list = pre_conf.readlines()
    pre_list[1] = "listen_ip=192.168.29.213\n"
    pre_list[3] = "server_ip=192.168.29.213\n"
    pre_conf.seek(0,0)
    pre_conf.writelines(pre_list)
    pre_conf.close()
    #修改server信息且启动
    os.chdir("..//FRSServerV2.1.5.819")
    server_conf = open("opzoonfrs.yaml","r+")
    ser_list = server_conf.readlines()
    ser_list[23] = "    DB_IP: '192.168.29.213'\n"
    ser_list[32] = "    THRIFT_HOST: '192.168.29.213'\n"
    server_conf.seek(0,0)
    server_conf.writelines(ser_list)
    server_conf.close()
    
if __name__ == "__main__":
    #load_version()
    run_service()