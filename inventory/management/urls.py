from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 
from django.contrib import admin
from django.urls import path
from inventory import settings
from management import views, extra_views

app_name='management'

urlpatterns = [
    path('', views.LogInView.as_view(), name='signin'),
    path('new-user/', views.RegisterView.as_view(), name='new-user'), 
    ####
    path('overview/', views.HomePageView.as_view(), name = 'overview'),
    path('dashboard/', views.DashboardView.as_view(), name = 'dashboard'),
    path('edit-device/<int:pk>/', views.DeviceEditView.as_view(), name='edit-device'),
    ####
    path('profile/', views.ProfileView.as_view(), name = 'profile'),
    path('sign-out/', extra_views.log_user_out, name='logout'),
    ####
    path('delete-brand/', login_required(extra_views.delete_brand), name='delete-brand'),
    path('delete-device/', login_required(extra_views.delete_device), name='delete-device'),
    ####
    path('delete-user/', login_required(extra_views.delete_user), name='delete-user'),
    ####
] 