#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author = "susu"
from models import model,add_api
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import and_
Session_class = model.sessionmaker(bind=model.engine)
session = Session_class()
class Teachers(object):
    def __init__(self,name):
        self.name=name
        self.teacher_id()

    def add_student(self,data):
        stu_QQ=data["stu_QQ"]
        class_id=data["class_id"]
        session = Session_class()
        stu_obj=session.query(model.Students).filter(model.Students.QQ==stu_QQ).first()
        class_obj=session.query(model.Classes).filter(model.Classes.id==class_id).first()
        print(stu_obj,class_obj)
        stu_obj.my_classes=[class_obj]
        session.add(stu_obj)
        session.commit()
        print("Successful added!")

    def alter_score(self):
        all_classes=self.my_class()
        chioce_class=input("选择班级:")
        classname=all_classes[int(chioce_class)].name
        students=self.my_students(classname)
        for s in students:
            print(s)
        stu_name = input("学生姓名:")
        session = Session_class()
        student_obj=session.query(model.Students).filter(model.Students.name==stu_name).first()
        #打印出学生的所有信息
        class_id=all_classes[int(chioce_class)].id
        day1=input("第几天:")
        session = Session_class()
        ret = session.query(model.Study_record).filter(and_(model.Study_record.stu_id==student_obj.id,
                                                            model.Study_record.class_id==class_id,
                                                            model.Study_record.day ==int(day1))).first()
        if ret.homework=="yes":
            stu_score=input("分值:")
            ret.score=stu_score
            session.commit()
            print("Successful alter score")
        else:
            print("{}暂未提交作业!".format(stu_name))

    def student_record(self):
        day1=int(input("第几天(eg:1 表示第一天)\n>>"))
        tea_class=self.my_class()
        choice = int(input("选择课程:"))
        class_name=tea_class[choice].name
        class_id1=tea_class[choice].id
        all_students=self.my_students(class_name)
        for index,student_obj in enumerate(all_students):
            print(index,student_obj)
        choice1=input("选择学生:")
        student_name=all_students[int(choice1)].name
        session = Session_class()
        data = session.query(model.Students).filter_by(name=student_name)
        stu_id1 = (data[0].id)
        status1=input("{}'上课情况\nyes|no：".format(student_name))
        add_api.add_study_record(day=day1,stu_id=stu_id1,class_id=class_id1,status=status1)
        print("第{}天 <{}> <{}> 考勤：{}  ".format(day1,class_name,student_name,status1))

    def teacher_id(self):
        session = Session_class()
        data=session.query(model.Teachers).filter_by(name=self.name)
        self.id=(data[0].id)
    #教师班级
    def my_class(self):
        session = Session_class()
        teacher_obj = session.query(model.Teachers).filter(model.Teachers.name == self.name).first()
        for index, classname in enumerate(teacher_obj.my_class):
            print(index,"(\033[1;32m{}\033[0m)"\
                .format(classname))
        return teacher_obj.my_class

    def my_students(self,classname):
        session = Session_class()
        class_obj = session.query(model.Classes).filter(model.Classes.name==classname).first()
        return class_obj.students
    @staticmethod
    #返回职业和密码MD5值
    def role_passwd(name):
        session = Session_class()
        res=session.query(model.Teachers).filter(model.Teachers.name==name).first()
        if res:
            return ["teacher",res.password]

