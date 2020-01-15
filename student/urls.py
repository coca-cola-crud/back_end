from django.urls import path

from student import personal_info
from student import sign_in_out
from student import select_course
urlpatterns = [
    path('PersonalInformation/', personal_info.list_info),
    path('student/sign/', sign_in_out.signin),
    path('student/select_course/', select_course.dispatcher),
]