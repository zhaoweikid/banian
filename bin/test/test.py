#!/usr/local/bin/python3
# coding: utf-8
import os, sys
CWD = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(os.environ['HOME'], 'github'))
sys.path.append(os.path.dirname(CWD))
import client


def init():
    print('='*6, 'init', '='*6)
    global u, cli
    cli = client.HTTPClient()

    u = client.User(cli)

    #u.login()


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
 
 
def main():
    init()
    funcs = globals()
   
    name = ''
    if len(sys.argv) == 2:
        name = sys.argv[1]

    if name:
        funcs[name]()
        return

    for k,v in funcs.items():
        if k.startswith('test_'):
            print('='*6, k, '='*6)
            v()




if __name__ == '__main__':
    main()






