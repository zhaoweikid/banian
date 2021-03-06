# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import os
import sys
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 调试模式: True/False
# 生产环境必须为False
DEBUG = True

# URLS配置
URLS = None

# 静态路径配置
STATICS = {'/s1/':'/default/'}

# 模板配置
TEMPLATE = {
    'cache': not DEBUG,
    'path': 'templates',
    'tmp': os.path.join(HOME, 'tmp'),
}

# APP就是一个子目录
APPS = (

)

# 中间件
MIDDLEWARE = (
    # middleware
)

# WEB根路径
DOCUMENT_ROOT = os.path.join(HOME, 'static')

# 页面编码
CHARSET = 'UTF-8'

# session配置
# store:DiskSessionStore, expire:x, path:/tmp
# store:RedisSessionStore, expire:x, 'addr':[(ip,port)]
# store:MemcachedSessionStore, expire:x, addr:[(ip,port)]
#SESSION = {'store':'DiskSessionStore', 'expire':30, 'path':'/tmp'}

SESSION = { 
    'store':'SessionRedis', 
    'server':[{'addr':('127.0.0.1', 6379), 'timeout':1000}], 
    'expire':3600,
}

