from django.urls import path

from . import views

app_name = 'DebtDemand'
urlpatterns = [
    path('', views.DebtDemandCreateListView.as_view(), name="listdebtdamends"),
    path('create/', views.DebtDemandCreateListView.as_view(), name="creatdebtdemand"),
    path('payment/<int:pk>/', views.DebtDemandCloseView.as_view(), name="paymentdebtdemand"),
    path('delete/<int:pk>/', views.DebtDemandDeleteView.as_view(), name="deletedebtdemand"),
]
