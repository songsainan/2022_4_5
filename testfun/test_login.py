import unittest
import os

import requests

from common.handle_excel import HandleExcel
from unittestreport import ddt, list_data
from common.handle_path import CASE_DIR
from common.handle_conf import confger
from common.handle_log import my_logger


@ddt
class TestLogin(unittest.TestCase):
    """登录用例类"""
    # 创建工作簿，读取用例
    excel = HandleExcel(os.path.join(CASE_DIR, 'case.xlsx'), 'login')
    case = excel.read_excel()

    @list_data(case)
    def test_login(self, item):
        """登录用例方法"""
        # 准备测试数据
        expected = eval(item['expected'])
        head = eval(confger.get('evn', 'head'))
        body = eval(item['data'])
        url = confger.get('evn', 'url') + item['url']
        method = item['method'].lower()
        # 发送请求，获取结果
        response = requests.request(method=method, url=url, headers=head, json=body)
        res = response.json()
        # 断言，捕获异常
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            print(expected)
            print(res)
            my_logger.error('用例【{}】执行失败'.format(item['title']))
            my_logger.exception(e)
            raise e
        else:
            my_logger.info('用例【{}】执行成功'.format(item['title']))
