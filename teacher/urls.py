from django.urls import path
from teacher import sign_in_out
urlpatterns = [
    path('teacher/sign/', sign_in_out.signin),
]