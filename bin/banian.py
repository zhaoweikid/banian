# coding: utf-8
import os, sys
from banbase import *
from zbase.web import template
# GET:query POST:create PUT:update DELETE:delete
#

class BaseHandler (core.Handler):
    def GET(self):
        self.render('index.html')

class DataTpl (BaseHandler):
    def __init__(self):
        self.table = 'role'
        self.ret_fields = []
    
    def GET(self, xid=None):
        with get_connection(self.dbname) as conn:
            if roleid:
                ret = conn.select(self.table, {'id':xid}, self.ret_fields)
                self.succ(ret)
            else:
                data = self.req.input()
                pagecur = int(data.get('page', 1))
                pagesize = int(data.get('pagesize', 100))
                sql = conn.select_sql(self.table, fields=self.ret_fields)
                p =  conn.select_page(self.table, sql, pagecur, pagesize)
                ret = {'page':p.page, 'pagesize':pagesize, 'pagecount':p.pages, 'data':p.pagedata.data}
                self.succ(ret)

    def POST(self, data):
        with get_connection(self.dbname) as conn:
            data['id'] = createid.new_id64(conn=conn)
            conn.insert(self.table, data)

    def PUT(self, xid, data):
        with get_connection(self.dbname) as conn:
            conn.update(self.table, {'id':xid}, data)

    def DELETE(self, xid):
        with get_connection(self.dbname) as conn:
            conn.delete(self.table, {'id':xid})

class Role (DataTpl):
    def __init__(self):
        self.table = 'role'
        self.ret_fields = []

    
class Team (DataTpl):
    def __init__(self):
        self.table = 'team'
        self.ret_fields = []



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

class Attach (BaseHandler):
    pass

class Item (DataTpl):
    def __init__(self):
        self.table = 'item'
        self.ret_fields = []










