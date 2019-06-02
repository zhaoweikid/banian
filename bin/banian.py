# coding: utf-8
import os, sys
import time, datetime
import traceback
from zbase3.web import template, validator, advance
from zbase3.web.validator import *
from zbase3.base.dbpool import get_connection
from zbase3.utils import createid
from defines import *
import logging

log = logging.getLogger()


def record_change(record):
    if isinstance(record, list):
        for row in record:
            row['id'] = str(row['id'])
    elif isinstance(record, dict):
        record['id'] = str(record['id'])
    return record

class BaseHandler (advance.APIHandler):
    def fail(self, ret=-1, err='error', debug=''):
        return advance.APIHandler.fail(self, ret, errstr[ret], debug)

    def input(self):
        x1 = self.req.input()
        if x1:
            return x1
        x2 = self.req.inputjson()
        if x2:
            return x2
        return {}


class BaseObject (BaseHandler):
    dbname = 'banian'
    table = ''
    select_fields = '*'
    max_pagesize = 20

    def error(self, data):
        self.fail(ERR_PARAM)
    
    @with_validator([
        F('id', T_INT),
    ])
    def query(self):
        xid = self.data.get('id')
        log.debug('query: %s', xid)
        if xid:
            xid = int(xid)
            self.query_one(xid)
        else:
            self.query_all()
   

    def query_all(self):
        pagecur = int(self.data.get('page', 1))
        pagesize = int(self.data.get('pagesize', self.max_pagesize))
        if pagesize > self.max_pagesize:
            pagesize = self.max_pagesize

        try:
            with get_connection(self.dbname) as conn:
                sql = conn.select_sql(self.table, fields=self.select_fields, other="order by id desc")
                log.debug('select:%s', sql)
                p =  conn.select_page(sql, pagecur, pagesize)
                ret = {'page':p.page, 'pagesize':pagesize, 'pagenum':p.pages, 
                       'data':record_change(p.pagedata.data)}
                self.succ(ret)
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))


    def query_one(self, xid):
        try:
            with get_connection(self.dbname) as conn:
                ret = conn.select(self.table, {'id':int(xid)}, self.select_fields)
                if not ret:
                    self.fail(ERR_NODATA)
                    return
                self.succ(record_change(ret))
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))


    def create(self):
        try:
            log.debug('post data:%s', self.data)
            if not self.data:
                self.fail(ERR_PARAM)
                return
            with get_connection(self.dbname) as conn:
                self.data['id'] = createid.new_id64(conn=conn)
                conn.insert(self.table, self.data)

                self.succ({'id':str(self.data['id'])})
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))

    def modify(self, xid, data):
        xid = int(xid)
        try:
            if not xid:
                self.fail(ERR_PARAM)
                return

            if not data:
                self.fail(ERR_PARAM)
                return

            if 'id' in data:
                data.pop('id')
     
            with get_connection(self.dbname) as conn:
                conn.update(self.table, data, {'id':xid})
                ret = conn.select(self.table, {'id':xid}, self.select_fields)
                self.succ(record_change(ret))
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))


class DeleteMixin:
    def delete(self, xid):
        try:
            if not xid:
                log.info('must have xid')
                self.fail(ERR_PARAM)
                return
            with get_connection(self.dbname) as conn:
                conn.delete(self.table, {'id':int(xid)})
                self.succ()
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))


class Orga (BaseObject):
    table = 'orga'
    select_fields = 'id,name,ctime,utime'
    
    session_nocheck = [
        '/bn/v1/orga/query',
    ]

class Role (BaseObject):
    table = 'role'
    select_fields = 'id,name'

class Profile (BaseHandler):
    dbname = 'banian'
    def GET(self):
        retdata = {'username':'', 'org':{}, 'role':{}}

        try:
            userid = self.ses['userid']
            with get_connection(self.dbname) as conn:
                #ret = conn.query_one('profile', where={'userid':userid})
                ret = conn.query_one('select p.username as username,o.id as orgid,o.name as orgname,r.id as roleid,' \
                    'r.name as rulename, r.perm as perm'\
                    'from profile p,orga o,role r '\
                    'where p.userid=%d and o.id=p.orgid and r.id=p.roleid')
                if ret:
                    retdata['username'] = ret['username']

                    org = retdata['org']
                    org['id'] = ret['orgid']
                    org['name'] = ret['orgname']

                    role = retdata['role']
                    role['id'] = ret['roleid']
                    role['name'] = ret['rolename']
                    role['perm'] = ret['perm']

                return self.succ(retdata)
        except:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))


class Team (BaseObject):
    table = 'team'
    select_fields = 'id,ownerid,name,level,parent,tmtype,ctime,utime'
    max_pagesize = 1000

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



class Plan (BaseObject):
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

class Attachs (BaseObject):
    table = 'attachs'
    select_fields = 'id,itemid,discid,creatid,name,filepath,url,closed,ctime,utime'

class Discuss (BaseObject):
    table = 'discuss'

class Items (BaseObject):
    table = 'items'

class Product (BaseObject):
    table = 'product'

class Profile (BaseObject):
    table = 'profile'

class Tag (BaseObject):
    table = 'tag'


class Index (BaseHandler):
    def GET(self):
        log.info('ping')
        self.succ({'time':str(datetime.datetime.now())[:19], 'content':'pong'})

Ping = Index



