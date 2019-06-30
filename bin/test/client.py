# coding: utf-8
import os, sys
HOME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(HOME)), 'conf'))
import json
import urllib
import urllib.request
import pprint
from zbase3.base import dbpool, logger
from zbase3.utils import createid
import config_debug
import datetime, time
import urllib
import urllib.parse
from urllib.parse import urlparse

log = logger.install('stdout')
dbpool.install(config_debug.DATABASE)

class MyRequest (urllib.request.Request):
    method = 'GET'
    def get_method(self):
        return self.method


class HTTPClient:
    def __init__(self):
        self.cookie = ''

    def request(self, url, method='GET', values=None):
        print('\33[0;33m' + '='*30 + '\33[0m')
        print('>>>>')
        print(method, url)
        if values:
            print('values:', values)

        netloc = urlparse(url).netloc

        data = None
        if values:
            data = urllib.parse.urlencode(values).encode('utf-8')
        headers = {
            'User-Agent': 'testclient',
            #'Cookie': 'sid=%d'
        }
        if self.cookie:
            headers['Cookie'] = self.cookie

        #req = MyRequest(url, data, headers)
        req = MyRequest(url, data, headers=headers)
        req.method = method
        print('<<<<')

        ret = {}
        try:
            resp = urllib.request.urlopen(req)
        except Exception as e:
            #print(e.code)
            print(e)
        else:
            print(resp.code)
            #print resp.headers
            c = resp.headers.get('Set-Cookie')
            if c:
                self.cookie = c.split(';')[0]
                print('cookie:', self.cookie)

            s = resp.read()
            print('rawdata:', s)
            ret = json.loads(s)
            #pprint.pprint(ret)
            print(json.dumps(ret, indent=2))

            return ret






class Base:
    baseurl = 'http://127.0.0.1:6200/bn/v1/'
    name = ''

    def __init__(self, cli):
        self.cli = cli

    def make_args(self, url, args):
        params = []

        print('args:', args)
        for k,v in args.items():
            if isinstance(v, bytes):
                params.append('%s=%s' % (k, v))
            elif isinstance(v, str):
                if ',' in v and '__' not in k:
                    params.append('%s__in=%s' % (k, urllib.parse.quote(v.encode('utf-8'))))
                else:
                    params.append('%s=%s' % (k, urllib.parse.quote(v.encode('utf-8'))))
            else:
                params.append('%s=%s' % (k, str(v)))
        if params:
            url = url + '?' + '&'.join(params)

        return url

    def clear(self, userid=None, orgid=None):
        where = {}
        if userid:
            where['userid'] = userid

        if orgid:
            where['orgid'] = orgid

        with dbpool.get_connection('banian') as conn:
            conn.delete(self.table, where)


    def create(self, **data):
        url = self.baseurl + self.name +'/create'
        ret = self.cli.request(url, 'POST', data)
        return ret

    def query(self, **data):
        url = self.baseurl + self.name +'/query'
        ret = self.cli.request(self.make_args(url, data))
        return ret

    def modify(self, **data):
        url = self.baseurl + self.name +'/modify'
        ret = self.cli.request(url, 'POST', data)
        return ret

    def delete(self, **data):
        url = self.baseurl + self.name +'/delete'
        ret = self.cli.request(url, 'POST', data)
        return ret

    def any(self, funcname, **data):
        url = self.baseurl + self.name +'/' + funcname
        ret = self.cli.request(self.make_args(url, data))
        return ret



class User(Base):
    baseurl = 'http://127.0.0.1:6101/uc/v1/user'

    def __init__(self, cli, mobile=None):
        self.mobile = '18800006666'
        self.password = '123456'
        self.id = ''
        self.orgid = ''
        self.roleid = None
        self.username = ''

        if mobile:
            self.mobile = mobile

        Base.__init__(self, cli)

        #self.signin()
        #if self.id:
        #    self.init()

        self.init()

    def init(self):
        self.signin()
        if not self.id:
            return
        with dbpool.get_connection('banian') as conn:
            ret = conn.select_one('orga', where={'userid':int(self.id)})
            log.debug('init:%s', ret) 
            if not ret:
                return
            self.orgid = str(ret['id'])
            ret = conn.select_one('profile', where={'userid':int(self.id)})
            if not ret:
                return
            self.username = ret['username']
            self.roleid = ret['roleid']
        
    def signin(self):
        url = self.baseurl + '/signin?password=%s&mobile=%s' % (self.password, self.mobile)
        ret = self.cli.request(url, 'POST')
        self.id = ret['data']['id']
        return ret

    def signup(self):
        url = self.baseurl + '/signup?mobile=%s&password=%s&username=zhaowei%s&email=zhaowei%s@qq.com' % \
            (self.mobile, self.password, self.mobile, self.mobile)
        ret = self.cli.request(url, 'POST')
        self.id = ret['data']['id']

        data = {
            'userid': self.id,
            'username': 'hahe',
            'roleid':0,
            'ctime':DBFunc('UNIX_TIMESTAMP(now())'),
            'utime':DBFunc('UNIX_TIMESTAMP(now())'),
        }
        with dbpool.get_connection('banian') as conn:
            data['id'] = createid.new_id64(conn=conn)
            conn.insert('profile', data)
        return ret



         

class Orga (Base):
    name = 'orga'
    table = 'orga'

    def __init__(self, cli, id=None):
        self.id = id
        Base.__init__(self, cli)
    
class Role (Base):
    name = 'role'
    table = 'role'
    
    def __init__(self, cli, id=None):
        self.id = id
        Base.__init__(self, cli)

    def clear(self):
        where = {'id': ('>', 300)}
        with dbpool.get_connection('banian') as conn:
            conn.delete(self.table, where)

    def dbrecord(self):       
        with dbpool.get_connection('banian') as conn:
            return conn.select(self.table, where=None, fields='*')



class Profile (Base):
    name = 'profile'
    table = 'profile'
    
    def __init__(self, cli, userid=None):
        self.userid = userid
        Base.__init__(self, cli)

class Team (Base):
    name = 'team'
    table = 'team'
    
    def __init__(self, cli, id=None):
        self.id = id
        Base.__init__(self, cli)

    def join(self, **args):
        return self.any('join', **args)

    def quit(self, **args):
        return self.any('quit', **args)


class Tag (Base):
    name = 'tag'
    table = 'tag'
    
    def __init__(self, cli, orgid=None):
        self.orgid = orgid
        Base.__init__(self, cli)

class Product (Base):
    name = 'product'
    table = 'product'
    
    def __init__(self, cli, orgid=None):
        self.orgid = orgid
        Base.__init__(self, cli)

class Plan (Base):
    name = 'plan'
    table = 'plan'
    
    def __init__(self, cli, orgid=None):
        self.orgid = orgid
        Base.__init__(self, cli)


class Item (Base):
    name = 'item'
    table = 'item'
    
    def __init__(self, cli, orgid=None):
        self.orgid = orgid
        Base.__init__(self, cli)


class Discuss (Base):
    name = 'discuss'
    table = 'discuss'
    
    def __init__(self, cli, itemid=None):
        self.itemid = itemid
        Base.__init__(self, cli)

class Attach (Base):
    name = 'attach'
    table = 'attach'
    
    def __init__(self, cli, itemid=None):
        self.itemid = itemid
        Base.__init__(self, cli)




