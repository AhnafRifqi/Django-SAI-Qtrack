from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('log/new/', views.log_create_view, name='log_create'),
    path('logs/', views.log_list_view, name='log_list'),
]
