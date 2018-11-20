# coding: utf-8
import os, sys
import time, datetime
import traceback
from zbase3.web import template, validator, advance
from zbase3.web.validator import with_validator_self, Field, T_INT, T_STR, T_FLOAT, T_REG
from zbase3.base.dbpool import get_connection_exception
from zbase3.utils import createid
from defines import *
import logging

log = logging.getLogger()

# GET:query POST:create PUT:update DELETE:delete

def record_long2str(record):
    if isinstance(record, list):
        for row in record:
            row['id'] = str(row['id'])
    elif isinstance(record, dict):
        record['id'] = str(record['id'])
    return record

class BaseHandler (advance.APIHandler):
    def GET(self):
        self.render('index.html')

    def fail(self, ret=-1, err='error', debug=''):
        advance.APIHandler.fail(self, ret, errstr[ret], debug)

    def input(self):
        x1 = self.req.input()
        if x1:
            return x1
        x2 = self.req.inputjson()
        if x2:
            return x2
        return {}


class DataTpl (BaseHandler):
    dbname = 'banian'
    table = ''
    select_fields = '*'
    max_pagesize = 20

    GET_fields = []
    POST_fields = []
    PUT_fields = []

    def error(self, data):
        self.fail(ERR_PARAM)
 
    # select
    @with_validator_self
    def GET(self, xid=None):
        try:
            with get_connection_exception(self.dbname) as conn:
                if xid:
                    ret = conn.select(self.table, {'id':int(xid)}, self.select_fields)
                    if not ret:
                        self.fail(ERR_NODATA)
                        return
                    self.succ(record_long2str(ret))
                else:
                    data = self.req.input()
                    pagecur = int(data.get('page', 1))
                    pagesize = int(data.get('pagesize', self.max_pagesize))
                    if pagesize > self.max_pagesize:
                        pagesize = self.max_pagesize
                    sql = conn.select_sql(self.table, fields=self.select_fields)
                    log.debug('select:%s', sql)
                    p =  conn.select_page(sql, pagecur, pagesize)
                    ret = {'page':p.page, 'pagesize':pagesize, 'pagecount':p.pages, 
                           'data':record_long2str(p.pagedata.data)}
                    self.succ(ret)
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))

    # insert
    @with_validator_self
    def POST(self, xid=None):
        try:
            data = self.input()
            log.debug('post data:%s', data)
            if not data:
                self.fail(ERR_PARAM)
                return
            with get_connection_exception(self.dbname) as conn:
                data['id'] = createid.new_id64(conn=conn)
                conn.insert(self.table, data)

                self.succ({'id':str(data['id'])})
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))

    # update
    @with_validator_self
    def PUT(self, xid):
        try:
            if not xid:
                self.fail(ERR_PARAM)
                return

            data = self.input()
            if not data:
                self.fail(ERR_PARAM)
                return
     
            with get_connection_exception(self.dbname) as conn:
                conn.update(self.table, data, {'id':int(xid)})
                ret = conn.select(self.table, {'id':int(xid)}, self.select_fields)
                self.succ(record_long2str(ret))
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))

    # delete
    def DELETE(self, xid):
        try:
            if not xid:
                log.info('must have xid')
                self.fail(ERR_PARAM)
                return
            with get_connection_exception(self.dbname) as conn:
                conn.delete(self.table, {'id':int(xid)})
                self.succ()
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))


class NoDeleteMixin:
    def DELETE(self, xid):
        log.debug('no delete')
        self.fail(ERR_ACTION)




class Role (NoDeleteMixin, DataTpl):
    table = 'role'
    select_fields = 'id,name'
    POST_fields = []

class Team (NoDeleteMixin, DataTpl):
    table = 'team'
    select_fields = 'id,ownerid,name,level,parent,tmtype,ctime,utime'
    max_pagesize = 1000


class TeamMember (NoDeleteMixin, DataTpl):
    table = 'team_member'


class Plan (DataTpl):
    def __init__(self):
        self.table = 'plan'
        self.ret_fields = []

    def add_user(self, userid):
        pass

    def del_user(self, userid):
        pass

    def add_item(self, itemid):
        pass

    def del_item(self, itemid):
        pass

class Attachs (NoDeleteMixin, DataTpl):
    table = 'attachs'
    select_fields = 'id,itemid,discid,creatid,name,filepath,url,closed,ctime,utime'

class Discuss (NoDeleteMixin, DataTpl):
    table = 'discuss'

class Items (NoDeleteMixin, DataTpl):
    table = 'items'

class Product (NoDeleteMixin, DataTpl):
    table = 'product'

class Profile (NoDeleteMixin, DataTpl):
    table = 'profile'

class Tag (NoDeleteMixin, DataTpl):
    table = 'tag'


class Index (BaseHandler):
    def GET(self):
        log.info('ping')
        self.succ({'time':str(datetime.datetime.now())[:19], 'content':'pong'})

Ping = Index

