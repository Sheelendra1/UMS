from django.urls import path
from django.shortcuts import redirect
from . import views


def home_redirect(request):
    """Root URL: send to dashboard (which requires login → role check)."""
    return redirect('dashboard_redirect')


urlpatterns = [
    # Root → login → dashboard flow
    path('', home_redirect, name='home'),

    # Admin dashboard & settings
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('settings/', views.settings_view, name='settings'),

    # Common / Public pages
    path('about/', views.about_university, name='about_university'),
    path('contact/', views.contact_page, name='contact_page'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
    
    # Global Search
    path('search/', views.global_search, name='global_search'),
]
