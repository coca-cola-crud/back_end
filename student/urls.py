from django.urls import path

from student import personal_info
from student import sign_in_out
urlpatterns = [
    path('PersonalInformation/', personal_info.list_info),
    path('student/sign/', sign_in_out.signin),
]