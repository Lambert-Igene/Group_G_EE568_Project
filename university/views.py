from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from university.models import *


def login(request):
    template = loader.get_template('login.html')
    if request.method == "GET":
        context = {}
    elif request.method == "POST":
        login_as = request.POST.get("login_as", "")
        id = request.POST.get("id", "")
        password = request.POST.get("password", "")

        if login_as == 'admin':
            try:
                admin = Admin.objects.get(id=id)
                if admin.password == password:
                    request.session["login_as"] = login_as
                    request.session["id"] = id
                    return redirect('/admin')
                else:
                    context = {"error": "Wrong Password"}
            except Admin.DoesNotExist:
                context = {"error": "Invalid Admin ID"}
        elif login_as == 'professor':
            try:
                instructor = Instructor.objects.get(id=id)
                if instructor.password == password:
                    request.session["login_as"] = login_as
                    request.session["id"] = id
                    return redirect('/professor')
                else:
                    context = {"error": "Wrong Password"}
            except Instructor.DoesNotExist:
                context = {"error": "Invalid Instructor ID"}
        elif login_as == 'student':
            try:
                student = Student.objects.get(student_id=id)
                if student.password == password:
                    request.session["login_as"] = login_as
                    request.session["student_id"] = id
                    return redirect('/student')
                else:
                    context = {"error": "Wrong Password"}
            except Student.DoesNotExist:
                context = {"error": "Invalid Student ID"}
        else:
            return redirect('/login')

    return HttpResponse(template.render(context, request))


def logout(request):
    try:
        del request.session["login_as"]
        del request.session["id"]
        context = {'message': 'Logout Successfully'}
    except KeyError:
        pass
        context = {'error': 'Unable to Logout'}

    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


def admin(request):
    template = loader.get_template('admin/admin.html')
    context = {}

    return HttpResponse(template.render(context, request))


def roaster(request):
    sort_by = request.GET.get('sort_by')
    if sort_by not in ['id', 'name', 'dept_name', 'salary']:
        sort_by = 'id'

    template = loader.get_template('admin/roaster.html')
    professors = Instructor.objects.all().order_by(sort_by).values()
    context = {
        'professors': professors,
        'sort_by': sort_by
    }

    return HttpResponse(template.render(context, request))


def salary(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT dept_name, "
                       "MIN(salary) AS 'min_salary', "
                       "MAX(salary) AS 'max_salary', "
                       "ROUND(AVG(salary),2) AS 'average_salary' "
                       "FROM instructor "
                       "WHERE dept_name IS NOT NULL "
                       "GROUP BY dept_name")
        columns = [col[0] for col in cursor.description]
        departments = [dict(zip(columns, row)) for row in cursor.fetchall()]

    template = loader.get_template('admin/salary.html')

    context = {
        'departments': departments
    }

    return HttpResponse(template.render(context, request))


def performance(request):
    template = loader.get_template('admin/performance.html')
    context = {}

    return HttpResponse(template.render(context, request))


def performance_result(request):
    template = loader.get_template('admin/performance_result.html')
    context = {}

    return HttpResponse(template.render(context, request))


def professor(request):
    template = loader.get_template('professor/professor.html')
    context = {}

    return HttpResponse(template.render(context, request))


def professor_course_sections(request):
    semester = request.GET.get('semester')
    if semester not in ['1', '2', 'all']:
        semester = "all"

    year = request.GET.get('year')
    if not year:
        year = "all"

    prof_id = request.session["id"]
    query = "SELECT section.course_id,section.sec_id, section.semester, section.year, " \
            "COUNT(*) AS no_of_students FROM section " \
            "JOIN takes ON section.course_id = takes.course_id " \
            "AND section.sec_id = takes.sec_id " \
            "AND section.semester = takes.semester " \
            "AND section.year = takes.year " \
            "JOIN teaches ON section.course_id = teaches.course_id " \
            "AND section.sec_id = teaches.sec_id " \
            "AND section.semester = teaches.semester " \
            "AND section.year = teaches.year " \
            "WHERE teaches.teacher_id = %s " \

    if semester != 'all':
        query += "AND section.semester = '" + semester + "' "
    if year != 'all':
        query += "AND section.year = '" + year + "' "

    query += "GROUP BY section.course_id, section.sec_id,section.semester, section.year"

    with connection.cursor() as cursor:
        cursor.execute(query, [prof_id])
        columns = [col[0] for col in cursor.description]
        course_sections = [dict(zip(columns, row)) for row in cursor.fetchall()]
    template = loader.get_template('professor/course_sections.html')
    context = {
        'course_sections': course_sections,
        'semester': semester,
        'year': year
    }

    return HttpResponse(template.render(context, request))

def course_students(request):
    template = loader.get_template('professor/course_students.html')
    context = {}

    return HttpResponse(template.render(context, request))

def student(request):
    template = loader.get_template('student/student.html')
    context = {}

    return HttpResponse(template.render(context, request))


def department_courses(request):
    template = loader.get_template('student/department_courses.html')
    context = {}

    return HttpResponse(template.render(context, request))
