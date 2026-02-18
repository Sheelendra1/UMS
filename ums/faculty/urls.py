from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('list/', views.faculty_list, name='faculty_list'),
    path('add/', views.add_faculty, name='add_faculty'),
]
