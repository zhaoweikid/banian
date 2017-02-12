-- database
CREATE DATABASE banian;

CREATE TABLE profile (
	userid bigint(20) not null primary key
);

CREATE TABLE role (
	id bigint(20) not null primary key,
	name varchar(256) not null unique,
	perm varchar(256)
);

CREATE TABLE team (
	id bigint(20) not null primary key,
	userid bigint(20) not null,
	roleid bigint(20) not null,
	ctime int(4) unsigned not null,
	uptime int(4) unsigned not null
);


CREATE TABLE plan (
	id bigint(20) not null primary key,
	pmid bigint(20) not null,
	masterid bigint(20) not null,
	ctime int(4) unsigned not null,
	uptime int(4) unsigned not null
);

CREATE TABLE plan_ref (
	id bigint(20) not null primary key,
	planid bigint(20) not null,
	refid bigint(20) not null
);

CREATE TABLE project (
	id bigint(20) not null primary key,
	name varchar(256) not null,
	creatid bigint(20) not null comment '创建人id',
	ctime int(4) unsigned not null,
	uptime int(4) unsigned not null,
);


CREATE TABLE items (
	id bigint(20) not null primary key,
	parent bigint(20) not null default 0,
	title varchar(256) not null,
	content varchar(4096),
	attach varchar(2048),
	memo varchar(2048),
	creatid bigint(20) not null,
	state smallint not null default 1,
	ctime int(4) unsigned not null,
	uptime int(4) unsigned not null
);

CREATE TABLE attachs (
	id bigint(20) not null primary key,
	itemid bigint(20) not null,
	creatid bigint(20) not null,
	attach_type smallint not null comment '',
	content varchar(4096),
	ctime int(4) unsigned not null,
	uptime int(4) unsigned not null
);




