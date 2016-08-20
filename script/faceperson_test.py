#coding=utf-8
import unittest
import os,time
import sys
cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path+"\\..\\public")
import FacePerson
import SearchPic
import DataBase
import DMExceptions
from handle_exception import handle_exception


class FacePersonTestCase(unittest.TestCase):

    def setUp(self):
        self.faceperson = FacePerson.FacePerson()
        self.items = {}

    def tearDown(self):
        self.items = {}

    @handle_exception
    def test_faceperson_add_name_test299_cardId_test299(self):
        '''
        用例：添加人员，输入名称、性别、人脸库、卡号、备注、图片
        :return:
        '''
        result = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='test299',reg_type=1,grab_id=0,sex='0',cardId='test299',remark='test_auto')
        self.assertGreater(result["errorinfo"], 0,'add preson failed')
        self.items["person"] = result
        db = DataBase.DataBase()
        self.items["db"] = db
        require_sql = "select * from frs_person where p_id="+str(result['errorinfo'])
        facedb_query_id = "select fd_id from frs_facedb where fd_name='facedb_test'"
        facedb_id = db.fetch_all(facedb_query_id)
        require_result = db.fetch_all(require_sql)
        db.close()
        if len(require_result) < 1:
            self.fail("add person to frs_faceperson error!")
        else:
            self.assertEqual(require_result[0][1], "test299", "add faceperson name error!")
            self.assertEqual(require_result[0][3], "test299", "add cardID error!")
            self.assertEqual(require_result[0][7],facedb_id[0][0],"add facedb remark error!")
            self.assertEqual(require_result[0][8],0,"add sex remark error!")
            result_search = SearchPic.SearchPic().facepic_search(0,'zzz.jpg',1,threshold=0.9)
            self.assertEqual(result_search['return_data'][0]['p_id'],result["errorinfo"])

    @handle_exception
    def test_faceperson_add_name_test299_cardId_test299_items_full(self):
        '''
        用例：添加人员，输入名称、性别、人脸库、卡号、备注、图片、追逃编号、户籍地址、家庭住址、出生年月
        :return:
        '''
        result = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='test299_full',reg_type=1,grab_id=0,sex='0',\
                                                cardId='test299',pursuit_no="123456", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        self.assertGreater(result["errorinfo"], 0,'add preson failed')
        self.items["person"] = result
        db = DataBase.DataBase()
        self.items["db"] = db
        require_sql = "select * from frs_person where p_id="+str(result['errorinfo'])
        facedb_query_id = "select fd_id from frs_facedb where fd_name='facedb_test'"
        facedb_id = db.fetch_all(facedb_query_id)
        require_result = db.fetch_all(require_sql)
        db.close()
        if len(require_result) < 1:
            self.fail("add person to frs_faceperson error!")
        else:
            self.assertEqual(require_result[0][1], "test299_full", "add faceperson name error!")
            self.assertEqual(require_result[0][3], "test299", "add cardID error!")
            self.assertEqual(require_result[0][7],facedb_id[0][0],"add facedb remark error!")
            self.assertEqual(require_result[0][8],0,"add sex remark error!")
            self.assertEqual(require_result[0][2], "1990-01-01")
            self.assertEqual(require_result[0][4], "123456")
            self.assertEqual(require_result[0][5], "北京市朝阳区")
            self.assertEqual(require_result[0][6], "北京市朝阳区")
            self.assertEqual(require_result[0][12], "test_auto")
            result_search = SearchPic.SearchPic().facepic_search(0,'zzz.jpg',1,threshold=0.9)
            self.assertEqual(result_search['return_data'][0]['p_id'],result["errorinfo"])

    @handle_exception
    def test_faceperson_add_json_format_error(self):
        '''
        用例：添加人员，不输入姓名、性别、人脸库、卡号、图片
        :return:
        '''
        #不输入名称
        '''
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',reg_type=1,grab_id=0,sex='0',\
                                        cardId='test299',pursuit_no="123456", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        self.assertEqual(r["errorinfo"], -650)
        '''
        #不输入性别
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='no_sex_item',reg_type=1,grab_id=0,\
                                            cardId='no_sex_item',pursuit_no="no_sex_item", census_address="北京市朝阳区", \
                                            family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -650)
        #不输入人脸库
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',p_name='no_facedb',reg_type=1,grab_id=0,sex='0',\
                                            cardId='no_facedb',pursuit_no="no_facedb", census_address="北京市朝阳区", \
                                            family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        self.assertEqual(r["errorinfo"], -650)
        #不输入卡号
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='no_card',reg_type=1,grab_id=0,sex='0',\
                                            pursuit_no="no_card", census_address="北京市朝阳区", \
                                            family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
       # self.assertEqual(r["errorinfo"], -650)
        #不输入图片
        r = self.faceperson.faceperson_add(fd_name='facedb_test',p_name='no_pic',reg_type=1,grab_id=0,sex='0',\
                                           cardId='no_pic',pursuit_no="no_pic", census_address="北京市朝阳区", \
                                           family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -650)

    @handle_exception
    def test_faceperson_add_json_value_error(self):
        '''
        用例：
        添加人员，输入名称为空、整型、>64位字符串；
        性别为空、非0、1整型、字符串、>2^6；
        人脸库为不存在的ID，字符串，>2^11；
        卡号为空、整型、>32位字符串；
        追逃编号为空、整型、>32位字符串；
        户籍地址为空、整型、>256为字符串；
        家庭住址为空、整型、>256位字符串；
        remark为空、整型、>256位字符串
        :return:
        '''
        longer_64 = "1234567890123456789012345678901234567890\
                123456789012345678901234567890"
        longer_256 = "0123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890123456789"
        #输入名称为空
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='',reg_type=1,grab_id=0,sex='0',\
                                        cardId='name_empty',pursuit_no="name_empty", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入名称为整型
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name=111111,reg_type=1,grab_id=0,sex='0',\
                                        cardId='name_int',pursuit_no="name_int", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入名称为>64字符串
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name=longer_64,reg_type=1,grab_id=0,sex='0',\
                                        cardId='name_longer_64',pursuit_no="name_longer_64", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入性别为空
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='no_sex',reg_type=1,grab_id=0,sex='',\
                                        cardId='no_sex',pursuit_no="no_sex", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入性别为非0/1整数
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='sex_no_01',reg_type=1,grab_id=0,sex=100,\
                                        cardId='sex_no_01',pursuit_no="sex_no_01", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入性别为字符串
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='sex_string',reg_type=1,grab_id=0,sex="性别为字符串",\
                                        cardId='sex_string',pursuit_no="sex_string", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入性别>64
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='sex_longer_64',reg_type=1,grab_id=0,sex=65537,\
                                        cardId='sex_longer_64',pursuit_no="sex_longer_64", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入人脸库为不存在的ID
        db = DataBase.DataBase()
        require_sql = "select max(fd_id) from frs_facedb"
        result = db.fetch_all(require_sql)
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_id=result[0][0]+2,p_name='facedb_no_exists',reg_type=1,grab_id=0,sex='0',\
                                        cardId='facedb_no_exists',pursuit_no="facedb_no_exists", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入人脸库ID为字符串
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_id='facedb_test',p_name='facedb_string',reg_type=1,grab_id=0,sex='0',\
                                        cardId='facedb_string',pursuit_no="facedb_string", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入卡号为空
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='no_card',reg_type=1,grab_id=0,sex='0',\
                                        cardId='',pursuit_no="no_card", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入卡号为整型
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='card_int',reg_type=1,grab_id=0,sex='0',\
                                        cardId=12345555777,pursuit_no="card_int", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入卡号>32位字符串
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='card_longer_32',reg_type=1,grab_id=0,sex='0',\
                                        cardId=longer_64,pursuit_no="card_longer_32", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入追逃编号为空
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='persuit_empty',reg_type=1,grab_id=0,sex='0',\
                                        cardId='persuit_empty',pursuit_no="", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入追逃编号为整型
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='persuit_int',reg_type=1,grab_id=0,sex='0',\
                                        cardId='persuit_int',pursuit_no=112233, census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入追逃编号为>32位字符串
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='persuit_longer_32',reg_type=1,grab_id=0,sex='0',\
                                        cardId='persuit_longer_32',pursuit_no=longer_64, census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        print(r)
        #self.assertEqual(r["errorinfo"], -651)
        #输入户籍地址为空
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='census_no',reg_type=1,grab_id=0,sex='0',\
                                        cardId='census_no',pursuit_no="census_no", census_address="", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入户籍地址为整型
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='census_int',reg_type=1,grab_id=0,sex='0',\
                                        cardId='census_int',pursuit_no="census_int", census_address=111222, \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入户籍地址为>256位字符串
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='census_longer256',reg_type=1,grab_id=0,sex='0',\
                                        cardId='census_longer256',pursuit_no="census_longer256", census_address=longer_256, \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入家庭住址为空
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='family_no',reg_type=1,grab_id=0,sex='0',\
                                        cardId='family_no',pursuit_no="family_no", census_address="北京市朝阳区", \
                                        family_address="", birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入家庭住址为整型
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='family_int',reg_type=1,grab_id=0,sex='0',\
                                        cardId='family_int',pursuit_no="family_int", census_address="北京市朝阳区", \
                                        family_address=121212, birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入家庭住址为>256
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='family_longer_256',reg_type=1,grab_id=0,sex='0',\
                                        cardId='family_longer_256',pursuit_no="family_longer_256", census_address="北京市朝阳区", \
                                        family_address=longer_256, birth_date="1990-01-01", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入备注为整型
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='remark_int',reg_type=1,grab_id=0,sex='0',\
                                        cardId='remark_int',pursuit_no="remark_int", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark=14567)
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入备注为>256位字符串
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='remark_longer_256',reg_type=1,grab_id=0,sex='0',\
                                        cardId='remark_longer_256',pursuit_no="remark_longer_256", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1990-01-01", remark=longer_256)
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入出生日期不符合格式
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='birth_date_error',reg_type=1,grab_id=0,sex='0',\
                                        cardId='birth_date_error',pursuit_no="birth_date_error", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="1900.1.1", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入出生日期为空
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='birth_date_no',reg_type=1,grab_id=0,sex='0',\
                                        cardId='birth_date_no',pursuit_no="birth_date_no", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)
        #输入出生日期>10位
        r = self.faceperson.faceperson_add(pic_name='zzz.jpg',fd_name='facedb_test',p_name='birth_date_longer_10',reg_type=1,grab_id=0,sex='0',\
                                        cardId='birth_date_longer_10',pursuit_no="birth_date_longer_10", census_address="北京市朝阳区", \
                                        family_address="北京市朝阳区", birth_date="12345678901234", remark='test_auto')
        #self.assertEqual(r["errorinfo"], -651)
        print(r)

    @handle_exception
    def test_faceperson_add_pic_noface(self):
        r = self.faceperson.faceperson_add(fd_name="facedb_test", pic_name="car.jpg", p_name="no_face",reg_type=1,\
                                           grab_id=0, sex=0, cardId="123123123123")
        self.assertEqual(r["errorinfo"], -250)

    @handle_exception
    def test_faceperson_add_cardID_persuit_used(self):
        '''
        用例:添加人员时，输入已存在的卡号、追逃编号
        :return:
        '''
        #先添加某个人员
        result = self.faceperson.faceperson_add(fd_name="facedb_test", pic_name="zzz.jpg", p_name="cardid_persuit_used", \
                                                reg_type=1, grad_id=0, sex=0, cardId="basic_used", pursuit_no="basic_used")
        self.items["person"] = result
        #添加cardID重复的人员
        r = self.faceperson.faceperson_add(fd_name="facedb_test", pic_name="zzz.jpg", p_name="cardid_persuit_used", \
                                            reg_type=1, grad_id=0, sex=0, cardId="basic_used", pursuit_no="new")
        self.assertEqual(r["errorinfo"], -7)
        #添加追逃编号重复的人员
        r = self.faceperson.faceperson_add(fd_name="facedb_test", pic_name="zzz.jpg", p_name="cardid_persuit_used", \
                                            reg_type=1, grad_id=0, sex=0, cardId="new", pursuit_no="basic_used")
        self.assertEqual(r["errorinfo"], -7)

    @handle_exception
    def test_faceperson_modify_name_test299_cardId_test2999(self):
        '''
        用例:修改人员信息
        :return:
        '''
        result_add = self.faceperson.faceperson_add(p_name='test299',reg_type=1,grab_id=0,sex='0',cardId='test299',pic_name='zzz.jpg',fd_name='facedb_test',remark='test_auto')
        self.assertGreater(result_add["errorinfo"], 0, 'add preson fail')
        self.items["person"] = result_add
        result = self.faceperson.faceperson_modify(p_id=result_add["errorinfo"], p_name="change_test299", sex=None, cardId="change_test299",\
                                                   fd_name=None, remark=None)
        self.assertGreaterEqual(result["errorinfo"], 0)
        db = DataBase.DataBase()
        require_sql = "select * from frs_person where p_name='change_test299'"
        #print(require_sql)
        require_result = db.fetch_all(require_sql)
        db.close()
        #print(require_result)
        if len(require_result) < 1:
            self.fail("modify person to frs_faceperson error!")
        else:
            self.assertEqual(require_result[0][1], "change_test299", "modify faceperson name error!")
            self.assertEqual(require_result[0][3], "change_test299", "modify cardID threshold error!")
            result_search = SearchPic.SearchPic().facepic_search(0,'zzz.jpg',1,threshold=0.9)
            self.assertEqual(result_search['return_data'][0]['p_name'],'change_test299','preson match error!')

    @handle_exception
    def test_faceperson_modify_json_format_error(self):
        '''
        用例：修改人员信息，不输入名称、性别、卡号、人脸库
        :return:
        '''
        #新建人员
        result = self.faceperson.faceperson_add(p_name='test_json_format',reg_type=1,grab_id=0,sex='0',cardId='test299',pic_name='zzz.jpg',fd_name='facedb_test',remark='test_auto')
        self.items["person"] = result
        #不输入名称
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], sex=None, cardId=None, fd_name=None, remark=None)
        #self.assertEqual(r["errorinfo"], -650)
        #不输入性别
        #r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name=None, cardId=None, fd_name=None, remark=None)
        #self.assertEqual(r["errorinfo"], -650)
        #不输入卡号
        #r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name=None, sex=None, fd_name=None, remark=None)
        #self.assertEqual(r["errorinfo"], -650)
        #不输入人脸库
        #r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name=None, cardId=None, sex=None, remark=None)
        #self.assertEqual(r["errorinfo"], -650)
        #不输入备注
        #r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name=None, cardId=None, sex=None, fd_name=None)
        #self.assertEqual(r["errorinfo"], -650)

    @handle_exception
    def test_faceperson_modify_json_value_error(self):
        '''
        用例：修改人员，
        输入名称为空、整型、>64位字符串；
        性别为空、非0、1整型、字符串、>2^6；
        人脸库为不存在的ID，字符串，>2^11；
        卡号为空、整型、>32位字符串；
        追逃编号为空、整型、>32位字符串；
        户籍地址为空、整型、>256为字符串；
        家庭住址为空、整型、>256位字符串；
        remark为空、整型、>256位字符串；
        出生日期为空、出生日期格式不符合要求；出生日期>10位字符串
        :return:
        '''
        #创建基准人员
        result = self.faceperson.faceperson_add(p_name='test_json_value',reg_type=1,grab_id=0,sex=0,\
                                                cardId='test_json_value',pic_name='zzz.jpg',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        self.items["person"] = result
        longer_64 = "1234567890123456789012345678901234567890\
                    1234567890123456789012345678901234567890"
        longer_256 = "0123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890\
                  123456789012345678901234567890123456789"
        #输入名称为空
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #修改名称为整型
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name=12121221221,sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入名称>64位字符串
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name=longer_64,sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入性别为空
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex="",\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入性别为非0 1 数字
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=10,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入性别为字符串
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex="性别为字符串",\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入性别>2^6
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=1000,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入人脸库为不存在ID
        db = DataBase.DataBase()
        self.items["db"] = db
        require_sql = "select max(fd_id) from frs_facedb"
        result_db = db.fetch_all(require_sql)
        d = result_db[0][0]+2
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_id=d,\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入人脸库为字符串
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_id='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入卡号为空
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入卡号为整型
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId=121211212121,fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入卡号为>32位字符串
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId=longer_64,fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入追逃编号为整型
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no=1111111, census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入追逃编号为>32位字符串
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId=longer_64,fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入户籍地址为整型
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address=123123123, \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入户籍地址为>256位字符串
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address=longer_256, \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入家庭住址为整型
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address=22233334444, birth_date="1990-1-1")
        print(r)
        #输入家庭住址为>256位字符串
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address=longer_256, birth_date="1990-1-1")
        print(r)
        #输入备注为整型
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark=111111,pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #输入备注>256位字符串
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark=longer_256,pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990-1-1")
        print(r)
        #出生日期格式不符合要求
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="1990.1.1")
        print(r)
        #出生日期>10位字符串
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_json_value',sex=0,\
                                                cardId='test_json_value',fd_name='facedb_test',\
                                                remark='test_auto',pursuit_no="test_json_value", census_address="北京市朝阳区", \
                                                family_address="北京市朝阳区", birth_date="123456789012345")
        print(r)

    @handle_exception
    def test_faceperson_modify_pic_noface(self):
        '''
        用例：修改人员图片无人脸
        :return:
        '''
        #创建人员
        result = self.faceperson.faceperson_add(p_name='test_modify_noface',reg_type=1,grab_id=0,sex='0',cardId='test_modify_noface',pic_name='zzz.jpg',fd_name='facedb_test',remark='test_auto')
        self.items["person"] = result
        #修改人员图片为无人脸
        r = self.faceperson.faceperson_modify(p_id=result["errorinfo"], p_name='test_modify_noface',sex='0',cardId='test_modify_noface',pic_name='car.jpg',fd_name='facedb_test',remark='test_auto')
        #self.assertEqual(r["errorinfo"], -250)

    @handle_exception
    def test_faceperson_modify_cardid_persuit_used(self):
        '''
        用例：修改人员卡号、追逃编号重复
        :return:
        '''
        #创建两个人员
        result1 = self.faceperson.faceperson_add(p_name='test_card_used',reg_type=1,grab_id=0,sex='0',cardId='test_card_used',pic_name='zzz.jpg',\
                                                 fd_name='facedb_test',remark='test_auto', persuit_no="test_persuit_used")
        result2 = self.faceperson.faceperson_add(p_name='test_card_used2',reg_type=1,grab_id=0,sex='0',cardId='test_card_used2',pic_name='zzz.jpg',\
                                                 fd_name='facedb_test',remark='test_auto', persuit_no="test_persuit_used2")
        self.items["person"] = [result1,result2]
        #修改人员卡号重复
        r = self.faceperson.faceperson_add(p_name='test_card_used2',reg_type=1,grab_id=0,sex='0',cardId='test_card_used',pic_name='zzz.jpg',\
                                                 fd_name='facedb_test',remark='test_auto', persuit_no="test_persuit_used2")
        self.assertEqual(r["errorinfo"], -7)
        #修改人员追逃编号重复
        r = self.faceperson.faceperson_add(p_name='test_card_used2',reg_type=1,grab_id=0,sex='0',cardId='test_card_used2',pic_name='zzz.jpg',\
                                                 fd_name='facedb_test',remark='test_auto', persuit_no="test_persuit_used")
        self.assertEqual(r["errorinfo"], -7)

    @handle_exception
    def test_faceperson_delete_name_test299(self):
        '''
        用例：删除人员
        '''
        result_add = self.faceperson.faceperson_add(p_name='test299',reg_type=1,grab_id=0,sex='0',cardId='test299',pic_name='zzz.jpg',fd_name='facedb_test',remark='test_auto')
        self.assertGreater(result_add["errorinfo"], 0, 'add preson fail')
        result_search = SearchPic.SearchPic().facepic_search(0,'zzz.jpg',1,threshold=0.9)
        self.assertEqual(result_search['return_data'][0]['p_id'],result_add["errorinfo"])
        result = self.faceperson.faceperson_delete(p_id=result_add["errorinfo"])
        self.assertGreaterEqual(result["errorinfo"], 0, 'delete person fail')
        db = DataBase.DataBase()
        require_sql = "select * from frs_person where p_id="+str(result_add["errorinfo"])
        #print(require_sql)
        require_result = db.fetch_all(require_sql)
        db.close()
        #print(require_result)
        self.assertEqual(len(require_result), 0, 'delete person fail')
        result_search = SearchPic.SearchPic().facepic_search(0,'zzz.jpg',1,threshold=0.95)
        self.assertEqual(result_search['return_data'], [], 'delete person fail')

    @handle_exception
    def test_faceperson_delete_json_format_error(self):
        '''
        用例：删除人员时，不传入人员ID
        :return:
        '''
        r = self.faceperson.faceperson_delete()
        self.assertEqual(r["errorinfo"], -650)

    @handle_exception
    def test_faceperson_delete_no_faceid(self):
        '''
        用例：删除人员时，传入人员ID不存在、人员ID为字符串
        :return:
        '''
        db = DataBase.DataBase()
        self.items["db"] = db
        query_sql = "select max(p_id) from frs_person"
        result = db.fetch_all(query_sql)
        #删除人员ID不存在
        r = self.faceperson.faceperson_delete(p_id=result[0][0]+2)
        self.assertEqual(r["errorinfo"], -6)
        #删除人员ID为字符串
        r = self.faceperson.faceperson_delete(p_id="人员ID为字符串")
        self.assertEqual(r["errorinfo"], -6)

    @handle_exception
    def test_faceperson_query_name_test2991(self):
        result_add = self.faceperson.faceperson_add(p_name='test2991',reg_type=1,grab_id=0,sex='0',cardId='test2991',pic_name='zzz.jpg',fd_name='facedb_test',remark='test_auto')
        self.assertGreater(result_add['errorinfo'], 0, 'add person fail')
        self.items["person"] = result_add
        result_query = self.faceperson.faceperson_query(p_name='test2991')
        #print(result_query)
        self.assertGreaterEqual(result_query[0]["p_name"],'test2991')
        self.assertGreaterEqual(result_query[0]["cardId"],'test2991')
        self.assertGreaterEqual(result_query[0]["fd_id"],1)
        self.assertGreaterEqual(result_query[0]["sex"],0)
        result_del = self.faceperson.faceperson_delete('test2991',result_add['errorinfo'])
        self.assertGreaterEqual(result_del['errorinfo'], 0, 'delete person fail')


if __name__ == "__main__":
    # unittest.main()
    r_suite = unittest.TestSuite()
    r_suite.addTest(FacePersonTestCase('test_faceperson_modify_json_value_error'))
    unittest.TextTestRunner().run(r_suite)
