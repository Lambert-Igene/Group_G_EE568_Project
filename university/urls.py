"""Group_G_EE568_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from university import views

urlpatterns = [
    path('', views.login, name='index'),
    path('login', views.login, name='login'),
    path('admin', views.admin, name='admin'),
    path('admin/roaster', views.roaster, name='admin_roaster'),
    path('admin/salary', views.salary, name='admin_salary'),
    path('admin/performance', views.performance, name='admin_performance'),
    path('admin/performance_result', views.performance_result, name='admin_performance_result'),
    path('professor', views.professor, name='professor'),
    path('professor/courses', views.courses, name='professor_courses'),
    path('professor/course_students', views.course_students, name='professor_course_students'),
    path('student', views.student, name='student'),
    path('student/department_courses', views.department_courses, name='student.department_courses'),

]
