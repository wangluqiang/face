#coding=utf-8
import unittest
import os,time
import sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import FaceMatch
import DataBase
import DMExceptions
from handle_exception import handle_exception

class FaceMatchTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facemath=FaceMatch.FaceMath()
        cls.db=DataBase.DataBase()
        cls.items={}
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
    @handle_exception
    def test_facematch_add_name_test299_ip_129(self):
        result = self.facematch.facematch_add(m_name='test299',m_ip='129.9.9.9',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertGreater(result["errorinfo"], 0)
        self.items.setdefault('match',result)
        require_sql = "select * from frs_match where m_id="+str(result['errorinfo'])
        require_result = self.db.fetch_all(require_sql)
        if len(require_result) < 1:
            self.fail("add facematch to frs_match error!")
        else:
            self.assertEqual(require_result[0][1],"test299", "add facematch name error!")
            self.assertEqual(require_result[0][2],"129.9.9.9", "add facematch ip error!")
            self.assertEqual(require_result[0][3],9999, "add facematch port error!")
            self.assertEqual(require_result[0][5],10, "modify facematch port error!")
    @handle_exception
    def test_facematch_add_used(self):
        #添加比对服务
        result = self.facematch.facematch_add(m_name='test300',m_ip='129.9.9.10',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.items.setdefault('match',result)
        #添加名称相同的比对服务
        result=self.facematch.facematch_add(m_name='test300',m_ip='129.9.9.11',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-7)
        #添加IP和PORT相同的比对服务
        result=self.facematch.facematch_add(m_name='test302',m_ip='129.9.9.10',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-7)
    @handle_exception
    def test_facematch_add_json_format_error(self):
        #添加比对不传名称
        result=self.facematch.facematch_add(m_ip='129.9.9.12',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-650)
        #添加比对不传ip或port
        result=self.facematch.facematch_add(m_name='test304',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-650)
        result=self.facematch.facematch_add(m_name='test305',m_ip='129.9.9.14',face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-650)
        #添加比对不传检测人脸数量
        result=self.facematch.facematch_add(m_name='test306',m_ip='129.9.9.15',m_port=9999,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-650)
    @handle_exception
    def test_facematch_add_value_error(self):
        #添加比对名称为空
        result = self.facematch.facematch_add(m_name='',m_ip='129.9.9.16',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-651)
        #添加比对服务IP或PORT为空或非法字符
        result = self.facematch.facematch_add(m_name='test308',m_ip='',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-651)
        result = self.facematch.facematch_add(m_name='test310',m_ip='asdasd',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-651)
        result = self.facematch.facematch_add(m_name='test309',m_ip='129.9.9.18',m_port='',face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-651)
        result = self.facematch.facematch_add(m_name='test311',m_ip='129.9.9.22',m_port='asd',face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-651)
        #添加比对服务最大人脸数为空或非法字符
        result = self.facematch.facematch_add(m_name='test312',m_ip='129.9.9.19',m_port=9999,face_max='',client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-651)
        result = self.facematch.facematch_add(m_name='test315',m_ip='129.9.9.23',m_port=9999,face_max='das',client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-651)
        #添加比对服务最大或最小人脸像素为空或非法字符
        result = self.facematch.facematch_add(m_name='test313',m_ip='129.9.9.20',m_port=9999,face_max=10,client_max=11,min_face_pixel='',max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-651)
        result = self.facematch.facematch_add(m_name='test316',m_ip='129.9.9.24',m_port=9999,face_max=10,client_max=11,min_face_pixel='asd',max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-651)
        result = self.facematch.facematch_add(m_name='test317',m_ip='129.9.9.25',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel='')
        self.assertEqual(result['errorinfo'],-651)
        result = self.facematch.facematch_add(m_name='test318',m_ip='129.9.9.26',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel='sad')
        self.assertEqual(result['errorinfo'],-651)
    @handle_exception
    def test_facematch_add_fail(self):
        #填写名称大于64位的比对
        name='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result = self.facematch.facematch_add(m_name=name,m_ip='129.9.9.27',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertEqual(result['errorinfo'],-4)
        #填写备注信息大于64位的比对
        remark='''asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddd
        ddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd
        asddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasdddddddddddasddddddddddddddddaaaaaaaasddddddddddd'''
        result = self.facematch.facematch_add(m_name='test_319',m_ip='129.9.9.27',m_port=9999,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12,remark=remark)
        self.assertEqual(result['errorinfo'],-4)
    @handle_exception
    def test_facematch_modify_name_test2997(self):
        result_add = self.facematch.facematch_add(m_name='test299',m_ip='129.7.7.7',m_port=7777,face_max=10,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertGreater(result_add["errorinfo"], 0)
        result = self.facematch.facematch_modify('test299',result_add["errorinfo"],m_name_x='test2997',m_ip='129.7.7.7',m_port=7777,face_max=17,min_face_pixel=12,max_face_pixel=12)
        self.assertGreaterEqual(result["errorinfo"], 0)
        self.items.setdefault('match',result)
        require_sql = "select * from frs_match where m_id="+str(result_add["errorinfo"])
        require_result = self.db.fetch_all(require_sql)
        if len(require_result) < 1:
            self.fail("modify facematch to frs_match error!")
        else:
            self.assertEqual(require_result[0][1], "test2997", "modify facematch name error!")
            self.assertEqual(require_result[0][2], "129.7.7.7", "modify facematch ip error!")
            self.assertEqual(require_result[0][3], 7777, "modify facematch port error!")
            self.assertEqual(require_result[0][5], 17, "modify facematch port error!")

    @handle_exception
    def test_facematch_query_name_test2994(self):
        result_add = self.facematch.facematch_add(m_name='test2994',m_ip='124.4.4.4',m_port=4444,face_max=13,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertGreater(result_add["errorinfo"], 0)
        self.items.setdefault('match',result_add)
        result = self.facematch.facematch_query()
        self.assertEqual(result[-1]["m_name"], 'test2994')
        self.assertEqual(result[-1]["m_ip"], '124.4.4.4')
        self.assertEqual(result[-1]["m_port"], 4444)
        self.assertEqual(result[-1]["face_max"], 13)
    @handle_exception
    def test_facematch_delete_name_test2993(self):
        result_add = self.facematch.facematch_add(m_name='test2993',m_ip='123.3.3.3',m_port=3333,face_max=17,client_max=11,min_face_pixel=12,max_face_pixel=12)
        self.assertGreaterEqual(result_add["errorinfo"], 0)
        add_sql = "select * from frs_match where m_id="+str(result_add["errorinfo"])
        add_result = self.db.fetch_all(add_sql)
        self.assertGreaterEqual(len(add_result),1,"insert facematch error!")

        result = self.facematch.facematch_delete('test2993',result_add["errorinfo"])
        self.assertGreaterEqual(result["errorinfo"], 0)
        require_sql = "select * from frs_match where m_id="+str(result_add["errorinfo"])
        require_result = self.db.fetch_all(require_sql)
        if len(require_result) >= 1:
            self.fail("delete facepre to frs_collection error!")

if __name__ == "__main__":
    #unittest.main()
    #facematch_test = FaceMatchTestCase()
    #facematch_test.test_facematch_add_name_test299_ip_129()
    #facematch_test.test_facematch_modify_name_test2997()
    #facematch_test.test_facematch_query_name_test2994()
    #facematch_test.test_facematch_delete_name_test2993()
    test = unittest.TestSuite()
    test.addTest(FaceMatchTestCase("test_facematch_query_name_test2994"))
    unittest.TextTestRunner().run(test)