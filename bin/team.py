# coding: utf-8
import os, sys
import time, datetime
import traceback
from zbase3.web import template, validator, advance
from zbase3.web.validator import *
from zbase3.base.dbpool import get_connection, DBFunc
from zbase3.utils import createid
from defines import *
from base import BaseHandler, BaseObject, record_change
import config
import logging

log = logging.getLogger()


class TeamMember:
    table = 'team_member'
    fields = 'id,userid,teamid,FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'

    def __init__(self, teamid):
        self.teamid = teamid

    def create(self, userid):
        data = {
            'id':0,
            'teamid': self.teamid,
            'userid': userid,
            'ctime': DBFunc('UNIX_TIMESTAMP(now())'),
            'utime': DBFunc('UNIX_TIMESTAMP(now())'),
        }
        with get_connection('banian') as conn:
            data['id'] = createid.new_id64(conn=conn)
            conn.insert(self.table, data)

    def query(self, cond=None, fields=None):
        where = {}
        if cond:
            where.update(cond)
        where['teamid'] = self.teamid
        with get_connection('banian') as conn:
            ret = conn.select(self.table, where=where, fields=self.fields)
            record_change(ret)
            return ret


    def modify(self, val=None, cond=None):
        where = {}
        if cond:
            where.update(cond)
        where['teamid'] = self.teamid

        value = {} 
        if val:
            value.update(val)
        value['utime']  = DBFunc('UNIX_TIMESTAMP(now())')
        with get_connection('banian') as conn:
            ret = conn.update(self.table, value, where)
            return ret


class Team (BaseObject):
    table = 'team'
    select_fields = 'id,ownerid,name,parent,tmtype,FROM_UNIXTIME(ctime) as ctime,FROM_UNIXTIME(utime) as utime'
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
        F('id', T_INT),
        F('ownerid', T_INT),
        F('name'),
        F('parent', T_INT),
        F('tmtype', T_INT),
    ])
    def query(self):
        ret = BaseObject.query(self)
        if not ret:
            return ret
        if 'data' in ret and not ret.get('data'):
            return ret

        log.debug('ret:%s', ret)
        if 'page' in ret:
            rows = ret['data']
        else:
            rows = [ret]

        idstr = ','.join([ str(x['id']) for x in rows ])

        userinfo = None
        with get_connection('banian') as conn:
            sql = "select tm.teamid as teamid,tm.userid as userid, p.username as username " \
                  "from team_member tm, profile p where tm.teamid in (%s) and p.userid=tm.userid" \
                  % (idstr)
            userinfo = conn.query(sql)
            log.debug('userinfo:%s', userinfo)
            
        tuser = {}
        for row in userinfo:
            tmid = str(row['teamid'])
            item = {'userid':str(row['userid']), 'username':row['username']}
            if tmid in tuser:
                tuser[tmid].append(item)
            else:
                tuser[tmid] = [item]
        log.debug('tuser:%s', tuser)

        for row in rows:
            if row['id'] in tuser:
                row['member'] = tuser[row['id']]
            else:
                row['member'] = []

        return ret

    
    @with_validator([
        F('id', T_INT, must=True),
        F('userid', T_INT),
    ])
    def join(self):
        teamid = self.data.get('id')
        userid = self.data.get('userid')

        member = TeamMember(teamid)
        member.create(userid)
        ret = member.query()

        return ret

    @with_validator([
        F('id', T_INT, must=True),
        F('userid', T_INT),
    ])
    def quit(self):
        teamid = self.data.get('id')
        userid = self.data.get('userid')

        member = TeamMember(teamid)
        member.modify({'enabled':0}, {'userid':userid})
        ret = member.query()

        return ret



