from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from university.models import *


# Star of generic view functions for all users

def login(request):
    template = loader.get_template('login.html')
    if request.method == "GET":
        context = {}
    else:  # POST
        login_as = request.POST.get("login_as", "")
        user_id = request.POST.get("id", "")
        password = request.POST.get("password", "")

        if login_as == 'admin':
            try:
                admin = Admin.objects.get(id=user_id)
                if admin.password == password:
                    request.session["login_as"] = login_as
                    request.session["user_id"] = user_id
                    return redirect('/admin')
                else:
                    context = {"error": "Wrong Password"}
            except Admin.DoesNotExist:
                context = {"error": "Invalid Admin ID"}
        elif login_as == 'professor':
            try:
                instructor = Instructor.objects.get(id=user_id)
                if instructor.password == password:
                    request.session["login_as"] = login_as
                    request.session["user_id"] = user_id
                    return redirect('/professor')
                else:
                    context = {"error": "Wrong Password"}
            except Instructor.DoesNotExist:
                context = {"error": "Invalid Instructor ID"}
        elif login_as == 'student':
            try:
                student = Student.objects.get(student_id=user_id)
                if student.password == password:
                    request.session["login_as"] = login_as
                    request.session["student_id"] = user_id
                    return redirect('/student')
                else:
                    context = {"error": "Wrong Password"}
            except Student.DoesNotExist:
                context = {"error": "Invalid Student ID"}
        else:
            return redirect('/login')

    return HttpResponse(template.render(context, request))


def logout(request):
    request.session.delete("login_as")
    request.session.delete("user_id")
    context = {'message': 'Logout Successfully'}

    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


# Star of Admin view functions

def admin(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'admin':
        return redirect('/login')

    template = loader.get_template('admin/admin.html')
    context = {}

    return HttpResponse(template.render(context, request))


def admin_roaster(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'admin':
        return redirect('/login')

    sort_by = request.GET.get('sort_by')
    if sort_by not in ['id', 'name', 'dept_name', 'salary']:
        sort_by = 'id'

    sort_direction = request.GET.get('sort_direction')
    if sort_direction not in ['asc', 'desc']:
        sort_direction = 'asc'

    if sort_direction == 'desc':
        sort_by = f'-{sort_by}'

    template = loader.get_template('admin/roaster.html')
    professors = Instructor.objects.all().order_by(sort_by).values()
    context = {
        'professors': professors,
        'sort_by': sort_by,
        'sort_direction': sort_direction
    }

    return HttpResponse(template.render(context, request))


def admin_salary(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'admin':
        return redirect('/login')

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


def admin_performance(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'admin':
        return redirect('/login')

    template = loader.get_template('admin/performance.html')
    context = {}

    return HttpResponse(template.render(context, request))


def admin_performance_result(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'admin':
        return redirect('/login')

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


# Star of Professor view functions


def professor(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'professor':
        return redirect('/login')

    template = loader.get_template('professor/professor.html')
    context = {}

    return HttpResponse(template.render(context, request))


def professor_course_sections(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'professor':
        return redirect('/login')

    semester = request.GET.get('semester')
    if semester not in ['1', '2', 'all']:
        semester = "all"

    year = request.GET.get('year')
    if not year:
        year = "all"

    prof_id = request.session["user_id"]
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
            "WHERE teaches.teacher_id = %s "
    query_params = [prof_id]

    if semester != 'all':
        query += "AND section.semester = %s "
        query_params.append(semester)
    if year != 'all':
        query += "AND section.year = %s "
        query_params.append(year)

    query += "GROUP BY section.course_id, section.sec_id,section.semester, section.year"

    with connection.cursor() as cursor:
        cursor.execute(query, query_params)
        columns = [col[0] for col in cursor.description]
        course_sections = [dict(zip(columns, row)) for row in cursor.fetchall()]
    template = loader.get_template('professor/course_sections.html')
    context = {
        'course_sections': course_sections,
        'semester': semester,
        'year': year
    }

    return HttpResponse(template.render(context, request))


def professor_course_students(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'professor':
        return redirect('/login')

    template = loader.get_template('professor/course_students.html')
    courses = Course.objects.all()
    context = {
        'courses': courses
    }

    return HttpResponse(template.render(context, request))


def professor_course_students_result(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'professor':
        return redirect('/login')

    course = request.GET.get('course')
    semester = request.GET.get('semester')
    year = request.GET.get('year')
    professor_id = request.session["user_id"]

    with connection.cursor() as cursor:
        cursor.execute("SELECT student.*, takes.sec_id "
                       "FROM student JOIN takes ON "
                       "student.student_id = takes.student_id "
                       "JOIN teaches ON takes.course_id = teaches.course_id "
                       "AND takes.sec_id = teaches.sec_id "
                       "AND takes.semester = teaches.semester "
                       "AND takes.year = teaches.year "
                       "WHERE teaches.teacher_id = %s "
                       "AND takes.year = %s AND takes.semester = %s "
                       "AND takes.course_id = %s", [professor_id, year, semester, course])

        columns = [col[0] for col in cursor.description]
        course_students = [dict(zip(columns, row)) for row in cursor.fetchall()]

    template = loader.get_template('professor/course_students_result.html')
    context = {
        'course_students': course_students,
        'course': course,
        'semester': semester,
        'year': year
    }

    return HttpResponse(template.render(context, request))


# Star of Student view functions


def student(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'student':
        return redirect('/login')

    template = loader.get_template('student/student.html')
    context = {}

    return HttpResponse(template.render(context, request))


def student_department_courses(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'student':
        return redirect('/login')
    template = loader.get_template('student/department_courses.html')
    departments = Department.objects.all()
    context = {
        'departments': departments
    }

    return HttpResponse(template.render(context, request))


def student_department_courses_result(request):
    if not request.session.get("user_id") or request.session.get("login_as") != 'student':
        return redirect('/login')
    department = request.GET.get('department')
    semester = request.GET.get('semester')
    year = request.GET.get('year')

    with connection.cursor() as cursor:
        cursor.execute("SELECT section.*, course.dept_name, course.title FROM section "
                       "JOIN course ON course.course_id = section.course_id "
                       "WHERE course.dept_name = %s AND section.semester = %s AND section.year = %s",
                       [department, semester, year])

        columns = [col[0] for col in cursor.description]
        course_sections = [dict(zip(columns, row)) for row in cursor.fetchall()]

    template = loader.get_template('student/department_courses_result.html')
    context = {
        'course_sections': course_sections
    }

    return HttpResponse(template.render(context, request))
