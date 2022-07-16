from django.urls import path
from django.contrib.auth import views as dviews

from . import views

app_name = 'Profile'
urlpatterns = [
    path('login/', dviews.LoginView.as_view(), name="login"),
    path('logout/', dviews.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileChangePasswordView.as_view(), name='account'),
    path('account/', views.ChangeUserProfileView.as_view(), name='profile'),

    path('register/', views.RegisterView, name="register"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard")
]
