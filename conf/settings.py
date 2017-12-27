#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author = "susu"
hostname = "192.168.5.132"
database = 'susu'
username = 'junesu'
password = '123456'
connParams="mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8".format(username,password,hostname,database)