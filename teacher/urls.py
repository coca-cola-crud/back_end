from django.urls import path
from teacher import sign_in_out,personal_info,grade_manage
urlpatterns = [
    path('teacher/sign/', sign_in_out.signin),
    path('teacher/PersonalInformation/', personal_info.list_info),
    path('teacher/GradeManage/', grade_manage.dispatcher),
]