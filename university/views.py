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
        else :
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
    name = request.GET.get('name')
    year = request.GET.get('year')
    semester = request.GET.get('semester')

    # Total number of course sections taught during the semester/year
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM section "
                       "JOIN teaches ON section.course_id = teaches.course_id "
                       "AND section.sec_id = teaches.sec_id "
                       "AND section.semester = teaches.semester "
                       "AND section.year = teaches.year "
                       "JOIN instructor ON teaches.teacher_id = instructor.ID "
                       "WHERE instructor.name = %s "
                       "AND section.year = %s "
                       "AND section.semester = %s ", [name, year, semester])
        total_course_sections = cursor.fetchone()[0]

    # The total number of students taught
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM takes "
                       "JOIN teaches ON takes.course_id = teaches.course_id "
                       "AND takes.sec_id = teaches.sec_id "
                       "AND takes.semester = teaches.semester "
                       "AND takes.year = teaches.year "
                       "JOIN instructor ON teaches.teacher_id = instructor.ID "
                       "WHERE instructor.name = %s "
                       "AND teaches.year = %s "
                       "AND teaches.semester = %s ", [name, year, semester])
        total_students_taught = cursor.fetchone()[0]

    # The total dollar amount of funding the professor has secured
    with connection.cursor() as cursor:
        cursor.execute("SELECT SUM(funding_award.amount), COUNT(*) FROM funding_award_investigator "
                       "JOIN funding_award ON funding_award_investigator.funding_award = funding_award.id "
                       "JOIN instructor ON funding_award_investigator.professor = instructor.ID "
                       "WHERE instructor.name = %s ", [name])
        total_amount_of_funding, total_funding_awards = cursor.fetchone()

    # The total number of papers the professor has published
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM publication_author "
                       "JOIN instructor ON publication_author.professor = instructor.ID "
                       "WHERE instructor.name = %s ", [name])
        total_papers_published = cursor.fetchone()[0]

    template = loader.get_template('admin/performance_result.html')
    context = {
        "name": name,
        "semester": semester,
        "year": year,
        "total_course_sections": total_course_sections,
        "total_students_taught": total_students_taught,
        "total_amount_of_funding": total_amount_of_funding,
        "total_funding_awards": total_funding_awards,
        "total_papers_published": total_papers_published
    }

    return HttpResponse(template.render(context, request))

def professor(request):
    template = loader.get_template('professor/professor.html')
    context = {}

    return HttpResponse(template.render(context, request))

def courses(request):
    template = loader.get_template('professor/courses.html')
    context = {}

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