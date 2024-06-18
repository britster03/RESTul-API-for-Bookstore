from django.contrib import admin
from .views import *
from django.urls import path, include


urlpatterns = [
        path('student/',StudentAPI.as_view()),
        path('pdf/',GeneratePDF.as_view()),
        path('generic-student/',StudentGeneric.as_view()),
        path('generic-student/',StudentGeneric1.as_view()),
        path('register/',RegisterUser.as_view()),
        path('get-book/', get_book)
]

