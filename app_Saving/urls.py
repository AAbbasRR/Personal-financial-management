from django.urls import path

from . import views

app_name = 'Saving'
urlpatterns = [
    path('', views.SavingListCreateView.as_view(), name="listsaving"),
    path('create/', views.SavingListCreateView.as_view(), name="createsaving"),
    path('delete/<int:pk>/', views.SavingDeleteView.as_view(), name="deletesaving"),
    path('payment/<int:pk>/', views.PaymentSavingView.as_view(), name="paymentesaving"),
]
