from django.urls import path

from . import views

app_name = 'Bill'
urlpatterns = [
    path('', views.BillCreateListView.as_view(), name="listbills"),
    path('create/', views.BillCreateListView.as_view(), name="creatbill"),
    path('delete/<int:pk>/', views.BillDeleteView.as_view(), name="deletebill"),
]
