## 项目名称：学员管理系统

*本软件只在python3环境下运行。*

#### 实现功能

用户角色，讲师/学员， 用户登陆后根据角色不同，能做的事情不同，分别如下

讲师视图

　　1.管理班级，可创建班级，根据学员qq号把学员加入班级

　　2.可创建指定班级的上课纪录，注意一节上课纪录对应多条学员的上课纪录， 即每节课都有整班学员上， 为了纪录每位学员的学习成绩，需在创建每节上课纪录是，同时         为这个班的每位学员创建一条上课纪录

　　3.为学员批改成绩， 一条一条的手动修改成绩

学员视图

​	1.提交作业

​	2.查看作业成绩

​	3.一个学员可以同时属于多个班级，就像报了Linux的同时也可以报名Python一样， 所以提交作业时需先选择班级，再选择具体上课的节数

附加：学员可以查看自己的班级成绩排名

#### 程序架构

```php+HTML
├──Course_selection_system                #服务端
│      │──bin                       
│      │   ├──Course_selection_system.py      # 执行程序   
│      │   └──__init__.py
│      │── conf              #  配置文件       
│      │   ├──setting.py         
│      │   └──__init__.py
│      │──core               #  主程序交互        
│      │   ├──main.py         
│      │   └──__init__.py
│      │──models               #主程序模块        
│      │   ├──add_api.py     #ORM增删改查接口
│      │   ├──model.py       #创建数据库表结构
│      │   ├──students.py    #学生模块
│      │   ├──teachers.py    #讲师模块
│      │   └──__init__.py
│──README
```

`使用说明：`             q 返回上一层 

[博客地址]: http://www.cnblogs.com/xiangjun555
