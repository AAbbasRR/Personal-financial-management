"""Accounting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LoginView.as_view()),

    # apps
    path('profile/', include('app_Profile.urls')),
    path('installments/', include('app_Installments.urls')),
    path('debts_demands/', include('app_DebtDemand.urls')),
    path('bills/', include('app_Bills.urls')),
    path('receipts/', include('app_Receipt.urls')),
    path('savings/', include('app_Saving.urls')),
    path('check/', include('app_Checks.urls')),
    path('options/', include('app_Options.urls')),
    path('transactions/', include('app_Transactions.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
