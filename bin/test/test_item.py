#!/usr/local/bin/python3
# coding: utf-8
import os, sys
CWD = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.environ['HOME'], 'github'))
sys.path.append(os.path.dirname(CWD))
import client

cli = client.HTTPClient()
u = client.User(cli)

def test_item():
    global u, cli
    print('orgid:', u.orgid)
  
    p = client.Plan(cli, u.orgid)
    ret = p.query()
    pid = ret['data']['data'][0]['id']

    t = client.Item(cli, u.orgid)
    t.query()
    
    ret = t.create(orgid=u.orgid, parentid=0, planid=pid, topid=0, 
        prdid=0, itemtype=1, title='item title', content='item content',
        creatid=u.id, ownerid=u.id)
    itemid = ret['data']['id']

    ret = t.query(id=itemid)

    assert ret['data']['id'] == itemid
   
    newtitle = 'new title'
    ret = t.modify(id=itemid, title=newtitle)

    assert ret['data'][0]['title'] == newtitle


def test_discuss():
    global u, cli
    print('orgid:', u.orgid)
  
    t = client.Item(cli, u.orgid)
    ret = t.query()
    itemid = ret['data']['data'][0]['id']

    ds = client.Discuss(cli, itemid)
    ds.query()

    ret = ds.create(itemid=itemid, content='haha', creatid=u.id)
    dsid = ret['data']['id']

    ret = ds.query(id=dsid)
    assert ret['data']['id'] == dsid

    newcontent = 'new content'
    ret = ds.modify(id=dsid, content=newcontent)

    assert ret['data'][0]['content'] == newcontent
    

def test_attach():
    global u, cli
    print('orgid:', u.orgid)
  
    t = client.Item(cli, u.orgid)
    ret = t.query()
    itemid = ret['data']['data'][0]['id']

    at = client.Attach(cli, itemid)
    at.query()

    ret = at.create(itemid=itemid, discid=0, name='haha', creatid=u.id)
    atid = ret['data']['id']

    ret = at.query(id=atid)
    assert ret['data']['id'] == atid

    newname = 'new name'
    ret = at.modify(id=atid, name=newname)

    assert ret['data'][0]['name'] == newname
 
 

