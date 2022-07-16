from django.urls import path

from . import views

app_name = 'Check'
urlpatterns = [
    path('', views.CheckCreateListView.as_view(), name="listcheck"),
    path('create/', views.CheckCreateListView.as_view(), name="createcheck"),
    path('delete/<int:pk>/', views.CheckDeleteView.as_view(), name="deletecheck"),
    path('set_success/<int:pk>/', views.CheckSetSuccessView.as_view(), name="setsuccesscheck"),
    path('set_failure/<int:pk>/', views.CheckSetFailureView.as_view(), name="setfailurecheck"),
]
