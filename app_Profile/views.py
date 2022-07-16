from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count
from django.views.generic import ListView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from . import forms
from app_Installments.models import Installments
from app_Saving.models import Saving
from app_Bills.models import Bill

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
        context['factor'] = {
            "this_month": {
                "total": 0,
                "received": 0,
                "payment": 0
            },
            "this_week": {
                "total": 0,
                "received": 0,
                "payment": 0
            },
            "today": {
                "total": 0,
                "received": 0,
                "payment": 0
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
