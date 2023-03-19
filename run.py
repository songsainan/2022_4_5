import unittest
import os
from unittestreport import TestRunner
from common.handle_path import TESTFUN_DIR, REPORT_DIR
from unittestreport.core.sendEmail import SendEmail

# 创建用例套件
suite = unittest.defaultTestLoader.discover(TESTFUN_DIR)

# 创建运行对象,传入套件，测试报告路径
runner = TestRunner(suite, report_dir=REPORT_DIR, title='自动化测试报告')

# 调用run方法
runner.run()

# 发送邮件
runner.send_email(host='smtp.qq.com',
                  port=465,
                  user='27000599@qq.com',
                  password='tggskgisoincbgga',
                  to_addrs=['27000599@qq.com',],
                  is_file=True)

# 扩展：自定义邮件标题、内容
# em = SendEmail(host='smtp.qq.com',
#                user='27000599@qq.com',
#                password='tggskgisoincbgga')
# em.send_email(subject='接口自动化测试报告',
#               to_addrs='27000599@qq.com',
#               content='内容',
#               filename=REPORT_DIR)
