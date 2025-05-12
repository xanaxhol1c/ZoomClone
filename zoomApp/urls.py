from django.urls import path
from . import views

app_name = "zoomApp"

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('meeting/', views.meeting, name="meeting"),
    path('join/', views.join_meeting, name="join_meeting"),
    path('partials/login/', views.login_form_partial, name="login_form_partial"),
    path('partials/register/', views.register_form_partial, name="register_form_partial")
]
