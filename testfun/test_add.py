import unittest
import os

import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_path import CASE_DIR
from common.handle_conf import confger
from common.handle_log import my_logger
from common.replace_data import replace_data
from common.handle_mysql import HandleDB


@ddt
class TestAdd(unittest.TestCase):
    excel = HandleExcel(os.path.join(CASE_DIR, 'case.xlsx'), 'add')
    case = excel.read_excel()
    db = HandleDB(host=confger.get('mysql', 'host'),
                  user=confger.get('mysql', 'user'),
                  port=confger.getint('mysql', 'port'),
                  password=confger.get('mysql', 'password'))

    @classmethod
    def setUpClass(cls) -> None:
        """
        添加项目需要先登录
        :return:
        """
        url = 'http://api.lemonban.com/futureloan/member/login'
        head = eval(confger.get('evn', 'head'))
        body = {"mobile_phone": confger.getint('evn', 'mobile_phone'),
                "pwd": confger.getint('evn', 'pwd')}
        response = requests.request(method='post', url=url, headers=head, json=body)
        res = response.json()
        # 提取token更新到请求头，设置为类属性
        token = jsonpath(res, '$..token')[0]
        head['Authorization'] = 'Bearer ' + token
        cls.head = head
        # 提取用户id设置为类属性
        cls.member_id = jsonpath(res, '$..id')[0]

    @list_data(case)
    def test_add(self, item):
        expected = eval(item['expected'])
        url = confger.get('evn', 'url') + item['url']
        # .lower()方法可以将字符串全部转为小写
        method = item['method'].lower()
        # 替换数据
        body = eval(replace_data(TestAdd, item['data']))
        # 请求前查询数据库
        sql = 'select count(*) from future.loan where member_id={}'.format(self.member_id)
        start_num = self.db.find_one(sql)[0]
        print('请求前的项目数是：', start_num)

        response = requests.request(method=method, url=url, headers=self.head, json=body)
        res = response.json()
        # 请求后查询数据库
        end_num = self.db.find_one(sql)[0]
        print('请求后的项目数是：', end_num)
        # 计算前后项目数的差
        add_num = end_num-start_num

        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            if res['msg'] == 'OK':
                self.assertEqual(add_num, 1)
        except AssertionError as e:
            my_logger.error('用例【{}】执行失败'.format(item['title']))
            my_logger.exception(e)
            print(res)
            raise e
        else:
            my_logger.info('用例【{}】执行成功'.format(item['title']))
