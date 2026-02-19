from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TimetableListView.as_view(), name='timetable_list'),
    path('add/', views.TimetableCreateView.as_view(), name='timetable_add'),
    path('<int:pk>/edit/', views.TimetableUpdateView.as_view(), name='timetable_edit'),
    path('<int:pk>/delete/', views.TimetableDeleteView.as_view(), name='timetable_delete'),
]
