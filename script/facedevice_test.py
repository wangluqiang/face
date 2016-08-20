#coding=utf-8
import unittest
import os
import sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import FaceDevice
import DataBase
import DMExceptions
import LogConfig
from handle_exception import handle_exception


class FaceDeviceTestCase(unittest.TestCase):
    '''设备的相关功能测试脚本'''
    @classmethod
    def setUpClass(cls):
        # print('初始化')
        cls.facedevice = FaceDevice.FaceDevice()
        cls.db=DataBase.DataBase()
        cls.log=LogConfig.Logger()
        cls.items={}
    @classmethod
    def tearDownClass(cls):
        '''清除工作，关闭数据库连接，清除测试中增加的数据'''
        cls.db.close()

    @handle_exception
    def test_facedevice_add_name_ADDDEVICE_ip_129(self):
        self.log.logger.info('')
        channel1=self.facedevice.channel_add(0,'test0',[1,2,3])
        channel2=self.facedevice.channel_add(1,'test1',[1,2,3])
        channel=[channel1,channel2]
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE',device_ip='129.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.assertGreater(result["errorinfo"],0,'添加设备错误')
        self.items['facedevice']=result
        require_sql = "select * from frs_device where device_id="+str(result['errorinfo'])
        require_result = self.db.fetch_all(require_sql)
        if len(require_result) < 1:
            self.fail("add facedevice to frs_collection error!")
        else:
            self.assertEqual(require_result[0][1], "ADDDEVICE", "add facedevice name error!")
            self.assertEqual(require_result[0][2], '129.9.9.9', "add facedevice ip error!")
            self.assertEqual(require_result[0][3],9999,"add facedevice port error!")
            self.assertEqual(require_result[0][4],'admin',"add facedevice user error!")
            self.assertEqual(require_result[0][5],'admin',"add facedevice pwd error!")

    @handle_exception
    def test_facedevice_add_used(self):
        #添加一个设备
        self.log.logger.info('')
        channel1=self.facedevice.channel_add(0,'test0',[1,2,3])
        channel2=self.facedevice.channel_add(1,'test1',[1,2,3])
        channel=[channel1,channel2]
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE',device_ip='129.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.items['facedevice']=result
        #再次添加名称相同的设备
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE',device_ip='129.1.1.1',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.assertEqual(result['errorinfo'],-7,'添加已存在名称的设备返回错误码不正确')
        #添加ip和port相同的设备
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE_1',device_ip='129.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.assertEqual(result['errorinfo'],-7,'添加已存在的设备IP和PORT返回错误码不正确')
    @handle_exception
    def test_facedevice_add_json_format_error(self):
        #添加设备不输入名称
        result = self.facedevice.facedevice_add(device_ip='129.9.9.12',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        # print(result['errorinfo'])
        self.assertEqual(result['errorinfo'],-650,'添加设备不输入名称返回错误码不正确')
        #添加设备不输入IP或port
        result=self.facedevice.facedevice_add(device_name='ADDDEVICE_5',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        # print(result['errorinfo'])
        self.assertEqual(result['errorinfo'],-650,'添加设备不输入IP或PORT返回错误码不正确')
        result=self.facedevice.facedevice_add(device_name='ADDDEVICE_6',device_ip='129.9.9.9',url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        # print(result['errorinfo'])
        self.assertEqual(result['errorinfo',-650],'添加设备不输入IP或PORT返回错误码不正确')
        #添加设备不输入用户名或密码
        result=self.facedevice.facedevice_add(device_name='ADDDEVICE_7',device_ip='129.9.9.10',device_port=9999,url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo',-650],'添加设备不输入用户名或密码返回错误码不正确')
        result=self.facedevice.facedevice_add(device_name='ADDDEVICE_8',device_ip='129.9.9.11',device_port=9999,url_user='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo',-650],'添加设备不输入用户名或密码返回错误码不正确')

    @handle_exception
    def test_facedevice_add_json_value_error(self):
        #添加名称为空
        result = self.facedevice.facedevice_add(device_name='',device_ip='129.1.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-651,'添加设备名称为空返回错误码不正确')
        #添加IP或PORT为空
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE_9',device_ip='',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-651,'添加设备IP为空返回错误码不正确')
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE_10',device_ip='129.2.9.9',device_port='',url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-651,'添加设备port为空返回错误码不正确')
        #添加用户名或密码为空
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE_11',device_ip='129.4.9.9',device_port=9999,url_user='',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-651,'添加设备用户名为空返回错误码不正确')
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE_14',device_ip='129.3.9.9',device_port=9999,url_user='admin',url_pwd='',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-651,'添加设备密码为空返回错误码不正确')
        #添加IP为错误格式字符串
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE_12',device_ip='IP',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-651,'添加设备输入错误格式IP返回错误码不正确')
        #添加Port为错误格式port
        result = self.facedevice.facedevice_add(device_name='ADDDEVICE_13',device_ip='129.5.9.9',device_port='port',url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-651,'添加设备输入错误格式PORT返回错误码不正确')
        #添加设备输入的p_id不存在
        result=self.facedevice.facedevice_add(device_name='ADDDEVICE_100',device_ip='139.5.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_id=9999)
        self.assertEqual(result['errorinfo'],-651,'添加设备绑定的预处理不存在时返回错误码不正确')
        #添加设备输入的p_id为错误格式
        result=self.facedevice.facedevice_add(device_name='ADDDEVICE_101',device_ip='149.5.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_id='preprocess_test')
        self.assertEqual(result['errorinfo'],-651,'添加设备预处理Id传递字符串返回错误码不正确')

    @handle_exception
    def test_facedevice__add_fail(self):

        #名称为大于32位的字符串
        name='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result = self.facedevice.facedevice_add(device_name=name,device_ip='129.1.1.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-4,'添加设备输入名称太长返回错误码不正确')
        #用户名为大于32位的字符串
        name='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result = self.facedevice.facedevice_add(device_name='advice_20',device_ip='129.1.2.9',device_port=9999,url_user=name,url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-4,'添加设备输入用户名太长返回错误码不正确')
        #密码为大于32位的字符串
        passwd='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result = self.facedevice.facedevice_add(device_name='advice_21',device_ip='129.1.3.9',device_port=9999,url_user='admin',url_pwd=passwd,device_type=0,p_name='preprocess_test')
        self.assertEqual(result['errorinfo'],-4,'添加设备输入密码太长返回错误码不正确')
        #备注为大于256位的字符串
        remark='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result = self.facedevice.facedevice_add(device_name='advice_22',device_ip='129.1.4.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',remark=remark)
        self.assertEqual(result['errorinfo'],-4,'添加设备输入备注太长返回错误码不正确')
    @handle_exception
    def test_facedevice_modify_name_test2999(self):
        channel1=self.facedevice.channel_add(0,'test0',[1,2,3])
        channel2=self.facedevice.channel_add(1,'test1',[1,2,3])
        channel=[channel1,channel2]
        result_add = self.facedevice.facedevice_add(device_name='test299',device_ip='129.9.9.8',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.assertGreaterEqual(result_add["errorinfo"],0)
        self.items['facedevice']=result_add
        result = self.facedevice.facedevice_modify('test299',result_add['errorinfo'],device_name_x='test2999',device_ip='159.7.7.7',device_port=7777,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertGreaterEqual(result["errorinfo"],0)
        require_sql = "select * from frs_device where device_id="+str(result_add['errorinfo'])
        require_result = self.db.fetch_all(require_sql)
        if len(require_result) < 1:
            self.fail("modify facedeviceto frs_collection error!")
        else:
            self.assertEqual(require_result[0][1], "test2999", "modify device name error!")
            self.assertEqual(require_result[0][2], '159.7.7.7', "modify device ip error!")
            self.assertEqual(require_result[0][3],7777,"modify device port error!")

    @handle_exception
    def test_facedevice_modify_used(self):
        #先添加两个设备
        channel1=self.facedevice.channel_add(0,'test0',[1,2,3])
        channel2=self.facedevice.channel_add(1,'test1',[1,2,3])
        channel=[channel1,channel2]
        result = self.facedevice.facedevice_add(device_name='MODIFY',device_ip='19.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        result1 = self.facedevice.facedevice_add(device_name='MODIFY1',device_ip='20.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.items.setdefault('facedevice',[result,result1])
        #修改其中一个设备为已存在的设备名称
        result_modify=self.facedevice.facedevice_modify(result1['errorinfo'],device_name='MODIFY',device_ip='20.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.assertEqual(result_modify['errorinfo'],-7)
        #修改其中一个设备为已存在的设备IP和PORT
        result_modify=self.facedevice.facedevice_modify(result1['errorinfo'],device_name='MODIFY1',device_ip='19.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.assertEqual(result_modify['errorinfo'],-7)
        #为其中一个设备添加通道，通道号相同
        channel3=self.facedevice.channel_add(0,'test3')
        channel.append(channel3)
        result_modify=self.facedevice.facedevice_modify(result1['errorinfo'],device_name='MODIFY1',device_ip='20.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.assertEqual(result_modify['errorinfo'],-7)
        #为其中一个设备添加通道，通道名称相同used
        channel4=self.facedevice.channel_add(4,'test0')
        channel=[channel1,channel2,channel4]
        result_modify=self.facedevice.facedevice_modify(result1['errorinfo'],device_name='MODIFY1',device_ip='20.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.assertEqual(result_modify['errorinfo'],-7)
    @handle_exception
    def test_facedevice_modify_json_format_error(self):
        #添加一个设备
        result = self.facedevice.facedevice_add(device_name='MODIFY_JSON',device_ip='109.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.items.setdefault('facedevice',result)
        #修改该设备时不传递名称
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_ip='109.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_1['errorinfo'],-650)
        #修改该设备时不传递ip或port
        result_2=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_JSON',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_2['errorinfo'],-650)
        result_2=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_JSON',device_ip='109.9.9.9',url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_2['errorinfo'],-650)
        #修改该设备时不传递用户名或密码
        result_3=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_JSON',device_ip='109.9.9.9',device_port=9999,url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_3['errorinfo'],-650)
        result_3=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_JSON',device_ip='109.9.9.9',device_port=9999,url_user='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_3['errorinfo'],-650)

    @handle_exception
    def test_facedevice_modify_value_error(self):
        #添加一个设备
        result=self.facedevice.facedevice_add(device_name='MODIFY_VALUE',device_ip='49.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.items.setdefault('facedevice',result)
        #修改该设备名称为空
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='',device_ip='49.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_1['errorinfo'],-651)
        #修改该设备IP或PORT为空或为非法字符
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_VALUE',device_ip='',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_1['errorinfo'],-651)
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_VALUE',device_ip='asdasd',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_1['errorinfo'],-651)
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_VALUE',device_ip='49.9.9.9',device_port='',url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_1['errorinfo'],-651)
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_VALUE',device_ip='49.9.9.9',device_port='asdas',url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_1['errorinfo'],-651)
        #修改该设备用户名或密码为空
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_VALUE',device_ip='49.9.9.9',device_port=9999,url_user='',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_1['errorinfo'],-651)
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_VALUE',device_ip='49.9.9.9',device_port=9999,url_user='admin',url_pwd='',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_1['errorinfo'],-651)
        #修改该设备绑定预处理为不存在或预处理为字符串
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_VALUE',device_ip='49.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_id=9999)
        self.assertEqual(result_1['errorinfo'],-651)
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_VALUE',device_ip='49.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_id='asdasd')
        self.assertEqual(result_1['errorinfo'],-651)
    @handle_exception
    def test_facedevice_modify_error(self):
        #添加设备
        result=self.facedevice.facedevice_add(device_name='MODIFY_ERROR',device_ip='56.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.items.setdefault('facedevice',result)
        #修改设备名称为大于32位的字符串
        name='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name=name,device_ip='56.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test')
        self.assertEqual(result_1['errorinfo'],-4)
        #修改设备备注为大于256位的字符串
        remark='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result_1=self.facedevice.facedevice_modify(device_id=result['errorinfo'],device_name='MODIFY_ERROR',device_ip='56.9.9.9',device_port=9999,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',remark=remark)
        self.assertEqual(result_1['errorinfo'],-4)

    @handle_exception
    def test_facedevice_query_name_test299(self):
        channel1=self.facedevice.channel_add(0,'test0',[1,2,3])
        channel2=self.facedevice.channel_add(1,'test1',[1,2,3])
        channel=[channel1,channel2]
        result_add = self.facedevice.facedevice_add(device_name='test299',device_ip='129.4.4.4',device_port=4444,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.items.setdefault('facedevice',result_add)
        self.assertGreaterEqual(result_add["errorinfo"],0)
        result = self.facedevice.facedevice_query()
        #print(result)
        self.assertEqual(result[-1]["device_name"],'test299')
        self.assertEqual(result[-1]["device_ip"],'129.4.4.4')
        self.assertEqual(result[-1]["device_port"],4444)
        self.assertEqual(result[-1]["url_user"],'admin')
        self.assertEqual(result[-1]["url_pwd"],'admin')
        result_del = self.facedevice.facedevice_delete('test299',result_add["errorinfo"])
        self.assertGreaterEqual(result_del["errorinfo"],0)

    @handle_exception
    def test_facedevice_delete_name_test299(self):
        channel1=self.facedevice.channel_add(0,'test0',[1,2,3])
        channel2=self.facedevice.channel_add(1,'test1',[1,2,3])
        channel=[channel1,channel2]
        result_add = self.facedevice.facedevice_add(device_name='test299',device_ip='129.5.5.5',device_port=5555,url_user='admin',url_pwd='admin',device_type=0,p_name='preprocess_test',channel=channel)
        self.items.setdefault('facedevice',result_add)
        self.assertGreaterEqual(result_add["errorinfo"],0)
        result = self.facedevice.facedevice_delete('test299',result_add["errorinfo"])
        self.assertGreaterEqual(result["errorinfo"],0)
        require_sql = "select * from frs_device where device_id="+str(result_add["errorinfo"])
        require_result = self.db.fetch_all(require_sql)
        if len(require_result) >= 1:
            self.fail("delete facedevice to frs_device error!")
    @handle_exception
    def test_facedevice_delete_error(self):
        result=self.facedevice.facedevice_delete(device_id=99999)
        self.assertEqual(result['errorinfo'],-6,'删除不存在设备返回错误码不正确')
if __name__ == "__main__":
    #unittest.main()
    # suite = unittest.makeSuite(FaceDeviceTestCase,prefix='test_facedevice_add_name_ADDDEVICE_ip_129')
    suite=unittest.TestLoader().loadTestsFromName('facedevice_test.FaceDeviceTestCase.test_facedevice_add_json_format_error')
    unittest.TextTestRunner(verbosity=2).run(suite)