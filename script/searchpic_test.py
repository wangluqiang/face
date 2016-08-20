#coding=utf-8
import unittest
import os
import sys
sys.path.append("..\\public")
import SearchPic
import FacePerson
import DataBase
from handle_exception import handle_exception
from Base import get_max_id

class SearchPicTestCase(unittest.TestCase):

    def setUp(self):
        self.searchpic = SearchPic.SearchPic()
        self.faceperson=FacePerson.FacePerson()
        self.items = {}

    def teardown(self):
        pass

    @handle_exception
    def test_searchpic(self):
        result_person=self.faceperson.faceperson_add(p_name='test_zzz',reg_type=1,grab_id=0,sex='0',cardId='9999',pic_name='zzz.jpg',fd_name='facedb_test',remark='test_auto')
        self.assertGreater(result_person["errorinfo"],0)
        self.items["person"] = result_person
        result = self.searchpic.facepic_search(pic_name='zzz.jpg', fd_name="facedb_test", return_num=1, threshold=0.8)
        self.assertEqual(result['return_data'][0]['p_id'],result_person["errorinfo"])
        self.assertEqual(result['return_data'][0]['p_name'],'test_zzz')

    @handle_exception
    def test_searchpic_noresult(self):
        result = self.searchpic.facepic_search(pic_name='zzz.jpg', fd_name="facedb_test", return_num=1, threshold=1)
        print(result)

    @handle_exception
    def test_searchpic_json_format_error(self):
        '''
        用例：json串格式错误：不输入图片，相似度，返回值
        :return:
        '''
        #不输入图片
        r = self.searchpic.facepic_search(fd_name="facedb_test", threshold=0.4, return_num=12)
        print(r)
        #不输入相似度
        r = self.searchpic.facepic_search(pic_name="5.jpg", return_num=12)
        print(r)
        #不输入返回值 1120版本，比对挂起
        #r = self.searchpic.facepic_search(pic_name="5.jpg", threshold=0.5)

    @handle_exception
    def test_searchpic_json_value_error(self):
        '''
        用例：姓名输入>64位字符串；
            人脸库输入为字符串；
            相似度输入<0，>1，字符串，“”；
            返回值=0，<0，字符串，“”；
            图片为字符串，“”
        :return:
        '''
        #输入名称>64位字符串
        longer_64 = "1234567890123456789012345678901234567890\
                    1234567890123456789012345678901234567890"
        r = self.searchpic.facepic_search(pic_name="5.jpg", fd_name="facedb_test", p_name=longer_64,\
                return_num=12, threshold=0.6)
        print(r)
        #输入人脸库ID为字符串
        r = self.searchpic.facepic_search(pic_name="5.jpg", fd_id="人脸库为字符串" , return_num=12, threshold=0.6)
        print(r)
        #输入相似度<0
        r = self.searchpic.facepic_search(pic_name="5.jpg", fd_name="facedb_test",  return_num=12, threshold=-100)
        print(r)
        #输入相似度>1
        r = self.searchpic.facepic_search(pic_name="5.jpg", fd_name="facedb_test",  return_num=12, threshold=100)
        print(r)
        #输入相似度为字符串
        r = self.searchpic.facepic_search(pic_name="5.jpg", fd_name="facedb_test",  return_num=12, threshold="相似度为字符串")
        print(r)
        #输入相似度为空
        r = self.searchpic.facepic_search(pic_name="5.jpg", fd_name="facedb_test",  return_num=12, threshold="")
        print(r)
        #返回值  由于1120版本，返回值会导致比对挂起，所以先不写该脚本
        #图片为字符串
        #r = self.searchpic.facepic_search(pic_name="图片为字符串", fd_name="facedb_test",  return_num=12, threshold=0.5)
        #print(r)
        #图片为空
        #r = self.searchpic.facepic_search(pic_name="", fd_name="facedb_test",  return_num=12, threshold=0.5)
        #print(r)

    @handle_exception
    def test_searchpic_facedb_no_exist(self):
        '''
        用例：人脸图像检索时，输入不存在的人脸库
        :return:
        '''
        max_id = get_max_id(ip=self.searchpic.db_ip, port=self.searchpic.db_port, name=self.searchpic.db_name, \
                                    user=self.searchpic.db_user, passwd=self.searchpic.db_passwd)
        r = self.searchpic.facepic_search(pic_name="5.jpg", fd_id=max_id+2,  return_num=12, threshold=0.5)
        print(r)

    @handle_exception
    def test_searchpic_pic_noface(self):
        '''
        用例：输入不存在人脸的图片
        :return:
        '''
        r = self.searchpic.facepic_search(pic_name="car.jpg", fd_name="facedb_test",  return_num=12, threshold=0.5)
        print(r)

if __name__ == "__main__":
    #unittest.main()
    r_suite = unittest.TestSuite()
    r_suite.addTest(SearchPicTestCase('test_searchpic_facedb_no_exist'))
    unittest.TextTestRunner().run(r_suite)
