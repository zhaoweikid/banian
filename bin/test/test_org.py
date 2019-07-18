#!/usr/local/bin/python3
# coding: utf-8
import os, sys
CWD = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.environ['HOME'], 'github'))
sys.path.append(os.path.dirname(CWD))
import client


cli = client.HTTPClient()
u = client.User(cli)


def test_org():
    global cli
    c = client.Orga(cli)
    c.clear()

    ret = c.query()
    assert len(ret['data']['data']) == 0

    ret = c.create(name='我的组织测试6')
    orgid = ret['data']['id']
    print('create orgid:', orgid)

    ret = c.query(id=orgid)
    assert ret['data']['id'] == orgid

    ret = c.query()
    assert len(ret['data']['data']) == 1

    new_orgname = 'gogogogo'
    c.modify(id=orgid, name=new_orgname) 
    ret = c.query()
    assert len(ret['data']['data']) == 1
    assert ret['data']['data'][0]['name'] == new_orgname

    ret = c.query(userid=u.id)
    assert len(ret['data']['data']) == 1



