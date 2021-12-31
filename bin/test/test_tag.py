#!/usr/local/bin/python3
# coding: utf-8
import os, sys
CWD = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.environ['HOME'], 'github'))
sys.path.append(os.path.dirname(CWD))
import client


cli = client.HTTPClient()
u = client.User(cli)


def test_tag():
    global u, cli
    print('orgid:', u.orgid)
    
    t = client.Tag(cli, u.orgid)
    t.query()

    ret = t.create(name='tag1', info='my tag1', orgid=u.orgid)
    tag1 = ret['data']['id']
    ret = t.query(id=tag1)
    assert ret['data']['id'] == tag1
    ret = t.query()
    assert len(ret['data']['data']) >= 1

    newname = 'ragxxxxxx'
    t.modify(id=tag1, name=newname)
    ret = t.query(id=tag1)
    assert ret['data']['name'] == newname



