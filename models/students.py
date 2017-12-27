#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author = "susu"
from models import model,add_api
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import and_,func
Session_class = model.sessionmaker(bind=model.engine)
session = Session_class()
class Students(object):
    def __init__(self,name):
        self.name=name
        session = Session_class()
        self.student_obj = session.query(model.Students).filter(model.Students.name == self.name).first()
        self.classes=self.student_obj.my_classes

    def my_info(self):
        print( '''\033[32mName:\033[0m{}
\033[32mQQ:\033[0m{}
'''.format(self.name,self.student_obj.QQ,self.classes))
        # rank=
        for c in self.classes:
            print("\033[32mClass:\033[0m{}  \033[32mClass rank: \033[0m{}".format(c,1))
    #提交作业
    def commit_homework(self):
        if self.classes:
            for index, classname in enumerate(self.classes):
                print(index,"(\033[31m{}\033[0m)".format(classname))
            chioce_class = input("选择课程:")
            day1 = input("第几天:")
            class_id = self.classes[int(chioce_class)].id
            session = Session_class()
            ret = session.query(model.Study_record).filter(and_(model.Study_record.stu_id == self.student_obj.id,
                                                                model.Study_record.class_id == class_id,
                                                                model.Study_record.day == int(day1))).first()
            if ret.homework=="no":
                y_n = input("确定要提交第{}天{}作业吗？\n(y|n)>>".format(day1,self.classes[int(chioce_class)].name))
                if y_n=="y":
                    ret.homework = "yes"
                    session.commit()
                    print("\033[32mSuccessful commit homework\033[0m")
            else:
                print("你已提交过作业.")
        else:
            print("\033[1;31m你还没有选课!\033[0m")
    #查看成绩
    def check_score(self):
        session = Session_class()
        record=session.query(model.Study_record).filter(model.Study_record.stu_id==self.student_obj.id).all()
        for r in record:
            print(r.score)
            score_info='''\033[32m{}\033[0m
Day:\033[31m{}\033[0m
Class:\033[31m{}\033[0m
score:\033[31m{}\033[0m
'''.format("-"*20,r.day,r.classes,r.score)
            print(score_info)

    #班级排名  先查出所有班级，每个班级的每个学生的分数全部相加，再给所有学生排序
    def class_rank(self):
        for c in self.classes:
            print("\033[1;31;47m================{}================\033[0m".format(c.name))
            session = Session_class()
            data =session.query(model.Study_record.stu_id, func.sum(model.Study_record.score)) \
                .filter(model.Study_record.class_id ==c.id) \
                .group_by(model.Study_record.stu_id) \
                .order_by(func.sum(model.Study_record.score).desc()).all()
            count = 0
            for r in data:
                session = Session_class()
                stu_name = session.query(model.Students.name).filter(model.Students.id == r[0]).first().name
                count += 1
                if r[0]==self.student_obj.id:
                    print("\033[1;31m名次：{}  \033[0m姓名：\033[1;32m{}\033[0m   总数：\033[1;31m{}\033[0m".format(count, stu_name, r[1]))
                else:
                    print("名次：{}    姓名：{}    总数：{}".format(count, stu_name, r[1]))

    @staticmethod
    #返回职业和密码MD5值
    def role_passwd(name):
        session = Session_class()
        res=session.query(model.Students).filter(model.Students.name==name).first()
        if res:
            return ["student",res.password]



