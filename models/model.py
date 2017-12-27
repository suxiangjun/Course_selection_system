#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author = "susu"
from sqlalchemy import create_engine,Table,UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from conf import settings
engine = create_engine(settings.connParams)
Base = declarative_base()  # 生成orm基类
#班级----学生  多对多关联
class_m2m_student = Table("class_m2m_student",Base.metadata,
                        Column("id",Integer,primary_key=True),
                        Column('class_id',Integer,ForeignKey("class.id")),
                        Column('student_id',Integer,ForeignKey("student.id")))

#创建教师表
class Teachers(Base):
    __tablename__ = "teacher"  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32),nullable=False)
    password=Column(String(32),nullable=False)
    def __repr__(self):
        return self.name

#创建学生表
class Students(Base):
    __tablename__ = "student"  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32),nullable=False)
    password=Column(String(32),nullable=False)
    QQ= Column(String(12),nullable=False)
    def __repr__(self):
        return self.name

#创建班级表
class Classes(Base):
    __tablename__ = "class"  # 表名
    id = Column(Integer, primary_key=True)
    name= Column(String(32),nullable=False)
    tea_id=Column(Integer,ForeignKey("teacher.id"),nullable=False)   #关联外键
    teachers = relationship("Teachers", backref="my_class")
    students= relationship("Students",secondary=class_m2m_student,backref="my_classes")
    def __repr__(self):
        return  self.name

#创建学习记录表
class Study_record(Base):
    __tablename__ = "study_record"
    __table_args__=(UniqueConstraint("day","stu_id","class_id",name="ay_student_class"),)
    id = Column(Integer, primary_key=True)
    day= Column(Integer,nullable=False)
    stu_id=Column(Integer,ForeignKey("student.id"),nullable=False)
    class_id=Column(Integer,ForeignKey("class.id"),nullable=False)
    status=Column(String(3),nullable=False)
    homework=Column(String(3),default="no")
    score=Column(Integer,default=0)
    students=relationship("Students",backref="day_status")
    classes = relationship("Classes", backref="day_stutus")
    def __repr__(self):
        return '''day:{}
        student:{}
        class:{}
        status:{}
        homework:{} '''.format(self.day,Students.name,Classes.name, self.status,self.homework)

Base.metadata.create_all(engine)
