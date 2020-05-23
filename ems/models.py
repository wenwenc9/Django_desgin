from django.db import models
# 注意这里从其他app引入model的方式，正常python不支持这样的导入，但是django里边采用这种方法  创建数据库
from user.models import User


GENDER_LIST = ((1, '男'), (-1, '女'))

class Student(models.Model):
    # 学生
    # 注意user：与学生为一对一关系，可以为空（当一个学生信息没有绑定到任何用户的时候）
    s_id = models.IntegerField(primary_key=True, verbose_name='学号')
    real_name = models.CharField(max_length=10, verbose_name='姓名')
    gender = models.IntegerField(choices=GENDER_LIST, default=1, verbose_name='性别')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, verbose_name='用户', null=True, blank=True)
    password = models.CharField(max_length=10, verbose_name='校园卡密码')

    def __str__(self):
        return '{} {}'.format(self.s_id, self.real_name)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'


class Teacher(models.Model):
    # 教师
    # 注意user：与教师为一对一关系，可以为空（当一个教师信息没有绑定到任何用户的时候）
    t_id = models.IntegerField(primary_key=True, verbose_name='工号')
    real_name = models.CharField(max_length=10, verbose_name='姓名')
    gender = models.IntegerField(choices=GENDER_LIST, default=1, verbose_name='性别')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, verbose_name='用户', null=True, blank=True)
    password = models.CharField(max_length=10, verbose_name='校园卡密码')


    def __str__(self):
        return '{} {}'.format(self.t_id, self.real_name)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'


class Term(models.Model):
    # 学期
    # 注意名字必须唯一
    # 包含一个开始日期和一个结束日期
    name = models.CharField(max_length=20, verbose_name='名称', unique=True)
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '学期'
        verbose_name_plural = '学期'


class Subject(models.Model):
    # 课程
    # 注意与老师和学期都为一对多关系（一个老师可以教多门课，一个学期可以有多门课，但反过来都是唯一的）
    # 注意与学生为多对多关系（一个课程里有多个学生，一个学生可以有很多课）
    id = models.IntegerField(primary_key=True, verbose_name='课程号')
    name = models.CharField(max_length=20, verbose_name='课程名')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='任课教师')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name='开课学期')
    student = models.ManyToManyField(Student, verbose_name='学生')
    credit = models.FloatField(verbose_name='学分')

    def __str__(self):
        return '{} {}'.format(self.id, self.name)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'


class Grade(models.Model):
    # 成绩
    # 即某一个课程上某一个学生的分数
    point = models.FloatField(verbose_name='分数')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='课程')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')

    def __str__(self):
        return '{} {} {}'.format(self.student.real_name, self.subject.name, self.point)

    class Meta:
        verbose_name = '成绩'
        verbose_name_plural = '成绩'
        # 注意这里student和subject的联合值应该是唯一的
        # 即一个学生在一个课程上的分数只有一个，二者构成联合主键
        unique_together = (("student", "subject"),)
