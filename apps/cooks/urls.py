from django.urls import path

from .views import cook_application_status_view, cook_apply_view

app_name = 'cooks'

urlpatterns = [
    path('cook/apply/', cook_apply_view, name='cook_apply'),
    path('cook/application/status/', cook_application_status_view, name='cook_application_status'),
]
