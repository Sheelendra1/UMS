from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.NoticeListView.as_view(), name='notice_list'),
    path('add/', views.NoticeCreateView.as_view(), name='notice_add'),
    path('<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='notice_delete'),
]
