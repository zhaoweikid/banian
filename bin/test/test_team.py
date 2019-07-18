#!/usr/local/bin/python3
# coding: utf-8
import os, sys
CWD = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.environ['HOME'], 'github'))
sys.path.append(os.path.dirname(CWD))
import client


cli = client.HTTPClient()
u = client.User(cli)

def test_team():
    global u, cli
    print('orgid:', u.orgid)

    t = client.Team(cli)
    t.clear(orgid=u.orgid)

    t.query()

    ret = t.create(orgid=u.orgid, ownerid=u.id, name='我的团队', parent=0, tmtype=1)
    tid = ret['data']['id']

    ret = t.query(id=tid)
    assert ret['data']['id'] == tid

    ret = t.query()
    assert len(ret['data']['data']) == 1

    c2 = client.HTTPClient()
    newuser = client.User(c2, '18800007777')
    if not newuser.id:
        newuser.signup()
    
    t.join(id=tid, userid=newuser.id)
    
    ret = t.query(id=tid)
    
    assert len(ret['data']['member']) == 1



