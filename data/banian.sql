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

CREATE TABLE project (
	id bigint(20) not null primary key,
	name varchar(256) not null,
	creatid bigint(20) not null comment '创建人id',
	ctime int(4) unsigned not null,
	uptime int(4) unsigned not null,
);

CREATE TABLE plan (
	id bigint(20) not null primary key,
);
