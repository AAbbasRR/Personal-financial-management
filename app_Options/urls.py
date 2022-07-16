from django.urls import path

from . import views

app_name = 'Options'
urlpatterns = [
    path('', views.NotificationOptionCreateListView.as_view(), name="listnotificationoption"),
    path('create/', views.NotificationOptionCreateListView.as_view(), name="createnotificationoption"),
    path('update/<int:pk>/', views.NotificationOptionUpdateView.as_view(), name="updatenotificationoption"),
    path('delete/<int:pk>/', views.NotificationOptionDeleteView.as_view(), name="deletenotificationoption"),
]
