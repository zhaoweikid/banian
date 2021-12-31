#!/usr/local/bin/python3
# coding: utf-8
import os, sys
CWD = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.environ['HOME'], 'github'))
sys.path.append(os.path.dirname(CWD))
import client


cli = client.HTTPClient()
u = client.User(cli)


def test_role():
    global u, cli
    print('orgid:', u.orgid)

    r = client.Role(cli)
    r.clear()

    record = r.dbrecord()

    ret = r.query() 
    assert len(ret['data']['data']) == len(record)


    ret = r.create(name='hehe', info='测试的', orgid=u.orgid)
    assert ret['ret'] == 0

    roleid = ret['data']['id'] 

    ret = r.query(id=roleid, orgid=u.orgid)
    assert ret['data']['id'] == roleid

    role_info = '哈哈哈哈'
    ret = r.modify(id=roleid, info=role_info)
    ret = r.query(id=roleid)
    assert ret['data']['info'] == role_info


