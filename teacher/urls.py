from django.urls import path
from teacher import sign_in_out,personal_info
urlpatterns = [
    path('teacher/sign/', sign_in_out.signin),
    path('teacher/PersonalInformation/', personal_info.list_info),
]