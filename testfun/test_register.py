import unittest
import os
import random

import requests
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_path import CASE_DIR
from common.handle_conf import confger
from common.handle_log import my_logger

excel = HandleExcel(os.path.join(CASE_DIR, 'case.xlsx'), 'register')
case = excel.read_excel()
base_url = confger.get('evn', 'url')


@ddt
class TestRegister(unittest.TestCase):
    """注册用例类"""

    def random_phone(self):
        """生成随机手机号，用于注册"""
        phone = str(random.randint(13000000000, 18999999999))
        return phone

    @list_data(case)
    def test_register(self, item):
        """注册用例方法"""
        # 1.准备数据：预期结果，url,请求方法，请求体，请求头
        expected = eval(item['expected'])
        # 调用方法生成一个随机手机号
        phone = self.random_phone()
        # 用随机手机号替换data中的#phone#
        item['data'] = item['data'].replace('#phone#', phone)
        body = eval(item['data'])
        head = eval(confger.get('evn', 'head'))
        url = base_url + item['url']
        method = item['method'].lower()

        # 2.发送请求，获取实际结果
        response = requests.request(method, url, headers=head, json=body)
        res = response.json()

        # 3.断言、捕获异常
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            print(expected)
            print(res)
            my_logger.error('用例 【{}】 执行失败'.format(item['title']))
            my_logger.exception(e)
            raise e
        else:
            my_logger.info('用例 【{}】 执行成功'.format(item['title']))
