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

def index(request):
    template = loader.get_template('university/***.html')
    context = {}

    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('university/***.html')
    context = {}

    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('university/***.html')
    context = {}

    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('university/***.html')
    context = {}

    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('university/***.html')
    context = {}

    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('university/***.html')
    context = {}

    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('university/***.html')
    context = {}

    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('university/***.html')
    context = {}

    return HttpResponse(template.render(context, request))