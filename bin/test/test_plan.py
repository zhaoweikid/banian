#!/usr/local/bin/python3
# coding: utf-8
import os, sys
CWD = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.environ['HOME'], 'github'))
sys.path.append(os.path.dirname(CWD))
import client


cli = client.HTTPClient()
u = client.User(cli)


def test_plan():
    global u, cli
    print('orgid:', u.orgid)
  
    p = client.Plan(cli, u.orgid)
    p.clear()

    p.query()
    
    ret = p.create(orgid=u.orgid, creatid=u.id, pmid=0, title='plan1', content='plan content', state=1)
    pid = ret['data']['id']

    p.query()
    ret = p.query(id=pid)
    assert ret['data']['id'] == pid
   
    newtitle = 'new title'
    ret = p.modify(id=pid, title=newtitle)
    assert ret['data'][0]['title'] == newtitle


