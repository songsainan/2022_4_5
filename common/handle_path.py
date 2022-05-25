import os

# 获取当前文件绝对路径
res = os.path.abspath(__file__)
# print(res)

# 获取当前文件所在目录路径(当前文件的上一级目录路径)
file_dir = os.path.dirname(res)
# print(file_dir)

# 获取当前文件名称
name = os.path.basename(__file__)
# print(name)

# 嵌套使用os.path.dirname()和os.path.abspath(__file__)可以获取当前项目的根目录
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_path)

# 通过os.path.join()拼接方法获取各文件夹路径
CASE_DIR = os.path.join(base_path, 'cases')
CONF_DIR = os.path.join(base_path, 'conf')
LOG_DIR = os.path.join(base_path, 'log')
REPORT_DIR = os.path.join(base_path, 'report')
TESTFUN_DIR = os.path.join(base_path, 'testfun')

# print(CONF_DIR, '\n', CASE_DIR, '\n', LOG_DIR, '\n', REPORT_DIR)
