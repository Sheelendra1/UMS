from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.DepartmentListView.as_view(), name='department_list'),
    path('add/', views.DepartmentCreateView.as_view(), name='department_add'),
    path('<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_edit'),
    path('<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
]
