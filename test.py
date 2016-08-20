#coding=utf-8
__author__ = 'rjxy'
import unittest,HTMLTestRunner
from Study_unittest import *
if __name__ == '__main__':
    test=unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    # suit=unittest.TestSuite()
    fb=open(r'C:\Users\rjxy\Desktop\frs_dm\123.txt','w')
    unittest.TextTestRunner(stream=fb,verbosity=2).run(test)
    # fb=open(r'C:\Users\rjxy\Desktop\frs_dm\123.txt','wb')
    # result=unittest.TextTestResult(stream=fb,descriptions='学习',verbosity=1024)
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fb,title="学习",description="")
    # result.addSuccess(MyTestCase)
    # result.startTest(test)
    # runner.run(test)
