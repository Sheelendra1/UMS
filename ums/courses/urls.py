from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.CourseListView.as_view(), name='course_list'),
    path('add/', views.CourseCreateView.as_view(), name='course_add'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('<int:pk>/enroll/', views.enroll_students, name='course_enroll'),
]
