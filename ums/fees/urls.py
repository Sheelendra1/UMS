from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('structures/', views.FeeStructureListView.as_view(), name='fee_structure_list'),
    path('structures/add/', views.FeeStructureCreateView.as_view(), name='fee_structure_add'),
    path('payments/', views.FeePaymentListView.as_view(), name='fee_payment_list'),
    path('payments/add/', views.FeePaymentCreateView.as_view(), name='fee_payment_add'),
]
