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


class Plan (BaseObject):
    table = 'plan'
    select_fields = 'id,orgid,creatid,tag1,tag2,tag3,pmid,' \
        'title,content,state,memo,tstart,tend,tstart_real,tend_real,' \
        'point,rate,enabled,' \
        'FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'


    @with_validator([
        F('orgid', T_INT),
        F('title', must=True),
        F('content'),
        F('pmid', T_INT),
        F('tag1'),
        F('tag2'),
        F('tag3'),
        F('state', T_INT, default=1),
        F('memo'),
        F('tstart', T_DATETIME),
        F('tend', T_DATETIME),
        F('tstart_real', T_DATETIME),
        F('tend_real', T_DATETIME),
        F('point', T_INT),
    ])
    def create(self):
        return BaseObject.create(self)

    @with_validator([
        F('id', T_INT, must=True),
        F('orgid', T_INT),
        F('title'),
        F('content'),
        F('pmid', T_INT),
        F('tag1'),
        F('tag2'),
        F('tag3'),
        F('state', T_INT),
        F('memo'),
        F('tstart', T_DATETIME),
        F('tend', T_DATETIME),
        F('tstart_real', T_DATETIME),
        F('tend_real', T_DATETIME),
        F('point', T_INT),
        F('rate', T_INT),
        F('enable', T_INT),
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
        F('state', T_INT),
        F('tstart', T_DATETIME),
        F('tend', T_DATETIME),
        F('tstart_real', T_DATETIME),
        F('tend_real', T_DATETIME),
        F('enable', T_INT),
    ])
    def query(self):
        return BaseObject.query(self)
    

    def add_user(self, userid):
        pass

    def del_user(self, userid):
        pass

    def add_item(self, itemid):
        pass

    def del_item(self, itemid):
        pass


class Item (BaseObject):
    table = 'item'
    select_fields = 'id,orgid,parentid,planid,topid,prdid,itemtype,' \
        'tag1,tag2,tag3,title,content,memo,creatid,ownerid,' \
        'point,rate,enabled,' \
        'FROM_UNIXTIME(tstart) as tstart,FROM_UNIXTIME(tend) as tend,' \
        'FROM_UNIXTIME(tstart_real) as tstart_real,FROM_UNIXTIME(tend_real) as tend_real,' \
        'FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'

    @with_validator([
        F('orgid', T_INT),
        F('parentid', T_INT, must=True),
        F('planid', T_INT, must=True),
        F('topid', T_INT, must=True),
        F('prdid', T_INT, must=True),
        F('ownerid', T_INT),
        F('itemtype', T_INT, must=True),
        F('title', must=True),
        F('content'),
        F('tag1'),
        F('tag2'),
        F('tag3'),
        F('state', T_INT, default=1),
        F('memo'),
        F('tstart', T_DATETIME),
        F('tend', T_DATETIME),
        F('tstart_real', T_DATETIME),
        F('tend_real', T_DATETIME),
        F('point', T_INT),
    ])
    def create(self):
        return BaseObject.create(self)

    @with_validator([
        F('id', T_INT, must=True),
        F('orgid', T_INT),
        F('parentid', T_INT),
        F('planid', T_INT),
        F('topid', T_INT),
        F('prdid', T_INT),
        F('ownerid', T_INT),
        F('itemtype', T_INT),
        F('title'),
        F('content'),
        F('tag1'),
        F('tag2'),
        F('tag3'),
        F('state', T_INT),
        F('memo'),
        F('tstart', T_DATETIME),
        F('tend', T_DATETIME),
        F('tstart_real', T_DATETIME),
        F('tend_real', T_DATETIME),
        F('point', T_INT),
        F('rate', T_INT),
    ])
    def modify(self):
        return BaseObject.modify(self)


    @with_validator([
        F('id', T_INT),
        F('orgid', T_INT),
        F('parentid', T_INT),
        F('planid', T_INT),
        F('topid', T_INT),
        F('prdid', T_INT),
        F('ownerid', T_INT),
        F('itemtype', T_INT),
        F('title'),
        F('tag1'),
        F('tag2'),
        F('tag3'),
        F('state', T_INT),
        F('tstart', T_DATETIME),
        F('tend', T_DATETIME),
        F('tstart_real', T_DATETIME),
        F('tend_real', T_DATETIME),
    ])
    def query(self):
        return BaseObject.query(self)


class Discuss (BaseObject):
    table = 'discuss'
    select_fields = 'id,itemid,content,creatid,enabled,' \
        'FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'
    
    @with_validator([
        F('itemid', T_INT, must=True),
        F('content'),
    ])
    def create(self):
        return BaseObject.create(self)

    @with_validator([
        F('id', T_INT, must=True),
        F('itemid', T_INT),
        F('content'),
        F('enabled'),
    ])
    def modify(self):
        return BaseObject.modify(self)

    @with_validator([
        F('id', T_INT),
        F('itemid', T_INT),
        F('enabled'),
    ])
    def query(self):
        return BaseObject.query(self)




class Attach (BaseObject):
    table = 'attach'
    select_fields = 'id,itemid,discid,creatid,name,filepath,url,enabled,' \
        'FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'

    @with_validator([
        F('itemid', T_INT, must=True),
        F('discid', T_INT, must=True),
        F('name'),
        F('filepath'),
        F('url'),
    ])
    def create(self):
        return BaseObject.create(self)

       
    @with_validator([
        F('id', T_INT, must=True),
        F('itemid', T_INT),
        F('discid', T_INT),
        F('name'),
        F('filepath'),
        F('url'),
        F('enabled'),
    ])
    def modify(self):
        return BaseObject.modify(self)

    @with_validator([
        F('id', T_INT),
        F('itemid', T_INT),
        F('discid', T_INT),
        F('name'),
        F('filepath'),
        F('url'),
        F('enabled'),
    ])
    def query(self):
        return BaseObject.query(self)


    def upload(self):
        pass
    
