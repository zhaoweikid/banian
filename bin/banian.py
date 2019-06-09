# coding: utf-8
import os, sys
import time, datetime
import traceback
from zbase3.web import template, validator, advance
from zbase3.web.validator import *
from zbase3.base.dbpool import get_connection, DBFunc
from zbase3.utils import createid
from defines import *
from base import BaseHandler, BaseObject
import config
import logging

log = logging.getLogger()


class Orga (BaseObject):
    table = 'orga'
    select_fields = 'id,name,FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'

    @with_validator([
        F('name', must=True),
        F('userid'),
    ])
    def create(self):
        if 'userid' in self.data and not self.ses.get('isadmin', 0):
            log.debug('only admin can use userid')
            self.fail(ERR_PERM)
            return 
        self.data['userid'] = self.ses.get('userid')
        return BaseObject.create(self)


    @with_validator([
        F('id', T_INT, must=True),
        F('name', must=True),
        F('userid'),
    ])
    def modify(self):
        if 'userid' in self.data and not self.ses.get('isadmin', 0):
            log.debug('only admin can modify userid')
            self.fail(ERR_PERM)
            return 
        return BaseObject.modify(self)
 
    @with_validator([
        F('id', T_INT),
        F('name'),
    ])
    def query(self):
        return BaseObject.query(self)
 
    def check_orgid(self):
        # 创建必须有orgid
        # 修改只有admin才可以改orgid
        # 查询只有admin可以指定orgid
        orgid = self.data.get('orgid')
        isadmin = self.ses.get('isadmin', 0)

        if not orgid and not isadmin:
            log.debug('only admin can not use orgid')
            self.fail(ERR_PERM)
            return False
        return True


class Role (BaseObject):
    table = 'role'
    select_fields = 'id,name,info,orgid,perm,FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'

    @with_validator([
        F('name', must=True),
        F('info'),
        F('orgid', T_INT),
        F('perm'),
    ])
    def create(self):
        return BaseObject.create(self)

    @with_validator([
        F('id', T_INT, must=True),
        F('name'),
        F('info'),
        F('orgid', T_INT),
    ])
    def modify(self):
        return BaseObject.modify(self)
 
    @with_validator([
        F('id', T_INT),
        F('name'),
        F('orgid', T_INT),
    ])
    def query(self):
        return BaseObject.query(self)
 



class Team (BaseObject):
    table = 'team'
    select_fields = 'id,ownerid,name,level,parent,tmtype,ctime,utime'
    max_pagesize = 1000


    @with_validator([
        F('orgid', T_INT),
        F('ownerid', T_INT),
        F('name'),
        F('parent', T_INT, default=0),
        F('tmtype', T_INT, default=1),
    ])
    def create(self):
        return BaseObject.create(self)

    @with_validator([
        F('id', T_INT, must=True),
        F('ownerid', T_INT),
        F('name'),
        F('parent', T_INT, default=0),
        F('tmtype', T_INT, default=1),
    ])
    def modify(self):
        return BaseObject.modify(self)
 
    @with_validator([
        F('id', T_INT, must=True),
        F('ownerid', T_INT),
        F('name'),
        F('parent', T_INT),
        F('tmtype', T_INT),
    ])
    def query(self):
        return BaseObject.query(self)
 
    def add_member(self):
        member = TeamMember()

    def member(self, teamid):
        try:
            retdata = {'users':[]}
            with get_connection(self.dbname) as conn:
                ret = conn.select('team_member', where={'teamid':teamid}) 
                if ret:
                    retdata['users'] = [ row['userid'] for row in ret ]
        except:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))

class Tag (BaseObject):
    table = 'tag'
    select_fields = 'id,name,info,orgid,FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'

    @with_validator([
        F('name', must=True),
        F('info'),
        F('orgid', T_INT),
    ])
    def create(self):
        return BaseObject.create(self)

    @with_validator([
        F('id', T_INT, must=True),
        F('name'),
        F('info'),
        F('orgid', T_INT),
    ])
    def modify(self):
        return BaseObject.modify(self)
 
    @with_validator([
        F('id', T_INT),
        F('name'),
        F('orgid', T_INT),
    ])
    def query(self):
        return BaseObject.query(self)
 

class Product (BaseObject):
    table = 'product'
    select_fields = 'id,orgid,title,content,creatid,pmid,tag1,tag2,tag3,' \
        'FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'

    @with_validator([
        F('orgid', T_INT),
        F('title', must=True),
        F('content'),
        F('pmid', T_INT),
        F('tag1'),
        F('tag2'),
        F('tag3'),
    ])
    def create(self):
        return BaseObject.create(self)

    @with_validator([
        F('id', T_INT, must=True),
        F('orgid', T_INT),
        F('title', must=True),
        F('content'),
        F('pmid', T_INT),
        F('tag1'),
        F('tag2'),
        F('tag3'),
    ])
    def modify(self):
        return BaseObject.modify(self)
 
    @with_validator([
        F('id', T_INT),
        F('orgid', T_INT),
        F('title'),
        F('pmid', T_INT),
        F('tag1'),
        F('tag2'),
        F('tag3'),
    ])
    def query(self):
        return BaseObject.query(self)
 


class Index (BaseHandler):
    session_nocheck = [
        '/bn/v1/ping',
    ]
    def GET(self):
        log.info('ping')
        self.succ({'time':str(datetime.datetime.now())[:19], 'content':'pong'})

Ping = Index



