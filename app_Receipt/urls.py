from django.urls import path

from . import views

app_name = 'Receipt'
urlpatterns = [
    path('', views.ReceiptCreateListView.as_view(), name="listreceipt"),
    path('create/', views.ReceiptCreateListView.as_view(), name="createreceipt"),
    path('delete/<int:pk>/', views.ReceiptDeleteView.as_view(), name="deletereceipt"),
]
