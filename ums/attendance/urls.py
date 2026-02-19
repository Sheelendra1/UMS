from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.attendance_list, name='attendance_list'),
    path('<int:pk>/detail/', views.attendance_detail, name='attendance_detail'),
    path('export/', views.attendance_export, name='attendance_export'),
]
