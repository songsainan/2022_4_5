import os
from configparser import ConfigParser
from common.handle_path import CONF_DIR


# 创建一个类继承ConfigParser
class HandleConf(ConfigParser):
    # confname 为配置文件名（即绝对路径）
    def __init__(self, confname):
        super().__init__()
        self.read(confname, encoding='utf-8')


confger = HandleConf(os.path.join(CONF_DIR, 'conf.ini'))
# print(confger.get('url', 'url'))
