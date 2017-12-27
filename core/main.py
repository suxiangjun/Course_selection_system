#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author = "susu"
import sys,hashlib
import sqlalchemy
from models import teachers,add_api,students
from models import model,add_api
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import and_
Session_class = model.sessionmaker(bind=model.engine)
#注册模块
def register():
    role = input("你的身份是？\033[1;31m\n1.学生\n2.讲师\n\033[0m>>")
    if role=="1":
        for i in range(3):
            _username = input("姓名：")
            if _username=="q":break
            _password = input("密码：")
            if _password=="q":break
            _password1 = input("重新输入密码：")
            if _password1=="q":break
            if _password ==_password1:
                qq=input("QQ号：")
                add_api.add_student(_username,_password,qq)
                break
            else:
                print("两次输入不同，重新输入。")
        else:
            sys.exit("输错3次。")
    elif role=="2":
        for i in range(3):
            _username = input("姓名：")
            if _username=="q":break
            _password = input("密码：")
            if _password=="q":break
            _password1 = input("重新输入密码：")
            if _password1=="q":break
            if _password ==_password1:
                add_api.add_teacher(_username,_password)
                break
            else:
                print("两次输入不同，重新输入。")
        else:
            sys.exit("输错3次。")
    elif role=="q": sys.exit()
    else:
        pass

#装饰器
def login(fun):
    print("\033[1;31;46m================欢迎登陆校园网================\033[0m")
    def deco(*args, **kwargs):
        username = input("用户名>>:")
        for i in range(3):
            role_password = teachers.Teachers.role_passwd(username)  # eg: [“teacher”,"密码"]
            if not role_password:
                role_password = students.Students.role_passwd(username)
            if not role_password:
                print("用户不存在,请注册")
                register()
                continue
            password = input("登录密码>>:")
            m = hashlib.md5()  # 创建MD5对象登陆
            m.update(password.encode())
            _password = m.hexdigest()
            if _password == role_password[1]:  # 认证功能
                fun(role_password[0], username)
            else:
                print("密码错误")
        else:
            sys.exit("错误次数超过3次")
    return deco  # 返回装饰函数的内存地址

def teacher(name):
    print("welcome:\033[32m{}\033[0m".format(name))
    info='''\033[31m
1.创建我的班级
2.添加学生
3.学生考勤
4.批改作业
5.我的班级\033[0m  
>>'''
    while True:
        try:
            teacher_obj = teachers.Teachers(name)
            choice1=input(info)
            if choice1=="1":
                class_name=input("新班级的名字:")
                add_api.add_classes(class_name,teacher_obj.id)
            elif choice1=="2":
                stu_qq=input("学生QQ:")
                session = Session_class()
                stu_obj = session.query(model.Students).filter(model.Students.QQ == stu_qq).first()
                if stu_obj:
                    res=teacher_obj.my_class()
                    chioce_class = input("选择班级:")
                    if chioce_class.isdigit():
                        data={"stu_QQ":stu_qq,"class_id":res[int(chioce_class)].id}
                        teacher_obj.add_student(data)
                else:
                    print("\033[1;32m该学生不存在\033[0m")
            elif choice1=="3":
                teacher_obj.student_record()
            elif choice1=="4":
                teacher_obj.alter_score()
            elif choice1=="5":
                teacher_obj.my_class()
            elif choice1=="q":
                sys.exit()
        except AttributeError as e:
            print("\033[1;31m学生信息错误.\033[0m")

def student(name):
    print("\033[1;31mwelcome:\033[0m\033[32m{}\033[0m".format(name))
    stu_obj = students.Students(name)
    while True:
        choice1 = input("1.我的资料.\n2.提交作业.\n3.查看作业分数.\n4.班级排名\n>>")
        if choice1 == "1":
            stu_obj.my_info()
        elif choice1 == "2":
            stu_obj.commit_homework()
        elif choice1 == "3":
            stu_obj.check_score()
        elif choice1=="4":
            stu_obj.class_rank()
        elif choice1=="q":
            sys.exit()

@login
def run(role,name):
    if role=="teacher":
        teacher(name)
    elif role=="student":
        student(name)


