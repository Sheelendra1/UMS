from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ExamListView.as_view(), name='exam_list'),
    path('add/', views.ExamCreateView.as_view(), name='exam_add'),
    path('<int:pk>/edit/', views.ExamUpdateView.as_view(), name='exam_edit'),
    path('<int:pk>/delete/', views.ExamDeleteView.as_view(), name='exam_delete'),
    path('<int:pk>/results/', views.result_entry, name='result_entry'),
]
