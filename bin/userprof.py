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


