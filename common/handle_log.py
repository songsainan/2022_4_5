import logging
import os
from common.handle_path import LOG_DIR
from common.handle_conf import confger


# 定义方法，创建一个日志收集器
def create_logger(logger_name='my_logger', logger_level='INFO', logfile_name='test.log',
                  sh_level='INFO', fh_level='INFO'):
    # 一、创建收集器logger，传入收集器名字
    logger = logging.getLogger(logger_name)

    # 二、设置收集器收集等级
    logger.setLevel(logger_level)

    # 三、创建日志输出渠道
    # 1.输出渠道为控制台
    sh = logging.StreamHandler()
    # 2.输出渠道为日志文件，需要传入日志文件名，和文件编码格式
    fh = logging.FileHandler(logfile_name, encoding='utf-8')

    # 四、设置日志输出渠道的输出等级
    sh.setLevel(sh_level)
    fh.setLevel(fh_level)

    # 五、绑定日志收集器和输出渠道
    logger.addHandler(sh)
    logger.addHandler(fh)

    # 六、创建日志输出格式（想要什么格式可以自定义，网上有模板）
    log_format = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')

    # 七、将输出格式设置到对应的输出渠道
    sh.setFormatter(log_format)
    fh.setFormatter(log_format)

    # 八、返回日志收集器logger
    return logger


# 为方便后期调用,直接创建一个对象
my_logger = create_logger(
    logger_name=confger.get('logging', 'logger_name'),
    logger_level=confger.get('logging', 'logger_level'),
    logfile_name=os.path.join(LOG_DIR, confger.get('logging', 'logfile_name')),
    sh_level=confger.get('logging','sh_level'),
    fh_level=confger.get('logging','fh_level')
)


if __name__ == '__main__':
    my_logger.info('测试日志')