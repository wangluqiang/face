#coding=utf-8
import unittest
import os
import sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import FacePre
import DataBase
import DMExceptions
from handle_exception import handle_exception
class FacePreTestCase(unittest.TestCase):
    '''
    功能：对于预处理服务增、删、改、查的封装
    '''

    @classmethod
    def setUpClass(cls):
        #初始化测试环境
        cls.facepre=FacePre.FacePre()
        cls.db=DataBase.DataBase()
        cls.items={}
    @classmethod
    def tearDownClass(cls):
        #清理环境
        cls.db.close()
    @handle_exception
    def test_facepre_add_name_test2999_ip_129(self):
        #测试添加预处理功能
        result = self.facepre.facepre_add(p_name='test2999',p_ip='129.9.9.9',p_port=9999,m_name='match_test',frame_interval=222)
        self.assertGreater(result["errorinfo"],0)
        self.items.setdefault('preprocess',result)
        require_sql = "select * from frs_collection where p_id="+str(result['errorinfo'])
        require_result = self.db.fetch_all(require_sql)
        if len(require_result) < 1:
            self.fail("add facepre to frs_collection error!")
        else:
            self.assertEqual(require_result[0][1], "test2999", "add facepre name error!")
            self.assertEqual(require_result[0][2], '129.9.9.9', "add facepre ip error!")
            self.assertEqual(require_result[0][3],9999,"add facepre port error!")
            self.assertGreaterEqual(require_result[0][4],1,"add facepre m_id error!")
            self.assertEqual(require_result[0][5],222,"add facepre frame_interval error!")

    @handle_exception
    def test_facepre_add_used(self):
        #添加一个预处理
        result_add=self.facepre.facepre_add(p_name='test3000',p_ip='129.9.9.10',p_port=10000,m_name='match_test',frame_interval=222)
        self.items.setdefault('preprocess',result_add['errorinfo'])
        #添加一个名称相同的预处理
        result_add_used1=self.facepre.facepre_add(p_name='test3000',p_ip='129.9.9.11',p_port=10000,m_name='match_test',frame_interval=222)
        self.assertEqual(result_add_used1['errorinfo'],-7)
        #添加一个IP和PORT相同的预处理
        result_add_used2=self.facepre.facepre_add(p_name='test3001',p_ip='129.9.9.10',p_port=10000,m_name='match_test',frame_interval=222)
        self.assertEqual(result_add_used2['errorinfo'],-7)
    @handle_exception
    def test_facepre_add_json_format_error(self):
        #添加预处理不输入名称
        restlt=self.facepre.facepre_add(p_ip='129.9.9.12',p_port=10000,m_name='match_test',frame_interval=222)
        self.assertEqual(restlt['errorinfo'],-650)
        #添加预处理不输入ip或port
        result=self.facepre.facepre_add(p_name='test3002',p_port=10000,m_name='match_test',frame_interval=222)
        self.assertEqual(restlt['errorinfo'],-650)
        result=self.facepre.facepre_add(p_name='test3003',p_ip='129.9.9.13',m_name='match_test',frame_interval=222)
        self.assertEqual(result['errorinfo'],-650)
        #添加预处理不输入抓拍间隔
        result=self.facepre.facepre_add(p_name='test3004',p_ip='129.9.9.14',p_port=10000,m_name='match_test')
        self.assertEqual(restlt['errorinfo'],-650)
    @handle_exception
    def test_facepre_add_value_error(self):
        #添加预处理名称为空
        result_add=self.facepre.facepre_add(p_name='',p_ip='129.9.9.15',p_port=10000,m_name='match_test',frame_interval=222)
        self.assertEqual(result_add['errorinfo'],-651)
        #添加预处理IP或PORT为空或非法类型
        result_add=self.facepre.facepre_add(p_name='test3001',p_ip='',p_port=10000,m_name='match_test',frame_interval=222)
        self.assertEqual(result_add['errorinfo'],-651)
        result_add=self.facepre.facepre_add(p_name='test3002',p_ip='ip',p_port=10000,m_name='match_test',frame_interval=222)
        self.assertEqual(result_add['errorinfo'],-651)
        result_add=self.facepre.facepre_add(p_name='test3003',p_ip='129.9.9.16',p_port='',m_name='match_test',frame_interval=222)
        self.assertEqual(result_add['errorinfo'],-651)
        result_add=self.facepre.facepre_add(p_name='test3004',p_ip='129.9.9.17',p_port='port',m_name='match_test',frame_interval=222)
        self.assertEqual(result_add['errorinfo'],-651)
        #添加预处理抓拍间隔为空或非法类型
        result_add=self.facepre.facepre_add(p_name='test3005',p_ip='129.9.9.18',p_port=10000,m_name='match_test',frame_interval='')
        self.assertEqual(result_add['errorinfo'],-651)
        result_add=self.facepre.facepre_add(p_name='test3006',p_ip='129.9.9.19',p_port=10000,m_name='match_test',frame_interval='frame_interval')
        self.assertEqual(result_add['errorinfo'],-651)
    @handle_exception
    def test_facepre_add_fail(self):
        #添加名称为大于32位的预处理
        name='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result_add=self.facepre.facepre_add(p_name=name,p_ip='129.9.9.20',p_port=10000,m_name='match_test',frame_interval=222)
        self.assertEqual(result_add['errorinfo'],-4)
        #添加备注大于32位的预处理
        name='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result_add=self.facepre.facepre_add(p_name='test_3007',p_ip='129.9.9.20',p_port=10000,m_name='match_test',frame_interval=222,remark=name)
        self.assertEqual(result_add['errorinfo'],-4)

    @handle_exception
    def test_facepre_modify_name_test2997_interval_224(self):
        #测试修改预处理功能
        result_add = self.facepre.facepre_add(p_name='test299',p_ip='129.9.9.7',p_port=7777,m_name='match_test',frame_interval=222)
        self.assertGreaterEqual(result_add["errorinfo"],0)
        result = self.facepre.facepre_modify('test299',result_add["errorinfo"],p_name_x='test2997',p_ip='129.9.9.7',p_port=7777,frame_interval=224)
        self.assertGreaterEqual(result["errorinfo"],0)
        self.items.setdefault('preprocess',result)
        require_sql = "select * from frs_collection where p_id="+str(result_add["errorinfo"])
        require_result = self.db.fetch_all(require_sql)
        if len(require_result) < 1:
            self.fail("modify facepre to frs_collection error!")
        else:
            self.assertEqual(require_result[0][1],"test2997", "modify facepre name error!")
            self.assertEqual(require_result[0][2],'129.9.9.7', "modify facepre ip error!")
            self.assertEqual(require_result[0][3],7777,"modify facepre port error!")
            #self.assertEqual(require_result[0][4],77,"modify facepre m_id error!")
            self.assertEqual(require_result[0][5],224,"modify facepre frame_interval error!")

    @handle_exception
    def test_facepre_query_name_test2996(self):
        #测试查询预处理功能
        result_add = self.facepre.facepre_add(p_name='test2996',p_ip='127.7.7.7',p_port=5555,m_name='match_test',frame_interval=155)
        self.assertGreaterEqual(result_add["errorinfo"],0)
        self.items.setdefault('preprocess',result_add)
        result = self.facepre.facepre_query()
        self.assertEqual(result[-1]["p_name"],'test2996')
        self.assertEqual(result[-1]["p_ip"],'127.7.7.7')
        self.assertEqual(result[-1]["p_port"],5555)
        self.assertEqual(result[-1]["frame_interval"],155)

    @handle_exception
    def test_facepre_delete_name_test2994(self):
        result_add = self.facepre.facepre_add(p_name='test2994',p_ip='129.5.5.5',p_port=4444,m_name='match_test',frame_interval=144)
        self.assertGreaterEqual(result_add["errorinfo"],0)
        result_add_sql = "select * from frs_collection where p_id="+str(result_add["errorinfo"])
        result_add_mum = self.db.fetch_all(result_add_sql)
        self.assertEqual(len(result_add_mum),1)
        result = self.facepre.facepre_delete('test2994',result_add["errorinfo"])
        self.assertGreaterEqual(result["errorinfo"],0)
        require_sql = "select * from frs_collection where p_id="+str(result_add["errorinfo"])
        require_result = self.db.fetch_all(require_sql)
        self.db.close()
        #print(require_result)
        if len(require_result) >= 1:
            self.fail("delete facepre to frs_collection error!")

if __name__ == "__main__":
    #unittest.main()
    #facepre_test = FacePreTestCase()
    #facepre_test.test_facepre_add_name_test2999_ip_129()
    #facepre_test.test_facepre_modify_name_test2997_interval_224()
    #facepre_test.test_facepre_query_name_test2996()
    #facepre_test.test_facepre_delete_name_test2994()
    suite = unittest.TestSuite()
    suite.addTest(FacePreTestCase("test_facepre_query_name_test2996"))
    unittest.TextTestRunner().run(suite)