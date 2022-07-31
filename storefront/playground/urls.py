from django.urls import path
from . import views

#URLConf for playground
urlpatterns = [
  path('hello/', views.say_hello)
]