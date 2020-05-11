from django.urls import path

from admin import student_info,sign_in_out,teacher_info,course_info, personal_info

urlpatterns = [
    path('admin/PersonalInformation/', personal_info.list_info),
    path('admin/sign/', sign_in_out.signin),
    path('admin/student_info/', student_info.dispatcher),
    path('admin/teacher_info/', teacher_info.dispatcher),
    path('admin/course_info/',course_info.dispatcher)
]