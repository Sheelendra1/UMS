from django.urls import path
from . import views

urlpatterns = [
    # ── Admin-facing routes (backward compat) ──────────
    path('structures/', views.FeeStructureListView.as_view(), name='fee_structure_list'),
    path('structures/add/', views.FeeStructureCreateView.as_view(), name='fee_structure_add'),
    path('structures/<int:pk>/edit/', views.FeeStructureUpdateView.as_view(), name='fee_structure_edit'),
    path('structures/<int:pk>/delete/', views.FeeStructureDeleteView.as_view(), name='fee_structure_delete'),
    path('payments/', views.FeePaymentListView.as_view(), name='fee_payment_list'),
    path('payments/add/', views.FeePaymentCreateView.as_view(), name='fee_payment_add'),
    path('payments/<int:payment_id>/download/', views.download_receipt_admin, name='fee_receipt_download_admin'),


    # ── Accountant Panel (6 pages) ─────────────────────
    # 1. Dashboard
    path('dashboard/', views.accountant_dashboard, name='accountant_dashboard'),

    # 2. Collect Fees
    path('collect/', views.accountant_collect_fees, name='accountant_collect_fees'),

    # 3. Payment History
    path('history/', views.accountant_payment_history, name='accountant_payment_history'),
    path('receipt/<int:payment_id>/', views.accountant_receipt, name='accountant_receipt'),

    # 4. Financial Reports
    path('reports/', views.accountant_reports, name='accountant_reports'),
    path('reports/export/', views.accountant_reports_export, name='accountant_reports_export'),

    # 5. Notices
    path('notices/', views.accountant_notices, name='accountant_notices'),
    path('notices/post/', views.accountant_post_notice, name='accountant_post_notice'),

    # 6. Profile
    path('profile/', views.accountant_profile, name='accountant_profile'),
]
