#coding=utf-8
__author__ = 'rjxy'

import unittest,HTMLTestRunner
import time,sys

def sum(a,b):
    return a+b

class MyTestCase(unittest.TestCase):
    '''学习'''
    @classmethod
    def setUpClass(cls):
        cls.a=1
        cls.b=2
        print('初始化%s+%s'%(cls.a,cls.b))
    @classmethod
    def tearDownClass(cls):
        # time.sleep(10)
        print('结束')
    # def setUp(self):
    #     print('初始化')
    # def tearDown(self):
    #     print('结束')
    def test_sum(self):
        try:
            3/0
            self.assertEqual(3,sum(self.a,self.b),'!=')
        except Exception:
            print(123123123)

    def test_sum1(self):
        self.assertEqual(4,sum(2,3),'!=')

if __name__ == '__main__':
    pass
    ################################################
    # suit=unittest.TestSuite()
    # print(suit)
    # suit.addTest(MyTestCase('test_sum'))
    # print(suit)
    # print(getattr(MyTestCase,'sss',None))
    # unittest.TextTestRunner(verbosity=2).run(suit)
    ################################################
    # suit1=unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    # print(suit1)
    # unittest.TextTestRunner(verbosity=2).run(suit1)
    ################################################
    # test=unittest.makeSuite(MyTestCase,prefix='test_sum1')
    # print(test)
    # unittest.TextTestRunner(verbosity=2).run(test)
    ###############################################
    suite=unittest.TestLoader().loadTestsFromName('Study_unittest.MyTestCase.test_sum1')
    # suite=unittest.defaultTestLoader.loadTestsFromModule(MyTestCase())
    unittest.TextTestRunner(verbosity=2).run(suite)
    # fb=open(r'C:\Users\rjxy\Desktop\frs_dm\123.html','wb')
    # result=unittest.TextTestResult(stream=fb,descriptions='',verbosity=2)
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fb,title="学习",description="")
    # result.addSuccess(MyTestCase)
    # result.startTest(MyTestCase)
    # runner.run(tests)



