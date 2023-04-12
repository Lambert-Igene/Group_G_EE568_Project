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
    template = loader.get_template('admin/roaster.html')
    context = {}

    return HttpResponse(template.render(context, request))

def salary(request):
    template = loader.get_template('admin/salary.html')
    context = {}

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