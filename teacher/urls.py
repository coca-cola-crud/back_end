from django.urls import path
from teacher import sign_in_out,personal_info,grade_manage,password
urlpatterns = [
    path('teacher/sign/', sign_in_out.signin),
    path('teacher/PersonalInformation/', personal_info.list_info),
    path('teacher/GradeManage/', grade_manage.dispatcher),
    path('teacher/password/alter',password.alterpassword),
    path('teacher/password/verify',password.verify),
]