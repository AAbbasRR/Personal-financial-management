from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models.functions import TruncWeek, TruncMonth, TruncDay
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import ListView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from . import forms
from app_Installments.models import Installments
from app_Saving.models import Saving
from app_Bills.models import Bill
from app_Transactions.models import Transaction

User = get_user_model()


def RegisterView(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("Profile:login"))
    else:
        form = forms.SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


class DashboardView(LoginRequiredMixin, ListView):
    model = User
    template_name = "panel/index.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['cards'] = {
            "total_bill": Bill.objects.filter(user=self.request.user).count(),
            'count_installments': Installments.objects.filter(user=self.request.user, status="OPN").count(),
            'total_saving': Saving.objects.filter(user=self.request.user).aggregate(Sum('amount'))['amount__sum']
        }
        today = timezone.now().date()

        month_received = list(Transaction.objects.filter(user=self.request.user, condition='ADT', created_date__year=today.year).annotate(month=TruncMonth('created_date')).values('month').annotate(sum_amount=Sum('amount')).values('month', 'sum_amount'))[-1]
        month_payment = list(Transaction.objects.filter(user=self.request.user, condition='DET', created_date__year=today.year).annotate(month=TruncMonth('created_date')).values('month').annotate(sum_amount=Sum('amount')).values('month', 'sum_amount'))[-1]

        week_received = list(Transaction.objects.filter(user=self.request.user, condition='ADT', created_date__year=today.year).annotate(week=TruncWeek('created_date')).values('week').annotate(sum_amount=Sum('amount')).values('week', 'sum_amount'))[-1]
        week_payment = list(Transaction.objects.filter(user=self.request.user, condition='DET', created_date__year=today.year).annotate(week=TruncWeek('created_date')).values('week').annotate(sum_amount=Sum('amount')).values('week', 'sum_amount'))[-1]

        today_received = list(Transaction.objects.filter(user=self.request.user, condition='ADT', created_date__year=today.year, created_date__month=today.month, created_date__day=today.day).annotate(day=TruncDay('created_date')).values('day').annotate(sum_amount=Sum('amount')).values('sum_amount'))[-1]
        today_payment = list(Transaction.objects.filter(user=self.request.user, condition='DET', created_date__year=today.year, created_date__month=today.month, created_date__day=today.day).annotate(day=TruncDay('created_date')).values('day').annotate(sum_amount=Sum('amount')).values('sum_amount'))[-1]
        context['factor'] = {
            "this_month": {
                "total": month_received['sum_amount'] - month_payment['sum_amount'],
                "received": month_received['sum_amount'],
                "payment": month_payment['sum_amount']
            },
            "this_week": {
                "total": week_received['sum_amount'] - week_payment['sum_amount'],
                "received": week_received['sum_amount'],
                "payment": week_payment['sum_amount']
            },
            "today": {
                "total": today_received['sum_amount'] - today_payment['sum_amount'],
                "received": today_received['sum_amount'],
                "payment": today_payment['sum_amount']
            }
        }
        return context


class ProfileChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'panel/profile.html'
    success_url = reverse_lazy("Profile:account")


class ChangeUserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.UpdateProfileForm
    success_url = reverse_lazy('Profile:account')

    def get_success_url(self):
        return HttpResponseRedirect(reverse('Profile:account'))

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        user_obj = self.get_object()
        user_form = forms.UpdateProfileForm(data=request.POST, instance=user_obj)
        if user_form.is_valid():
            user_form.save()
            return self.get_success_url()
