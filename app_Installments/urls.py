from django.urls import path

from . import views

app_name = 'Installments'
urlpatterns = [
    path('', views.InstallmentCreateListView.as_view(), name="listinstallments"),
    path('create/', views.InstallmentCreateListView.as_view(), name="createinstallments"),
    path('close/<int:pk>/', views.InstallmentCloseView.as_view(), name="closeinstallments"),
    path('delete/<int:pk>/', views.InstallmentDeleteView.as_view(), name="deleteinstallments"),
    path('payment/<int:pk>/', views.PaymentInstallmentView.as_view(), name="paymentinstallments"),
]
