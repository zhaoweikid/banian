# coding: utf-8
import os, sys
import time, datetime
import traceback
from zbase3.web import template, validator, advance
from zbase3.web.validator import *
from zbase3.base.dbpool import get_connection, DBFunc
from zbase3.utils import createid
from defines import *
import config
import logging

log = logging.getLogger()


def record_change(record):
    def _(row):
        for k in ['id','userid','orgid']:
            if k in row:
                row[k] = str(row[k])
        if 'password' in row:
            row.pop('password')

    if isinstance(record, list):
        for row in record:
            _(row)
    elif isinstance(record, dict):
        _(row)

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
    session_conf = config.SESSION
    dbname = 'banian'
    table = ''
    select_fields = '*'
    max_pagesize = 20

    def error(self, data):
        self.fail(ERR_PARAM)
    
    def query(self):
        xid = self.data.get('id')
        log.debug('query: %s', xid)
        if xid:
            xid = int(xid)
            self.query_one(xid)
        else:
            if not self.ses.get('isadmin'):
                self.fail(ERR_PERM)
                return
            self.query_all()
   

    def query_all(self):
        pagecur = int(self.data.get('page', 1))
        pagesize = int(self.data.get('pagesize', self.max_pagesize))
        if pagesize > self.max_pagesize:
            pagesize = self.max_pagesize
        where = {}

        for k,v in self.data.items():
            if k in ['page', 'pagesize']:
                continue

            if isinstance(v, (list,tuple)):
                where[k] = (self.validaor.get(k).op, v)
            else:
                where[k] = v

        try:
            with get_connection(self.dbname) as conn:
                sql = conn.select_sql(self.table, where, fields=self.select_fields, other="order by id desc")
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

            self.data['ctime'] = DBFunc('UNIX_TIMESTAMP(now())')
            self.data['utime'] = DBFunc('UNIX_TIMESTAMP(now())')
            with get_connection(self.dbname) as conn:
                self.data['id'] = createid.new_id64(conn=conn)
                conn.insert(self.table, self.data)
                ret = conn.select(self.table, {'id':self.data['id']}, self.select_fields)
                record_change(ret)
                self.succ(ret)
        except Exception as e:
            log.error(traceback.format_exc())
            self.fail(ERR, str(e))

    def modify(self):
        xid = int(self.data.get('id'))
        self.data.pop('id') 
        try:
            self.data['utime'] = DBFunc('UNIX_TIMESTAMP(now())')
            with get_connection(self.dbname) as conn:
                conn.update(self.table, self.data, {'id':xid})
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



