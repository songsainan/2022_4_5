import re


def replace_data(cls, data):
    """

    :param cls: 测试类，主要是为了获取类属性
    :param data: 需要被替换的数据，里面被替换的字符需要与类属性名保持一致
    :return:
    """
    while re.search('#(.+?)#', data):
        res = re.search('#(.+?)#', data)
        param = res.group()
        attr = res.group(1)
        value = getattr(cls, attr)
        data = data.replace(param, str(value))

    return data


if __name__ == '__main__':
    class Demo:
        id = 1
        name = 'li'
        age = 13
        data = 'niubi'


    case = '{"id":#id#,"name":#name#,"age":#age#,"data":#data#}'

    res = replace_data(Demo, case)
    print(res)
