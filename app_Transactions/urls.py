from django.urls import path

from . import views

app_name = 'Transaction'
urlpatterns = [
    path('', views.TransactionCreateListView.as_view(), name="listtransactions"),
    path('create/', views.TransactionCreateListView.as_view(), name="createtransactions"),
]
