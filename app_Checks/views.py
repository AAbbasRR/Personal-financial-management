from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import Check
from .forms import CheckCreateForm


class CheckCreateListView(LoginRequiredMixin, CreateView):
    model = Check
    form_class = CheckCreateForm
    template_name = "panel/checks.html"
    success_url = reverse_lazy("Check:listcheck")

    def form_valid(self, form):
        check_object = form.save(commit=False)
        check_object.user = self.request.user
        return super(CheckCreateListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CheckCreateListView, self).get_context_data(**kwargs)
        context['checks_payment_list'] = {
            "during": Check.objects.filter(user=self.request.user, type="PAY", status="DUR"),
            "successful": Check.objects.filter(user=self.request.user, type="PAY", status="SUC"),
            "failure": Check.objects.filter(user=self.request.user, type="PAY", status="FIL"),
        }
        context['checks_received_list'] = {
            "during": Check.objects.filter(user=self.request.user, type="REC", status="DUR"),
            "successful": Check.objects.filter(user=self.request.user, type="REC", status="SUC"),
            "failure": Check.objects.filter(user=self.request.user, type="REC", status="FIL"),
        }
        return context


class CheckSetSuccessView(LoginRequiredMixin, UpdateView):
    model = Check
    success_url = reverse_lazy("Check:listcheck")

    def get_success_url(self):
        return HttpResponseRedirect(reverse("Check:listcheck"))

    def get_queryset(self):
        return Check.objects.filter(user=self.request.user, status="DUR")

    def get(self, request, *args, **kwargs):
        check_object = self.get_object()
        if check_object:
            check_object.status = "SUC"
            check_object.save()
            return self.get_success_url()


class CheckSetFailureView(LoginRequiredMixin, UpdateView):
    model = Check
    success_url = reverse_lazy("Check:listcheck")

    def get_success_url(self):
        return HttpResponseRedirect(reverse("Check:listcheck"))

    def get_queryset(self):
        return Check.objects.filter(user=self.request.user, status="DUR")

    def get(self, request, *args, **kwargs):
        check_object = self.get_object()
        if check_object:
            check_object.status = "FIL"
            check_object.save()
            return self.get_success_url()


class CheckDeleteView(LoginRequiredMixin, DeleteView):
    model = Check
    success_url = reverse_lazy("Check:listcheck")

    def get_queryset(self):
        return Check.objects.filter(Q(user=self.request.user), Q(status='SUC') | Q(status='FIL'))

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
