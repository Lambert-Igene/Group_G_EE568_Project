from django.http import HttpResponse
from django.template import loader


def login(request):
    template = loader.get_template('login.html')
    context = {}

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