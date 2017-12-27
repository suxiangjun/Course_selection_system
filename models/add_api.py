#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author = "susu"
from sqlalchemy.orm import sessionmaker
from models import model
import hashlib
Session_class = sessionmaker(bind=model.engine)
session = Session_class()
def add_student(*args):
    m = hashlib.md5()  # 创建MD5对象
    m.update(args[1].encode())
    _password = m.hexdigest()
    student=model.Students(name=args[0],password=_password,QQ=args[2])
    session.add(student)
    session.commit()
    print("成功注册")

def add_teacher(*args):
    m = hashlib.md5()  # 创建MD5对象
    m.update(args[1].encode())
    _password = m.hexdigest()
    teacher = model.Teachers(name=args[0],password=_password)
    session.add(teacher)
    session.commit()
    print("Successful creation！")

#增加班级
def add_classes(*args):
    class_obj=model.Classes(name=args[0], tea_id=args[1])
    session.add(class_obj)
    session.commit()

#
def add_study_record(**kwargs):
    print("qwqeq",kwargs)
    record=model.Study_record(day=kwargs["day"], stu_id=kwargs["stu_id"],
                              class_id=kwargs["class_id"],status=kwargs["status"])
    session.add(record)
    session.commit()




