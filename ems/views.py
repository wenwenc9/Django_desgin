from django.shortcuts import render, HttpResponse, reverse, redirect, get_object_or_404
from django.views import View
from .utils import login_required, relate, search_grade, relate_required, success, server_error, params_error
from .parameters import CURRENT_USER
from .forms import RelateForm
from django.utils.decorators import method_decorator
from .models import Grade, Term, Subject, Student
import json
from django.core.paginator import Paginator, EmptyPage

@login_required
def index(request, **kwargs):
    # 主页，直接渲染html
    return render(request, 'ems/index.html')


@method_decorator(login_required, name='dispatch')
class RelateView(View):
    # 关联

    # get方法，直接渲染页面，传入error_message
    def get(self, request, error_message=None, **kwargs):
        if not error_message:
            error_message = request.GET.get('error_message')
        if error_message:
            context = {
                'error_message': error_message
            }
        else:
            context = {}
        return render(request, 'ems/relate.html', context=context)

    # post方法，处理用户提交的关联信息，根据处理结果做不同的返回
    def post(self, request, **kwargs):
        form = RelateForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            result = relate(request, id, password)  # 关联，参看relate
            if result['code'] == 200:
                return self.get(request, error_message=result.get('message'))
            else:
                error_message= result['message']
                return self.get(request, error_message)
        else:
            error_message = form.errors.popitem()[1][0]
            return self.get(request, error_message=error_message)


@method_decorator(login_required, name='dispatch')
@method_decorator(relate_required, name='dispatch')
class GradeTeacherView(View):
    # 成绩

    # get方法，渲染页面，传入error_message
    def get(self, request, subject_id, error_message=None, **kwargs):
        current_user = kwargs.get(CURRENT_USER)
        subject = get_object_or_404(Subject, pk=subject_id)
        context = {
            'subject': subject,
            'error_message': error_message,
        }
        if current_user.role.name == '教师':
            # 先验证登录的人是不是教师
            if subject.teacher == current_user.teacher:
                # 验证教师是否教这门课
                students = subject.student.all()
                for student in students:
                    grade = Grade.objects.filter(student=student).filter(subject=subject).first()
                    student.grade = grade
                context['students'] = students
                if error_message:
                    context['error_message'] = error_message
                return render(request, 'ems/grade_teacher.html', context=context)

            else:
                return redirect(reverse('subject_teacher'))
        else:
            return redirect(reverse('grade_student'))


    # post方法，处理用户提交的成绩信息，根据处理结果做不同的返回
    # 用于教师给学生录入或修改成绩
    # 前端会把成绩的id和更新后的分数一一配对传过来（points）
    # points结构： [{成绩id：更新后的成绩分数}, {同}, ...]
    def post(self, request, subject_id, **kwargs):
        error_message = None
        points = request.POST.getlist('point') # 获取分数列表
        grades = request.POST.getlist('grade') # 获取成绩id列表
        for i in range(len(grades)):
            # 遍历获取所有的配对值（成绩id-分数）
            # 根据成绩id，找出对应的成绩，修改分数，保存到数据库

            grade_id = grades[i]
            try:
                point = float(points[i])
                if point<0 or point>100:
                    error_message = '小于0或大于100的分数不会被更改！'
                else:
                    grade = get_object_or_404(Grade, pk=grade_id)
                    grade.point = point
                    grade.save()
            except:
                error_message = '提交过程出现错误，请检查输入是否合理！'
                return self.get(request, subject_id, error_message=error_message, **kwargs)
        return self.get(request, subject_id, error_message=error_message, **kwargs)


@login_required
@relate_required
def subject(request, **kwargs):
    # 课程列表页
    current_user = kwargs.get(CURRENT_USER)
    if current_user.role.name == '教师':
        # 筛选出登录教师执教的所有课程
        subjects = Subject.objects.all().filter(teacher=current_user.teacher)
        context = {
            'subjects': subjects
        }
        return render(request, 'ems/subject_teacher.html', context)
    else:
        return redirect(reverse('ems:grade_student'))


@login_required
@relate_required
def grade_student(request, **kwargs):
    # 学生成绩查询界面
    # 注意筛选条件也属于get方法（没有写入数据，只是筛选了获得的数据）
    # 前端会传入term， subject等数据，根据它们进行筛选，参看search_grade
    current_user = kwargs.get(CURRENT_USER)
    term_id = request.GET.get('term')
    subject_id = request.GET.get('subject')
    if term_id:
        term = Term.objects.get(id=term_id)
    else:
        term = None
    if subject_id:
        subject = Subject.objects.get(id=subject_id)
    else:
        subject = None
    grades = search_grade(request, term, subject)
    terms = Term.objects.all()  # 取出所有的学期传入前端以便前端选择
    subjects = Subject.objects.all()  # 取出所有的课程传入前端以便前端选择

    context = {
        'grades': grades,
        'terms': terms,
        'subjects': subjects,
    }

    if current_user.role.name == '学生':
        student = current_user.student
        context['student'] = student
        return render(request, 'ems/grade_student.html', context)
    else:
        return redirect(reverse('ems:subject_teacher'))
