# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import os
import sys
from webconfig import *

# 服务地址
HOST = '0.0.0.0'

# 服务端口
PORT = 6200

# 日志文件配置
LOGFILE = 'stdout'

# 数据库配置
DATABASE = {
    'banian': {
        'engine':'pymysql',
        'db': 'banian',
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'zhaowei',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
}

