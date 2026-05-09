from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/redirect/', views.role_redirect, name='role_redirect'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/profile/edit/', views.customer_profile_edit, name='customer_profile_edit'),
    path('cook/dashboard/', views.cook_dashboard, name='cook_dashboard'),
    path('platform-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
