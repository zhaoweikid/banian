#!/usr/local/bin/python3
# coding: utf-8
import os, sys
CWD = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.environ['HOME'], 'github'))
sys.path.append(os.path.dirname(CWD))
import client


cli = client.HTTPClient()
u = client.User(cli)

def test_product():
    global u, cli
    print('orgid:', u.orgid)
    
    p = client.Product(cli, u.orgid)
    p.query()

    ret = p.create(orgid=u.orgid, title='支付产品', content='haha', createid=u.id, pmid=0)
    pid = ret['data']['id']
    p.query()

    t = client.Tag(cli, u.orgid)
    ret = t.query()
    t1 = ret['data']['data'][0]['id']
    
    p.modify(id=pid, tag1=t1)
    ret = p.query()


