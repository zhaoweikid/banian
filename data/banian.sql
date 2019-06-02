-- database

DROP DATABASE banian;

CREATE DATABASE banian;
USE banian;
SET NAMES 'utf8';

CREATE TABLE orga (
	id bigint(20) not null primary key,
	name varchar(128) not null unique COMMENT '组织名字',
	ctime int(11) unsigned not null,
	utime int(11) unsigned not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '组织';

CREATE TABLE profile (
	userid bigint(20) not null primary key,
	roleid bigint(20) not null COMMENT '角色',
	orgid bigint(20) not null COMMENT '组织id',
	username varchar(128) not null unique COMMENT '用户名',
	ctime int(11) unsigned not null,
	utime int(11) unsigned not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '用户信息';

CREATE TABLE role (
	id bigint(20) not null primary key,
	name varchar(128) not null unique COMMENT '角色名',
	info varchar(128) not null unique COMMENT '角色描述',
	orgid bigint(20) not null COMMENT '组织id',
	perm varchar(256) COMMENT '权限'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '用户角色';

insert into role(id,name,orgid,info) values (100,'VP',0,'副总裁');
insert into role(id,name,orgid,info) values (101,'TM',0,'总监');
insert into role(id,name,orgid,info) values (102,'TL',0,'技术经理');
insert into role(id,name,orgid,info) values (103,'PM',0,'产品经理');
insert into role(id,name,orgid,info) values (104,'DEV',0,'开发');
insert into role(id,name,orgid,info) values (105,'ARCH',0,'架构师');
insert into role(id,name,orgid,info) values (106,'OP',0,'运维');
insert into role(id,name,orgid,info) values (107,'DBA',0,'数据库管理员');
insert into role(id,name,orgid,info) values (108,'QA',0,'测试');
insert into role(id,name,orgid,info) values (109,'UI',0,'设计师');
insert into role(id,name,orgid,info) values (200,'Android',0,'安卓开发');
insert into role(id,name,orgid,info) values (201,'iOS',0,'苹果开发');
insert into role(id,name,orgid,info) values (202,'Server',0,'服务端开发');
insert into role(id,name,orgid,info) values (203,'Web',0,'前端开发');


CREATE TABLE team (
	id bigint(20) not null primary key,
	orgid bigint(20) not null COMMENT '组织id',
	ownerid bigint(20) not null COMMENT '团队负责人',
	name varchar(128) not null unique COMMENT '团队名称',
	parent bigint(20) not null default 0 COMMENT '父级团队',
	tmtype tinyint not null default 1 COMMENT '团队类型 1.专业团队 2.项目团队',
	ctime int(11) unsigned not null,
	utime int(11) unsigned not null
	/*key `ownerid_idx` (ownerid)*/
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '团队';

CREATE TABLE team_member (
	id bigint(20) not null primary key,
	teamid bigint(20) not null COMMENT '团队id',
	userid bigint(20) not null COMMENT '用户id',
	ctime int(11) unsigned not null,
	utime int(11) unsigned not null,
	key (userid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '团队成员';

CREATE TABLE tag (
	id bigint(20) not null primary key,
	orgid bigint(20) not null COMMENT '组织id',
	name varchar(128) not null COMMENT '类别名称',
	info varchar(256) not null COMMENT '描述',
	ctime int(11) unsigned not null,
	utime int(11) unsigned not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '项目类别';	


CREATE TABLE product (
	id bigint(20) not null primary key,
	orgid bigint(20) not null COMMENT '组织id',
	title varchar(256) not null COMMENT '名称',
	content varchar(1024) not null COMMENT '描述',
	creatid bigint(20) not null COMMENT '创建人',
	pmid bigint(20) not null COMMENT '负责人',
	tag1 bigint(20) not null COMMENT '标签1',
	tag2 bigint(20) not null COMMENT '标签2',
	tag3 bigint(20) not null COMMENT '标签3',
	ctime int(11) unsigned not null,
	utime int(11) unsigned not null,
	key (creatid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '产品';	

CREATE TABLE plan (
	id bigint(20) not null primary key,
	orgid bigint(20) not null COMMENT '组织id',
	creatid bigint(20) not null COMMENT '创建人',
	tag1 bigint(20) not null COMMENT '标签1',
	tag2 bigint(20) not null COMMENT '标签2',
	tag3 bigint(20) not null COMMENT '标签3',
	pmid bigint(20) not null COMMENT '项目负责人',
	title varchar(128) not null COMMENT '迭代名称',
	content varchar(1024) not null COMMENT '迭代描述',
	state tinyint not null default 1 COMMENT '状态 1.创建 2.已确认 3.已开始 4.已暂停 5.已完成 5.取消',
	memo varchar(512) COMMENT '扩展信息',
	tstart int(11) unsigned  NOT NULL default 0 COMMENT '计划开始时间',
	tend int(11) unsigned  NOT NULL default 0 COMMENT '计划结束时间',
	tstart_real int(11) unsigned  NOT NULL default 0 COMMENT '真实开始时间',
	tend_real int(11) unsigned  NOT NULL default 0 COMMENT '真实结束时间',
	point smallint not null default 0 COMMENT '迭代完成需要点数',
	rate smallint not null default 0 COMMENT '迭代完成百分比，100为完成，10表示10%',
	enabled tinyint not null default 1 COMMENT '是否可用',
	ctime int(11) unsigned NOT NULL DEFAULT 0 COMMENT '创建时间',
	utime int(11) unsigned not null COMMENT '更新时间',
	key (creatid),
	key (pmid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '迭代计划';

CREATE TABLE items (
	id bigint(20) not null primary key,
	orgid bigint(20) not null COMMENT '组织id',
	parentid bigint(20) not null default 0 COMMENT '父级任务，任务拆分时可能有多级',
	planid bigint(20) not null default 0 COMMENT '迭代id',
	topid bigint(20) not null default 0 COMMENT '第1级任务id',
	prdid bigint(20) not null default 0 COMMENT '产品id',
	itemtype smallint not null default 0 COMMENT '任务类型 1.开发任务 2.产品需求',
	tag1 bigint(20) not null COMMENT '标签1',
	tag2 bigint(20) not null COMMENT '标签2',
	tag3 bigint(20) not null COMMENT '标签3',
	title varchar(256) not null COMMENT '任务标题',
	content varchar(4096) COMMENT '任务内容',
	memo varchar(2048) COMMENT '扩展信息',
	creatid bigint(20) not null COMMENT '创建人',
	ownerid bigint(20) not null COMMENT '负责人，即实际做的人',
	point smallint not null default 0 COMMENT '任务完成需要点数',
	rate smallint not null default 0 COMMENT '任务完成百分比，100为完成，10表示10%',
	state smallint not null default 1 COMMENT '状态 1.创建 2.已确认 3.已开始 4.已暂停 5.已完成',
	closed tinyint not null default 0 COMMENT '是否关闭',
	ctime int(11) unsigned not null,
	utime int(11) unsigned not null COMMENT '更新时间',
	key (planid),
	key (topid),
	key (creatid),
	key (ownerid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '任务';

CREATE TABLE discuss (
	id bigint(20) not null primary key,
	itemid bigint(20) not null,
	content varchar(1024) not null COMMENT '内容',
	creatid bigint(20) not null COMMENT '创建人',
	closed tinyint not null default 0 COMMENT '是否删除',
	ctime int(11) unsigned not null,
	utime int(11) unsigned not null COMMENT '更新时间',
	key (itemid),
	key (creatid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '讨论';
	

CREATE TABLE attachs (
	id bigint(20) not null primary key,
	itemid bigint(20) not null COMMENT '任务id',
	discid bigint(20) not null default 0 COMMENT '评论id, 0表示不是评论',
	creatid bigint(20) not null COMMENT '创建人',
	name varchar(128) not null COMMENT '文件名',
	filepath varchar(256) not null COMMENT '路径',
	url varchar(256) not null COMMENT 'URL',
	closed tinyint not null default 0 COMMENT '是否关闭',
	ctime int(11) unsigned not null COMMENT '创建时间',
	utime int(11) unsigned not null COMMENT '更新时间',
	key (itemid),
	key (creatid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '附件';




