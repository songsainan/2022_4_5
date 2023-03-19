import unittest
import os

import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_path import CASE_DIR
from common.handle_conf import confger
from common.handle_log import my_logger
from common.handle_mysql import HandleDB


@ddt
class TestRecharge(unittest.TestCase):
    """充值类"""
    excel = HandleExcel(os.path.join(CASE_DIR, 'case.xlsx'), 'recharge')
    case = excel.read_excel()
    db = HandleDB(host=confger.get('mysql', 'host'),
                  port=confger.getint('mysql', 'port'),
                  user=confger.get('mysql', 'user'),
                  password=confger.get('mysql', 'password')
                  )


    @classmethod
    def setUpClass(cls) -> None:
        """用例类的前置方法，登录提取token"""
        # 1.请求登录接口，获取响应数据
        url = confger.get('evn', 'url') + '/member/login'
        head = eval(confger.get('evn', 'head'))
        body = {
            'mobile_phone': confger.get('evn', 'mobile_phone'),
            "pwd": confger.get('evn', 'pwd')
        }
        response = requests.request(method='post', url=url, headers=head, json=body)
        res = response.json()
        # 2.从登录接口的响应数据中，提取token
        token = jsonpath(res, '$..token')[0]
        # 3.把token添加到请求头中
        head['Authorization'] = 'Bearer ' + token
        # 4.把更新后的请求头head添加为类属性，给充值接口方法调用
        cls.head = head
        # 5.提取用户id，给充值接口使用
        cls.member_id = jsonpath(res, '$..id')[0]

    @list_data(case)
    def test_recharge(self, item):
        """充值方法"""
        # 准备数据
        expected = eval(item['expected'])
        body = eval(item['data'].replace('#id#', str(self.member_id)))
        url = confger.get('evn', 'url') + item['url']
        method = item['method'].lower()

        # 发送充值请求前，查询数据库该账号余额
        sql = 'select leave_amount from future.member where mobile_phone = {}'.format(
            confger.getint('evn', 'mobile_phone'))
        start_amount = self.db.find_one(sql)[0]
        print('充值前金额是：', start_amount)

        # 发送请求,获取响应结果
        response = requests.request(method=method, headers=self.head, json=body, url=url)
        res = response.json()
        print('预期结果是：', expected)
        print('实际结果是：', res)

        # 发送充值请求后，查询数据库该账号余额
        end_amount = self.db.find_one(sql)[0]
        print('充值后金额是：', end_amount)

        # 断言
        try:
            # 判断预期结果与响应结果是否一致
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            # 判断数据库中余额的变化是否与充值金额一致（加个if语句对充值成功和充值失败分别判断）
            if res['msg'] == 'OK':
                self.assertEqual(float(end_amount - start_amount), body['amount'])
            else:
                self.assertEqual(end_amount - start_amount, 0)
        except AssertionError as e:
            my_logger.error('用例【{}】执行失败'.format(item['title']))
            my_logger.exception(e)
            raise e
        else:
            my_logger.info('用例【{}】执行成功'.format(item['title']))
